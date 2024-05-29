import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

def plot_line(_x_coordinates_1, _x_coordinates_2, _data, _colors, _x_label, _y_label, _line_labels,
              _markers, _legend_pos):
    types = len(_data)
    # Set ticks
    font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=22)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
    plt.xticks( [15000, 43000, 70000, 95000, 124000], ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"])
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]

    # Set x, y labels
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24}, labelpad=10)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    plt.ylim(0,70)
    plt.xlim(0, 142000)
    # plt.title(title, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})

    # plot
    plt.plot(_x_coordinates_2, _data[1], color=_colors[1], marker=_markers[2], label=_line_labels[1], linewidth=3, markersize=1)
    plt.plot(_x_coordinates_1, _data[0], color=_colors[0], marker=_markers[2], label=_line_labels[0], linewidth=3, markersize=1)
    plt.vlines(x=30815, ymin=0, ymax=70, lw=2.5, colors='#dcdcdc', linestyles='--',
                )
    plt.vlines(x=55716, ymin=0, ymax=70, lw=2.5, colors='#dcdcdc', linestyles='--',
                )
    plt.vlines(x=83523, ymin=0, ymax=70, lw=2.5, colors='#dcdcdc', linestyles='--',
                )
    plt.vlines(x=107302, ymin=0, ymax=70, lw=2.5, colors='#dcdcdc', linestyles='--',
                )
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    
    plt.legend(prop=font_prop1, loc=_legend_pos)

def plot_dynamic_4GPU(_x_coordinates_1, _x_coordinates_2, _data, _colors, _line_labels,
                    _markers, _filename, _legend_pos):
    plot_line(_x_coordinates_1, _x_coordinates_2, _data, _colors, "(b)", "FPS", _line_labels,
              _markers,
              _legend_pos)
    plt.savefig(_filename, bbox_inches="tight")
    plt.show()
    print("Save 2ND.pdf")
    plt.clf()

if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (8.0, 6.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'out'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = ["#E49574","#788FB3", "#AEC5EB","#B0CEBB",  "#9E93C3"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["Dynamic", "Not Dynamic"]

    _4d_raw = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['fps'].tolist()
    _4d_raw_time = pd.read_csv('./1.dynamic/fig3data/dynamic/4Dynamic-th+multicheck2fps.csv')['time_rel'].tolist()
    _4nd_raw = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['fps'].tolist()
    _4nd_raw_time = pd.read_csv('./1.dynamic/fig3data/dynamic/4NotDynamicfps.csv')['time_rel'].tolist()
    # print(_2d_raw['fps'].tolist())

    _4_data = [
        _4d_raw,
        _4nd_raw
    ]
    
    plot_dynamic_4GPU(_4d_raw_time, _4nd_raw_time, _4_data, colors, labels, markers, "./img/4NonDynamic.pdf",
                    'best')

    