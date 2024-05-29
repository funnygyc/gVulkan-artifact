import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=24)
font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=24)

def plot_line(_data, _x_ticks, _colors, _x_label, _y_label, _line_labels,
              _markers, _legend_pos):
    types = len(_data)
    x = np.arange(len(_data))
    # Set ticks
    plt.xticks(x, _x_ticks)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]

    # Set x, y labels
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 28}, labelpad=10)
    plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 28})
    # plt.ylim(0,40)
    plt.xlim(-0.5, 6.5)

    # plot
    plt.plot(x, _data, color=_colors[1], marker=_markers[3], label=_line_labels, linewidth=3, markersize=12)
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    
def plt_abar(_bar_width, _x_ticks, _data, _colors, _bar_labels, 
             _markers):
    x = np.arange(len(_data))
    # plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    plt.xticks(x, _x_ticks)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    
    plt.ylabel("FPS", {'family': 'Times New Roman', 'weight': 'bold', 'size': 28})
    plt.xlabel("Resolution", {'family': 'Times New Roman', 'weight': 'bold', 'size': 28}, labelpad=10)
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    # plt.ylim(0, 230)
    plt.xlim(-0.5, 3.5)

    total_width, bar_num = 0.5, 1
    width = total_width / bar_num
    x = x - (total_width - width) / 2
    plt.rc('hatch', color=_colors[2], linewidth=3)

    for i in range(bar_num):
        plt.bar(x + i * width, _data, width=width, color=_colors[i], edgecolor="black",
            zorder=11)


def plot_ssp(_data, _x_ticks, _x_label, _colors, _line_labels,
                    _markers, _filename, _legend_pos):
    plot_line(_data, _x_ticks, _colors, _x_label, "FPS", _line_labels,
              _markers, _legend_pos)
    
def plot_resolution(_data, _x_ticks, _x_label, _colors, _line_labels,
                    _markers, _filename, _legend_pos):
    plt_abar(0.5, _x_ticks, _data, _colors, _x_label,
              _markers)
    
if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (16.0, 12.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    # [orange gold purple green blue]
    colors = [ "#B0CEBB", "#788FB3","#E49574", "#AEC5EB", "#9E93C3", "#3D58B2"]
    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["gVulkan-BM", "gVulkan-MT", "gVulkan", "Baseline"]

    # plt.subplots_adjust(wspace=0.3,hspace=0.08)
    plt.subplot(221)

    _resolution = [77.02, 45.085, 16.671792, 7.3527]
    x_ticks = ["360P", "480P", "720P", "1080P"]
    
    plot_resolution(_resolution, x_ticks, "Resolution", colors, "Baseline", markers, "./img/spp.pdf",
                    'best')
    # plt.legend(prop=font_prop1, loc='best')
    plt.subplot(222)

    _spp = [108.75, 61.88, 32.31, 16.67, 8.41, 4.24, 2.13]
    x_ticks = ["4", "8", "16", "32", "64", "128", "256"]
    
    plot_ssp(_spp, x_ticks, "Sample (#/pixel)", colors, "Baseline", markers, "./img/spp.pdf",
                    'best')
    
    plt.savefig("./img/spp_resolution.pdf", bbox_inches='tight')
    plt.show()
    print("Save spp_resolution.pdf")
    plt.clf()

    