# main.py
from common import decide_format, dual_axis_plot
number=10.333434343

print(decide_format(number))

DIR = "/Users/vcarlos/PycharmProjects/parseesxilogs/sample_stats/n294_2dp_16vcpu_ht_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_120/"
FILE = "n294_2dp_16vcpu_ht_6lcore_pnicrss0n_netqrss_5gudp_cpu_ctx3_1207.csv"
FULL_PATH = DIR + FILE
HOSTNAME = "n294-esxi-ht-04"
