# Graphs CPU and Memory for the Ericsson provided Stats
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file


import argparse
import os


def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)


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
     python TPUT_and_Packet_Drops.py -p /Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/ -f n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv 
'''


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)

    # Strings used for the CPU and Memory metrics
    STRING_TIME="Time"
    STRING_TPUT = "Dallas Throughput:"
    STRING_PKTLOSS = "Dallas E2E Packet loss:"

    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)


    # Reference https://pandas.pydata.org/docs/user_guide/10min.html
    # Reading the data frame
    import pandas as pd
    from common import decide_format
    df = pd.read_csv(FILE_PATH)

    # Get only the values I need
    # Extract x and y values (two axis) from the 'df' DataFrame (which contains all the data)
    x_values = df[STRING_TIME]
    y_values_throughput = df[STRING_TPUT]
    y_values_pktloss = df[STRING_PKTLOSS]


    # Find sample at which KPI (10 ppm lost) was exceeded
    position = (y_values_pktloss > 10).idxmax()

    print("Maximum Throughput = " + str(y_values_throughput.max()) + " Max Packet loss per min=" + str(
        y_values_pktloss.max()))
    print("KPI Crossed at sample \t: " + str(position) + " with value " + str(y_values_pktloss[position]))
    print("Capturing value at "+str(position-1))
    print("Throughput was \t\t: " + str(y_values_throughput[position]))
    print("Time was \t\t:" + df[STRING_TIME][position])
    print("Previous values:")
    print("Packet loss before tipping:" + str(y_values_pktloss[position-1]) )
    print("Throughput was \t\t: " + str(y_values_throughput[position-1]))
    print("Time was \t\t:" + df[STRING_TIME][position-1])
    markers = [position-1]
    tput_b4_kpi_fail = y_values_throughput[position-1]
    tput_b4_kpi_fail = decide_format(tput_b4_kpi_fail)
    drops_b4_kpi_fail=y_values_pktloss[position-1]
    drops_after_kpi_fail=y_values_pktloss[position]

    TPUT_LABEL = "TPUT=" + str(tput_b4_kpi_fail) + "\nDROPs=" + str(drops_b4_kpi_fail) +"\nSample:"+ str(position-1) +"\nTime:"+ df[STRING_TIME][position-1] + "\nDROPs after KPI fail=" + str(drops_after_kpi_fail)
    TPUT_LEGEND = "TPUT=" + str(tput_b4_kpi_fail)
    DROPS_LEGEND = "DROPS=" + str(y_values_pktloss[position-1])

    # Trying to have two scales
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
    '''
    Graph with two scales 
    '''
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Sample')
    ax1.set_ylabel('Throughput', color=color)
    ax1.plot(x_values, y_values_throughput, color=color, markevery=markers, marker='o', label=TPUT_LABEL)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Packet Loss', color=color)  # we already handled the x-label with ax1

    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(x_values, y_values_pktloss, color=color, markevery=markers, marker='o')

    # Trying to add a line

    # Add configute Throughput legend legends
    ax1.legend()

    # Highlight a specific point in the graph (index based o 0 would be 1,2 for example with an annotation
    highlight_index = position-1
    # xytext corresponds to where to write the Text. That corresponds to the x/y scale
    ax1.annotate(TPUT_LEGEND, xy=(x_values.iloc[highlight_index], y_values_throughput.iloc[highlight_index]),
                 xytext=(x_values.iloc[highlight_index], y_values_throughput.iloc[highlight_index] - 5),
                 arrowprops=dict(facecolor='red', shrink=0.05))
    ax2.annotate(DROPS_LEGEND, xy=(x_values.iloc[highlight_index], y_values_pktloss.iloc[highlight_index]),
                 xytext=(x_values.iloc[highlight_index], y_values_pktloss.iloc[highlight_index] + 40),
                 arrowprops=dict(facecolor='blue', shrink=0.05))

    # To organize the X axis labels
    tick_interval = 10
    plt.xticks(x_values[::tick_interval], rotation=90)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()