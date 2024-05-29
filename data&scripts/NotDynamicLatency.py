import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

def plot_bar(_bar_width, _y_coordinates, _y_ticks, _data, _left, _colors, _bar_labels, _x_label, _hatches, _show_legend,
             _need_log, _height):
    types = len(_data)
    # Set ticks
    plt.ylim(0, _height)
    plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='normal', size=10)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=10)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    plt.yticks(_y_coordinates, _y_ticks, rotation=-60, verticalalignment='center')

    # Set x y labels
    # plt.ylabel(y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})

    # plot
    if _need_log:
        plt.xscale('log', base=10)
    for i in range(types):
        plt.barh(_y_coordinates, _data[i], height=_bar_width, color=_colors[i], edgecolor="black",
                 label=_bar_labels[i], left=_left[i], hatch=_hatches[i], zorder=10)

    if _show_legend:
        plt.legend(loc='upper center', bbox_to_anchor=(1, 1.15), ncol=10, prop=font_prop1)


def plot_wbar(_bar_width, _x_ticks, _data, _colors, _bar_labels, _y_label, _x_label, size):
    x = np.arange(size)
    # plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=22)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
    font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=22)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    plt.xticks(x, _x_ticks, fontsize=20)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24}, labelpad=10)
    plt.grid(linewidth=0.4, axis="y", zorder=0)

    total_width, bar_num = 0.8, len(_bar_labels)
    width = total_width / bar_num
    x = x - (total_width - width) / 2

    for i in range(bar_num):
        length = len(_data[i])
        # a = np.percentile(_data[i], 0.5)
        # b = np.percentile(_data[i], 99.5)
        # _data[i] = np.array(_data[i])[(_data[i]>a) & (_data[i]<b)]

        if i <= 1:
            data_a = [
                np.mean(_data[i][0]),
                np.mean(_data[i][1]),
                np.mean(_data[i][2]),
                np.mean(_data[i][3]),
                np.mean(_data[i][4]),
            ]
            error = [
                np.std(_data[i][0]),
                np.std(_data[i][1]),
                np.std(_data[i][2]),
                np.std(_data[i][3]),
                np.std(_data[i][4]),
            ]
        else:
            data_a = [
                np.mean(_data[i][0]),
                np.mean(_data[i][1]),
                np.mean(_data[i][2]),
                np.mean(_data[i][3]),
                np.mean(_data[i][4]),
            ]
            error = [
                np.std(_data[i][0]),
                np.std(_data[i][1]),
                np.std(_data[i][2]),
                np.std(_data[i][3]),
                np.std(_data[i][4]),
            ]

        # print(_data[i])
        plt.bar(x + i * width, data_a, width=width, color=_colors[i], edgecolor="black", label=_bar_labels[i],
            zorder=10)
        plt.errorbar(x + i * width, data_a, yerr=error, capsize=3, elinewidth=1, fmt=' k,', zorder=11)
    plt.legend(loc='upper center', bbox_to_anchor=(1.3, 0.425), ncol=1, prop=font_prop3)


def plot_dynamic_latency(_bar_width, _x_ticks, _data, _colors, _bar_labels
                   , _filename):
    plot_wbar(_bar_width, _x_ticks, _data, _colors, _bar_labels, "Latency(ms)", "(c)", 5)

    plt.savefig(_filename, bbox_inches='tight')
    plt.show()
    print("Save latency.pdf")
    plt.clf()

if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (8.0, 6.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = ["#788FB3", "#AEC5EB", "#F9DEC9", "#B0CEBB", "#FFB1AE"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["2GPU Dynamic", "2GPU NotDynamic", "4GPU Dynamic", "4GPU NotDynamic"]

    _2d_raw_G1 = pd.read_csv('./1.dynamic/fig3data/dynamic/2Dynamic-th+multicheck2fps.csv')['GPU1'].dropna(axis=0,how='any').tolist()
    _2nd_raw_G1 = pd.read_csv('./1.dynamic/fig3data/dynamic/2Notdynamicfps.csv')['GPU1'].dropna(axis=0,how='any').tolist()
    
    _2d_raw_G2 = pd.read_csv('./1.dynamic/fig3data/dynamic/2Dynamic-th+multicheck2fps.csv')['GPU2'].dropna(axis=0,how='any').tolist()
    _2nd_raw_G2 = pd.read_csv('./1.dynamic/fig3data/dynamic/2Notdynamicfps.csv')['GPU2'].dropna(axis=0,how='any').tolist()

    _4d_raw_G1 = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['GPU1'].dropna(axis=0,how='any').tolist()
    _4nd_raw_G1 = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['GPU1'].dropna(axis=0,how='any').tolist()

    _4d_raw_G2 = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['GPU2'].dropna(axis=0,how='any').tolist()
    _4nd_raw_G2 = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['GPU2'].dropna(axis=0,how='any').tolist()

    _4d_raw_G3 = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['GPU3'].dropna(axis=0,how='any').tolist()
    _4nd_raw_G3 = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['GPU3'].dropna(axis=0,how='any').tolist()

    _4d_raw_G4 = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['GPU4'].dropna(axis=0,how='any').tolist()
    _4nd_raw_G4 = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['GPU4'].dropna(axis=0,how='any').tolist()

    # print(pd.read_csv('./1.dynamic/2Dynamicfps.csv')['latency_sub'])

    _data = [
        [rv for r in zip(_2d_raw_G1,_2d_raw_G2) for rv in r],
        [rv for r in zip(_2nd_raw_G1,_2nd_raw_G2) for rv in r],
        [rv for r in zip(_4d_raw_G1,_4d_raw_G2,_4d_raw_G3,_4d_raw_G4) for rv in r],
        [rv for r in zip(_4nd_raw_G1,_4nd_raw_G2,_4nd_raw_G3,_4nd_raw_G4) for rv in r],
    ]

    for i in range(4):
        a = np.percentile(_data[i], 0.1)
        b = np.percentile(_data[i], 99.9)
        _data[i] = np.array(_data[i])[(_data[i]>a) & (_data[i]<b)]

    _data_ph = [
        [_data[0][:1090*2], _data[0][1090*2:1764*2], _data[0][1764*2:2190*2], _data[0][2190*2:2848*2], _data[0][2848*2:]],
        [_data[1][:1094*2], _data[1][1094*2:1521*2], _data[1][1521*2:1950*2], _data[1][1950*2:2395*2], _data[1][2395*2:]],
        [_data[2][:1822*4], _data[2][1822*4:3276*4], _data[2][3276*4:4098*4], _data[2][4098*4:5047*4], _data[2][5047*4:]],
        [_data[3][:1843*4], _data[3][1843*4:2707*4], _data[3][2707*4:3488*4], _data[3][3488*4:4270*4], _data[3][4270*4:]],
    ]
    
    x_ticks = ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]
    plot_dynamic_latency(0.2, x_ticks, _data_ph, colors, labels, "./img/NotDynamicLatency.pdf"
                    )

    