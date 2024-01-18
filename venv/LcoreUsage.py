# Graphs Usage all Lcores
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

    return args

'''
    Can use these for now:
    DIR = "/Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/"
    FILE = "n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv"
    FULL_PATH = DIR + FILE
    HOSTNAME="n294-esxi-ht-04"
    python LcoreUsage.py -p /Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/ -f n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv -n n294-esxi-ht-04

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

    columns_list = df.columns.tolist()
    print("Number of original columns=" + str(df.shape[1]))
    index = 0
    print("Entries that matched "+lcoreusage_pattern+":")
    for col in columns_list:
        # print("col="+str(index)+" Name="+col)
        # Match a particular host
        if re.match(lcoreusage_pattern, col):
            print("col=" + str(index) + " Name=" + col)
        index = index + 1

    # Plot all the cores.
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.step.html
    # Not too readable
    # Filter to a df

    lcoreusage_df = df.filter(regex=lcoreusage_pattern)


    import matplotlib.pyplot as plt

    columns_list = lcoreusage_df.columns.tolist()
    plt.plot(df['Time'], lcoreusage_df, label=columns_list)

    plt.xlabel('Time')
    plt.ylabel('%')
    plt.title('Lcore usage graph')

    # plt.legend(loc='lower right')
    # This so the series are displayed on a separate box to the side on the upper left.
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 10
    plt.xticks(df['Time'][::tick_interval], rotation=90)

    plt.show()



