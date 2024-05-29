import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
from scipy.interpolate import make_interp_spline

font_prop1 = FontProperties(family='Times New Roman', weight='normal', size=22)
font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=19)

def plot_line_curve(_data, _x, _x_ticks, _colors, _y_label, _line_labels,
                    _markers):
    types = len(_data)
    # Set ticks
    plt.xticks([0, 1, 2, 3, 4, 5], ["0", "1", "2", "3", "4", "5"])
    # [0, 30815, 56716, 83523, 109302]
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]

    # Set x, y labels
    plt.xlabel("Latency (ms)", {'family': 'Times New Roman', 'weight': 'bold', 'size': 24}, labelpad=10)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    plt.ylim(0.1, 49)
    plt.xlim(0, 5)
    # plt.title(title, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})

    # plot
    # plt.plot(_x, _data[0], color=_colors[0], marker=_markers[0], label=_line_labels[0], linewidth=3, markersize=12)
    # plt.plot(_x, _data[1], color=_colors[1], marker=_markers[1], label=_line_labels[1], linewidth=3, markersize=10)
    # plt.plot(_x, _data[2], color=_colors[2], marker=_markers[2], label=_line_labels[2], linewidth=3, markersize=12)
    # plt.plot(_x, _data[3], color=_colors[3], marker=_markers[3], label=_line_labels[3], linewidth=3, markersize=12, linestyle="--")
    plt.grid(linewidth=0.4, axis="y", zorder=0)

    x_smooth = np.linspace(_x[0], _x[-1], 400)
    y1_smooth = make_interp_spline(_x, _data[3])(x_smooth)
    plt.plot(x_smooth, y1_smooth, color=_colors[3], linewidth=3)
    plt.fill_between(x_smooth,y1_smooth,0,where = y1_smooth > 0, color=_colors[3], zorder=1, label=_line_labels[3])
    
    y2_smooth = make_interp_spline(_x, _data[0])(x_smooth)
    plt.plot(x_smooth, y2_smooth, color=_colors[0], linewidth=3)
    plt.fill_between(x_smooth,y2_smooth,y1_smooth,where = y2_smooth > y1_smooth, color=_colors[0], zorder=1, label=_line_labels[0])

    y3_smooth = make_interp_spline(_x, _data[1])(x_smooth)
    plt.plot(x_smooth, y3_smooth, color=_colors[1], linewidth=3)
    plt.fill_between(x_smooth,y3_smooth,y2_smooth,where = y3_smooth > y2_smooth, color=_colors[1], zorder=1, label=_line_labels[1])

    y4_smooth = make_interp_spline(_x, _data[2])(x_smooth)
    plt.plot(x_smooth, y4_smooth, color=_colors[2], linewidth=3)
    plt.fill_between(x_smooth,y4_smooth,y3_smooth,where = y4_smooth > y3_smooth, color=_colors[2], zorder=1, label=_line_labels[2])

    plt.legend(prop=font_prop3, loc='best', ncol=2)

def plot_network(_data, _x, _x_ticks, _colors, _line_labels,
                    _markers, _legend_pos):
    plot_line_curve(_data, _x, _x_ticks, _colors, "FPS", _line_labels, _markers)
    
if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (8, 5)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'out'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_ticks = ["0", "0.1", "0.2", "0.3", "0.5", "1", "2", "3", "4", "5"]
    # [orange gold purple green blue]
    # colors = ["#F59D56", "#93CDDD", "#7F659F", "#C4D6A0", "#FFD066"]
    colors = [ "#B0CEBB", "#788FB3","#E49574", "#AEC5EB", "#9E93C3", "#3D58B2"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["gVulkan-BM", "gVulkan-MT", "gVulkan", "Baseline"]

    # print(_2d_raw['fps'].tolist())

    _x = [0, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 4, 5]

    # plt.subplot(221)
    _data = [
        [26.47487094, 26.03319383, 25.58651325, 24.70251651, 23.56258851, 20.73856625, 17.22066733, 14.38049866, 12.15371599, 10.56006142],
        [30.63268649, 30.0552044, 29.31903798, 28.75653668, 27.52863682, 25.0037853, 21.11498376, 18.01943793, 15.85835682, 14.0253309],
        [33.98371749, 34.01041777, 34.07282984, 33.96143498, 34.04135185, 34.04289829, 34.012401, 34.09232056, 29.01687444, 23.54237638],
        [25.69523307, 20.70651122, 17.81522794, 15.08161087, 12.17795681, 7.951066451, 4.702289361, 3.309725198, 2.560051767, 2.084184404]
    ]
    
    plot_network(_data, _x, x_ticks, colors, labels, markers,
                    'best')

    plt.savefig("./img/network.pdf", bbox_inches='tight')
    plt.show()
    print("Save 2ND.pdf")
    plt.clf()

    