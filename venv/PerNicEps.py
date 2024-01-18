# Shows per NIC Tx and Rx EPS on a particular VM
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file
# 3. -h <hostname> Name of the host we want to extract
# 4. -w <worker> Name of the worker node we want to graph

import argparse
import os


def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-n", "--name", help="HOSTNAME to parse stats for", required=True)
    parser.add_argument("-w", "--worker", help="Name of the worker we want to graph", required=True)



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
    WORKER="standard5gc-htnp-b9f7d6d9b-z574b"
    python PerLcoreUsage.py -p /Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/ -f n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv -n n294-esxi-ht-04 -w standard5gc-htnp-b9f7d6d9b-z574b

'''


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)
    HOSTNAME = args.name
    WORKER = args.worker


    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)
    print("Hostname:", HOSTNAME)
    print("Worker:", WORKER)


    # Reference https://pandas.pydata.org/docs/user_guide/10min.html
    # Reading the data frame
    import pandas as pd
    import re

    df = pd.read_csv(FILE_PATH)

    # Matching lcore usage pattern and dropping to a DF
    # Match looks like this: EDP lcore CPU usage:n294-esxi-ht-04.sc.sero.gic.ericsson.se-lcoreusage-Ens-Lcore-0


    #VM_EPS = r'Time|.*' + WORKER + '.*rxeps$'
    # For Tx and Rx EPS (which is where I am seeing the drops)
    VM_EPS = r'.*' + WORKER + '.*[t|r]xeps$'

    # For Tx EPS (which is where I am seeing the drops)
    #VM_EPS = r'.*' + WORKER + '.*txeps$'

    print("per VM EPS pattern=" + VM_EPS)
    vm_eps_df = df.filter(regex=VM_EPS)



    print(vm_eps_df)

    import matplotlib.pyplot as plt
    from common import decide_format
    columns_list = vm_eps_df.columns.tolist()
    print(columns_list)
    plt.plot(df['Time'], vm_eps_df,label=columns_list)



    # plt.legend(loc='lower right')





    plt.xlabel('Time')
    plt.ylabel('EPS')
    plt.title("EPS for "+WORKER)
    # This so the series are displayed on a separate box to the side on the upper left.
    #plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.legend(loc='best')

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 5
    plt.xticks(df['Time'][::tick_interval], rotation=90)



    plt.show()



'''
    # Trying with a function. Not working right now
    from common import single_axis_plot

    single_axis_plot(df['Time'], vm_eps_df, "Time", "EPS for " + WORKER)
'''

