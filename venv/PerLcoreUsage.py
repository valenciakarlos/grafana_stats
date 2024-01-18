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
    lcoreusage_pattern = r'Time|.*' + HOSTNAME + '.*-lcoreusage-Ens-Lcore-'+str(LCORE)+"$"





    # Filter to a df

    lcoreusage_df = df.filter(regex=lcoreusage_pattern)

    print("Usage table:")
    print(lcoreusage_df)

    import matplotlib.pyplot as plt
    from common import decide_format
    columns_list = lcoreusage_df.columns.tolist()


    x_values = lcoreusage_df[columns_list[0]]   # Time
    y_values = lcoreusage_df[columns_list[1]]   # Lcore usage


    STRING_TPUT = "Dallas Throughput:"
    STRING_PKTLOSS = "Dallas E2E Packet loss:"

    # Obtain Throuput and packet loss values
    tput_values=df[STRING_TPUT]
    pktloss_values=df[STRING_PKTLOSS]

    MAX_USAGE=str(y_values.max())
    MEAN_USAGE=str(decide_format(y_values.mean()))
    # Detect first time Max was found
    first_max_value=y_values.idxmax()
    TIME_FIRST_MAX=x_values[first_max_value]
    TPUT_AT_MAX=str(decide_format(tput_values[first_max_value]))
    Y_AXIS_LEGEND="MAX:"+MAX_USAGE+"\n" + "MEAN:"+MEAN_USAGE+"\n"+"First Max:"+TIME_FIRST_MAX+"\nTPUT="+TPUT_AT_MAX

    plt.plot(x_values, y_values, label=Y_AXIS_LEGEND)

    plt.xlabel('Time')
    plt.ylabel('%')
    plt.ylim([0,105])
    plt.title(columns_list[1])

    plt.legend(loc='lower right')

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 5
    plt.xticks(lcoreusage_df[columns_list[0]][::tick_interval], rotation=90)



    plt.show()



