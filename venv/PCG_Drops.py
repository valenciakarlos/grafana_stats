# Prints the Columns on a dataframe
def print_df_cols(dataframe):
    columns_list = dataframe.columns.tolist()
    print("Number of columns=" + str(dataframe.shape[1]))
    columns_list = dataframe.columns.tolist()
    for index, col in enumerate(columns_list):
        print(f'Index {index}: {col}')




def validate_arguments():
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-n", "--name", help="HOSTNAME to parse stats for", required=True)
    parser.add_argument("-w", "--worker", help="Worker node to parse stats for", required=True)



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









# Reference https://pandas.pydata.org/docs/user_guide/10min.html
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

DIR="/Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/"
FILE="n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv"
VM_PATTERN = r'standard5gc-htnp-b9f7d6d9b-z574b'
HOSTNAME="n294-esxi-ht-04"


args = validate_arguments()

FULL_PATH = os.path.join(args.path, args.filename)

#VM_PATTERN = r'standard5gc-htnp-b9f7d6d9b-z574b'
VM_PATTERN=args.worker

#HOSTNAME="n294-esxi-ht-04"
HOSTNAME = args.name

# Now you can use the validated arguments in your code.
print("Processing")
print("Filename:", FULL_PATH)
print("Hostname:", HOSTNAME)
print("Worker: ", VM_PATTERN)



df = pd.read_csv(FULL_PATH)

import re


from common import analyze_df_cols

'''
Index 589: pNIC RX Drop Rate net-stats:n294-esxi-ht-04.sc.sero.gic.ericsson.se-vmnic9-rxeps
Index 590: pNIC Driver RX Drop Rate net-s:n294-esxi-ht-01.sc.sero.gic.ericsson.se-vmnic4-rxeps
'''

PCG_DROPS = r'Time|PCG.*drop.*'

pcg_drops_df = df.filter(regex=PCG_DROPS)
print("Lines matching PCG Drops:"+PCG_DROPS)
analyze_df_cols(pcg_drops_df)
















