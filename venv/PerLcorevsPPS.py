# Graphs Usage per Lcore of usage vs PPS
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file
# 3. -h <hostname> Name of the host we want to extract
# 4. -l <lcore>

import argparse
import os



# start validate arguments function
# Validates that all arguments are provided and that the file name exists

def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-n", "--name", help="HOSTNAME to parse stats for", required=True)
    parser.add_argument("-l", "--lcore", help="Lcore to parse stats for. Will do all if not specified", required=True)
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
# End validate arguments function

'''
    Can use these for now:
    DIR = "/Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/"
    FILE = "n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv"
    FULL_PATH = DIR + FILE
    HOSTNAME="n294-esxi-ht-04"
    python PerLcoreUsage.py -p /Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/ -f n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv -n n294-esxi-ht-04 -l 3

'''


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)
    HOSTNAME = args.name
    LCORE = args.lcore
    # Match on Lcore usage and pps
    #  Combination of both patterns
    lcore_usage_pps_pattern = r'Time|.*' + HOSTNAME + '.*-lcoreusage-Ens-Lcore-' + str(LCORE) + '$|.*' + HOSTNAME + '.*-pps-Ens-Lcore-' + str(LCORE) + '$'




    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)
    print("Hostname:", HOSTNAME)
    print("Lcore:", str(LCORE))


    # Reference https://pandas.pydata.org/docs/user_guide/10min.html
    # Reading the data frame
    import pandas as pd
    df = pd.read_csv(FILE_PATH)

    # Matching lcore usage pattern and dropping to a DF
    # Match looks like this: EDP lcore CPU usage:n294-esxi-ht-04.sc.sero.gic.ericsson.se-lcoreusage-Ens-Lcore-0
    import re


    # Filter to a df

    lcore_usage_pps_pattern_df = df.filter(regex=lcore_usage_pps_pattern)
    # Resulting Data frame has Time, lcore usage series and lcore pps series
    print("Pattern is "+lcore_usage_pps_pattern)
    print(lcore_usage_pps_pattern_df.columns[1])


    # Import dual axis plot from the common library
    from common import dual_axis_plot
    x_axis=lcore_usage_pps_pattern_df.columns[0]
    lcore_usage=lcore_usage_pps_pattern_df.columns[1]
    lcore_pps=lcore_usage_pps_pattern_df.columns[2]

    dual_axis_plot(lcore_usage_pps_pattern_df[x_axis],lcore_usage_pps_pattern_df[lcore_usage], lcore_usage_pps_pattern_df[lcore_pps],"Time","Lcore Usage","MPPS")




