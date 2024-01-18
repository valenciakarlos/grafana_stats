# Graphs CPU and Memory for the Ericsson provided Stats
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file
# 3. -w <worker> Name of the worker we want to monitor (Only one worker can be used for now)

import argparse
import os


def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-w", "--worker",
                        help="Name of the worker we want to monitor (Only one worker can be used for now)",
                        required=True)

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
    WORKER="standard5gc-htnp-b9f7d6d9b-z574b"
    python CPU_and_Memory.py -p /Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/ -f n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv -n n294-esxi-ht-04 -w standard5gc-htnp-b9f7d6d9b-z574b
'''


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)
    WORKER = args.worker
    # Strings used for the CPU and Memory metrics
    STRING_CPU = "Nodes CPU usage:" + WORKER
    STRING_MEM = "Nodes Memory usage:" + WORKER

    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)

    print("Worker:", WORKER)

    # Reference https://pandas.pydata.org/docs/user_guide/10min.html
    # Reading the data frame
    import pandas as pd
    df = pd.read_csv(FILE_PATH)

    x_values = df["Time"]
    y_values_CPU = df[STRING_CPU]
    y_values_memory = df[STRING_MEM]

    '''
    y_values_CPU = df["Nodes CPU usage:standard5gc-htnp-b9f7d6d9b-z574b"]
    y_values_memory = df["Nodes Memory usage:standard5gc-htnp-b9f7d6d9b-z574b"]
    '''

    # Setting two scales. One for CPU one for Memory
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Sample')
    ax1.set_ylabel('CPU Usage', color=color)

    CPU_MAX = y_values_CPU.max()
    formatted_cpu_max = f"{CPU_MAX:.2f}"

    CPU_MEAN = y_values_CPU.mean()
    formatted_cpu_mean = f"{CPU_MEAN:.2f}"

    CPU_LEGEND = "Max CPU  :" + formatted_cpu_max + "\n" + "Mean CPU:" + formatted_cpu_mean
    ax1.plot(x_values, y_values_CPU, color=color, label=CPU_LEGEND)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Memory Usage', color=color)  # we already handled the x-label with ax1

    MEM_MAX = y_values_memory.max()
    formatted_mem_max = f"{MEM_MAX:.2f}"

    MEM_MEAN = y_values_memory.mean()
    formatted_mem_mean = f"{MEM_MEAN:.2f}"
    MEM_LEGEND = "Max Mem :" + formatted_mem_max + "\n" + "Mean Mem:" + formatted_mem_mean

    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(x_values, y_values_memory, color=color, label=MEM_LEGEND)
    ax2.legend(loc="lower right")

    # Add configured CPU Legend
    ax1.legend(loc="upper left")

    # To organize the X axis labels
    tick_interval = 30
    plt.xticks(x_values[::tick_interval], rotation=90)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title("CPU and Memory Usage for "+WORKER)
    plt.show()









