# Graphs Usage per Lcore (or ALL if not specified)
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file
# 3. -h <hostname> Name of the host we want to extract

import argparse
import os


def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-n", "--name", help="HOSTNAME to parse stats for", required=True)




    args = parser.parse_args()

    # Further validate the arguments

    # Check if the path exists
    if not os.path.exists(args.path):
        parser.error(f"The provided path '{args.path}' does not exist.")

    # Check with the file exists
    file_path = os.path.join(args.path, args.filename)
    if not os.path.exists(file_path):
        parser.error(f"The specified file '{file_path}' does not exist in the provided path.")
    print(type(args))
    return args

'''
    Can use these for now:
    DIR = "/Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/""
    FILE = "n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv"
    FULL_PATH = DIR + FILE
    HOSTNAME="n294-esxi-ht-04"

'''


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)
    HOSTNAME = args.name



    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)
    print("Hostname:", HOSTNAME)



    # Reference https://pandas.pydata.org/docs/user_guide/10min.html
    # Reading the data frame
    import pandas as pd
    df = pd.read_csv(FILE_PATH)

    # Matching lcore usage pattern and dropping to a DF
    import re
    lcoreusage_pattern = r'.*' + HOSTNAME + '.*-lcoreusage'

    # Filter to a df

    #  Match for Time , lcore Usage and pps
    lcore_usage_pps_pattern = r'Time|.*' + HOSTNAME + '.*-lcoreusage-Ens-Lcore-[0-9]+$|.*' + HOSTNAME + '.*-pps-Ens-Lcore-[0-9]+$'



    lcoreusage_df = df.filter(regex=lcoreusage_pattern)
    lcoreusage_pps_df=df.filter(regex=lcore_usage_pps_pattern)
    from common import lcore_insight
    from common import analyze_df_cols
    #lcore_insight(lcoreusage_df)

    print("Lcore Usage pps:")
    #print(lcoreusage_pps_df)
    lcore_insight(lcoreusage_pps_df)



    # Plotting lcores
    # This method allow for more customization
    import matplotlib.pyplot as plt

    # Extracts all columns which will be as many lcores as on the original data frame
    columns_list = lcoreusage_df.columns.tolist()


    # Define the number of subplots based on the number of series
    num_subplots = len(columns_list)

    # Create subplots
    fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 5 * num_subplots), sharex=True)

    # Here I want to plot against time on x values axis. That is still on original data frame
    x_values = df["Time"]

    # Plot each series in a separate subplot
    for i, column in enumerate(columns_list):
        SERIES_LABEL = column + " Max= " + str(lcoreusage_df[column].max())
        axes[i].plot(df['Time'], lcoreusage_df[column], label=SERIES_LABEL)
        axes[i].set_ylabel("Pct")
        # Fixing so y percentage scale is always between 0 and 100%
        axes[i].set_ylim([0, 105])
        axes[i].legend()

    # Set common x-axis label and adjust layout
    plt.xlabel('Time')

    # To organize the X axis labels
    tick_interval = 25
    plt.xticks(x_values[::tick_interval], rotation=90)

    # Show the plot
    plt.show()

