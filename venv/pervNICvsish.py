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


    # For Rx Packet drops
    VSI_PKT_DROP_PATTERN = r'.*vsish.*' + WORKER + '.*[T|R]x'




    print("per VM vsi Packet drop pattern=" + VSI_PKT_DROP_PATTERN)
    vsi_dropped_df = df.filter(regex=VSI_PKT_DROP_PATTERN)



    print(vsi_dropped_df)

    '''
    See if tuple unpacking works with df
    something like:
    VSI_PKT_DROP_PATTERN = r'Time|.*vsish.*' + WORKER + '.*Rx'
    x_axis, *vsi_dropped_df = vsi_dropped_df
    
    import pandas as pd

# Assuming df is your DataFrame
data = {'Name': ['John', 'Jane', 'Bob'],
        'Age': [25, 30, 22],
        'City': ['New York', 'San Francisco', 'Seattle']}

df = pd.DataFrame(data)

# Removing the 'Name' column from the original DataFrame
df = df.drop('Name', axis=1)

# Displaying the modified DataFrame
print(df)

can even drop in placE:
# Removing the 'Name' column from the original DataFrame in-place
df.drop('Name', axis=1, inplace=True)



    '''

    import matplotlib.pyplot as plt
    from common import decide_format
    columns_list = vsi_dropped_df.columns.tolist()
    print(columns_list)



    plt.plot(df['Time'], vsi_dropped_df,label=columns_list)



    # plt.legend(loc='lower right')





    plt.xlabel('Time')
    plt.ylabel('Pkts Dropped')
    plt.title("Packets Dropped for "+WORKER)
    # This so the series are displayed on a separate box to the side on the upper left.
    #plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.legend(loc='best')

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 5
    plt.xticks(df['Time'][::tick_interval], rotation=90)



    plt.show()



