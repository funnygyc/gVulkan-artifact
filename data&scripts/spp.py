import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=22)
font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)

def plot_line(_data, _x_ticks, _colors, _x_label, _y_label, _line_labels,
              _markers, _legend_pos):
    types = len(_data)
    x = np.arange(len(_data[0]))
    # Set ticks
    plt.xticks(x, _x_ticks)
    # [0, 30815, 56716, 83523, 109302]
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]

    # Set x, y labels
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24}, labelpad=10)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    # plt.ylim(0,40)
    plt.xlim(-0.5, 6.5)
    # plt.title(title, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})

    # plot
    plt.plot(x, _data[0], color=_colors[0], marker=_markers[0], label=_line_labels[0], linewidth=3, markersize=12)
    plt.plot(x, _data[1], color=_colors[1], marker=_markers[1], label=_line_labels[1], linewidth=3, markersize=10)
    plt.plot(x, _data[2], color=_colors[2], marker=_markers[2], label=_line_labels[2], linewidth=3, markersize=12)
    plt.plot(x, _data[3], color=_colors[3], marker=_markers[3], label=_line_labels[3], linewidth=3, markersize=12, linestyle="--")
    plt.grid(linewidth=0.4, axis="y", zorder=0)

def plot_ssp(_data, _x_ticks, _x_label, _colors, _line_labels,
                    _markers, _filename, _legend_pos):
    plot_line(_data, _x_ticks, _colors, _x_label, "FPS", _line_labels,
              _markers,
              _legend_pos)
    
if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (24.0, 5.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'out'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_ticks = ["4", "8", "16", "32", "64", "128", "256"]
    # [orange gold purple green blue]
    # colors = ["#F59D56", "#93CDDD", "#7F659F", "#C4D6A0", "#FFD066"]
    colors = [ "#B0CEBB", "#788FB3","#E49574", "#AEC5EB", "#9E93C3", "#3D58B2"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["gVulkan-BM", "gVulkan-MT", "gVulkan", "Baseline"]

    plt.subplots_adjust(wspace=0.3,hspace=0.08)
    plt.subplot(1, 3, 1)
    # print(_2d_raw['fps'].tolist())

    _1_gpu = [
        [59.03574943, 42.89175855, 26.99818194, 15.01544564, 8.234842407, 4.292226472, 2.171303912],
        [87.55637171, 54.46880868, 30.71250556, 16.72814788, 8.386158991, 4.263670056, 2.153412762],
        [128.6371989, 67.52796333, 35.02881899, 17.71333274, 8.90121133, 4.466644883, 2.220500495],
        [108.75, 61.88, 32.31, 16.67, 8.41, 4.24, 2.13]
    ]
    
    plot_ssp(_1_gpu, x_ticks, "Sample (#/pixel)\n\n(a) 1 GPU", colors, labels, markers, "./img/spp.pdf",
                    'best')
    plt.legend(prop=font_prop1, loc='best')
    plt.subplot(1, 3, 2)
    # print(_2d_raw['fps'].tolist())

    _2_gpu = [
        [70.59348413, 54.45910551, 37.92992303, 22.46836566, 12.8885063, 6.845462282, 3.532476569],
        [114.1903454, 79.79514989, 48.97170573, 25.98424194, 13.89424503, 7.085384496, 3.596983239],
        [242.3348152, 128.8520315, 66.47693657, 33.80221894, 17.03280446, 8.546309908, 4.262684806],
        [108.75, 61.88, 32.31, 16.67, 8.41, 4.24, 2.13]
    ]
    
    plot_ssp(_2_gpu, x_ticks, "Sample (#/pixel)\n\n(b) 2 GPU", colors, labels, markers, "./img/spp.pdf",
                    'best')
    
    plt.subplot(1, 3, 3)
    # print(_2d_raw['fps'].tolist())

    _4_gpu = [
        [84.74865151, 65.45654485, 50.0180454, 32.99262582, 19.52889111, 10.70209259, 5.623773385],
        [135.2901704, 104.5095888, 66.88659972, 40.22754667, 21.97479418, 11.40726136, 5.810157256],
        [222.9641699, 237.6105879, 128.133213, 65.07077929, 32.82922957, 16.51310912, 8.223593964],
        [108.75, 61.88, 32.31, 16.67, 8.41, 4.24, 2.13]
    ]
    
    plot_ssp(_4_gpu, x_ticks, "Sample (#/pixel)\n\n(c) 4 GPU", colors, labels, markers, "./img/spp.pdf",
                    'best')

    plt.savefig("./img/spp.pdf", bbox_inches='tight')
    plt.show()
    print("Save 2ND.pdf")
    plt.clf()

    