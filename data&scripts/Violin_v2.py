import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def plot_violin(_data, _colors, _xtick_labels, _label, _x_label, _y_label, 
               _legend_pos):
    types = len(_data)
    # Set ticks
    font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=20)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    plt.xticks( [0, 1, 2, 3], _xtick_labels)
    # [0, 30815, 56716, 83523, 109302]
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]

    # Set x, y labels
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24}, labelpad=12)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    # plt.xticks(rotation=30, ha='right')
    
    # plt.title(_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 26})

    # plot
    violins = plt.violinplot(_data, [0, 1, 2, 3], showmeans=True, showmedians=False, widths=0.8)
    for violin in violins['bodies']:
        violin.set_facecolor("#788FB3")
        violin.set_alpha(1)
        violin.set_zorder(10)
    violins['cbars'].set_color("#5A7194")
    violins['cbars'].set_zorder(11)
    violins['cmeans'].set_color("#5A7194")
    violins['cmeans'].set_zorder(11)
    violins['cmins'].set_color("#5A7194")
    violins['cmins'].set_zorder(11)
    violins['cmaxes'].set_color("#5A7194")
    violins['cmaxes'].set_zorder(11)

    plt.grid(linewidth=0.4, axis="y", zorder=-1)


def plot_utilization(_data, _colors, _xtick_labels,
                    _filename, _legend_pos):
    plt.subplot(221)
    plot_violin(_data[0], _colors, _xtick_labels, "", "(a)Phase 2", "Latency(ms)",
              _legend_pos)
    plt.subplot(222)
    plot_violin(_data[1], _colors, _xtick_labels, "", "(b)Phase 3", "Latency(ms)",
              _legend_pos)
    plt.subplot(223)
    plot_violin(_data[2], _colors, _xtick_labels, "", "(c)Phase 4", "Latency(ms)",
              _legend_pos)
    plt.subplot(224)
    plot_violin(_data[3], _colors, _xtick_labels, "", "(d)Phase 5", "Latency(ms)",
              _legend_pos)
    
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, \
        wspace=None, hspace=0.3)

    plt.savefig(_filename, bbox_inches='tight')
    plt.show()
    print("Save 2ND.pdf")
    plt.clf()

if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (16.0, 12.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'out'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = ["#F59D56", "#93CDDD", "#7F659F", "#C4D6A0", "#FFD066"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels_1 = ["Phase 1", 'Phase 2', 'Phase 3', "Phase 4", "Phase 5"]
    labels_1 = ['Baseline', 'Rb.', "Th.", "Mc."]

    _2d_raw = pd.read_csv('./1.dynamic/fig3data/dynamic/2Dynamic-th+multicheck2fps.csv')['latency'].dropna(axis=0,how='any').tolist()
    _2d_th_raw = pd.read_csv('./1.dynamic/fig3data/dynamic/2Dynamic-threasholdfps.csv')['latency'].dropna(axis=0,how='any').tolist()

    _2d_na = pd.read_csv('./1.dynamic/fig3data/dynamic/2Dynamic-notanythingfps.csv')['latency'].dropna(axis=0,how='any').tolist()
    _2nd = pd.read_csv('./1.dynamic/fig3data/dynamic/2NotDynamicfps.csv')['latency'].dropna(axis=0,how='any').tolist()

    # print(pd.read_csv('./1.dynamic/2Dynamicfps.csv')['latency_sub'])

    _data = [
        _2d_raw,
        _2d_th_raw,
        _2d_na,
        _2nd,
    ]


    _data_ph = [
        [_data[0][:1089], _data[0][1089:1764], _data[0][1764:2202], _data[0][2202:2862], _data[0][2862:]],
        [_data[1][:1109], _data[1][1109:1750], _data[1][1750:2146], _data[1][2146:2829], _data[1][2829:]],
        [_data[2][:1314], _data[2][1314:1908], _data[2][1908:2289], _data[2][2289:2913], _data[2][2913:]],
        [_data[3][:1093], _data[3][1093:1521], _data[3][1521:1950], _data[3][1950:2395], _data[3][2395:]],
    ]

    _data_re = [
        [_data[3][1093:1521], _data[2][1314:1908], _data[1][1109:1750], _data[0][1089:1764]],
        [_data[3][1521:1950], _data[2][1908:2289], _data[1][1750:2146], _data[0][1764:2202]],
        [_data[3][1950:2395], _data[2][2289:2913], _data[1][2146:2829], _data[0][2202:2862]],
        [_data[3][2395:], _data[2][2913:], _data[1][2829:], _data[0][2862:] ]
    ]

    for i in range(4):
        for j in range(4):
            a = np.percentile(_data_re[i][j], 3)
            b = np.percentile(_data_re[i][j], 97)
            _data_re[i][j] = np.array(_data_re[i][j])[(_data_re[i][j]>a) & (_data_re[i][j]<b)]
    
    plot_utilization(_data_re, colors, labels_1, "./img/Violin_v2.pdf",
                    'best')

    