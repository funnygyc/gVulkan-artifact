import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

def accumulate(data):
    types = len(data)
    # process data list
    periods = len(data[0])
    base = [0.0 for i in range(types)]
    processed_data = [base]
    for i in range(periods - 1):
        tmp = copy.copy(processed_data[-1])
        for j in range(len(tmp)):
            tmp[j] += data[j][i]
        processed_data.append(tmp)
    return processed_data


def transpose(data):
    processed_data = []
    for i in range(len(data[0])):
        tmp = []
        for j in range(len(data)):
            tmp.append(data[j][i])
        processed_data.append(tmp)
    return processed_data


def get_hbar_y(n, dist, h, w):
    y = []
    total_width = (n - 1) * dist + n * w
    c = h / 2
    t = c + total_width / 2 - w / 2
    for i in range(n):
        y.append(t)
        t -= (dist + w)
    return y

def plot_bar(_bar_width, _x_coordinates, _y_ticks, _data, _left, _colors, _bar_labels, _x_label, _hatches, _show_legend,
             _need_log, _height):
    types = len(_data)
    # Set ticks
    plt.ylim(0, _height)
    plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='normal', size=16)
    font_prop2 = FontProperties(family='Times New Roman', weight='bold', size=16)
    font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=20)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    # plt.yticks(_y_coordinates, _y_ticks, verticalalignment='center')

    # Set x y labels
    # plt.ylabel(_y_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 14})
    plt.xlabel(_x_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 16})

    # plot
    if _need_log:
        plt.xscale('log', base=10)
    for i in range(types):
        plt.bar(_x_coordinates, _data[i], width=_bar_width, color=_colors[i], edgecolor="black",
                 label=_bar_labels[i], left=_left[i], hatch=_hatches[i], zorder=10)

    if _show_legend:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=10, prop=font_prop3)

def plt_abar(_bar_width, _x_ticks, _data, _colors, _bar_labels, _markers, _baseline, _subtitle):
    
    x = np.arange(3)
    # plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='normal', size=22)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
    font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=15)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    
    plt.ylabel("Latency (ms)", {'family': 'Times New Roman', 'weight': 'bold', 'size': 28})
    plt.xlabel(_subtitle, {'family': 'Times New Roman', 'weight': 'bold', 'size': 28}, labelpad=12)
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    plt.xlim(-0.5, 2.5)

    total_width, bar_num = 0.7, 3
    width = total_width / bar_num
    x = x - (total_width - width) / 2
    x_ticks = []
    plt.rc('hatch', color=_colors[2], linewidth=3)

    
    for i in range(bar_num):
        x_ticks = x_ticks + list(x + i * width)
        for j in range(6):
            # if i == 0 and j == 4:
            #     plt.bar(x + i * width, transpose(_data[3*i:3*i+3])[j], width=width, bottom=accumulate(_data[3*i:3*i+3])[j], color=_colors[j], hatch="///", edgecolor=_colors[2], label="Render+Present",
            #         zorder=11)
            #     plt.bar(x + i * width, transpose(_data[3*i:3*i+3])[j], width=width, bottom=accumulate(_data[3*i:3*i+3])[j], color="none", edgecolor="black",
            #         zorder=12)
            # # else:
            if i == 0:
                plt.bar(x + i * width, transpose(_data[0:9:3])[j], width=width, bottom=accumulate(_data[0:9:3])[j], color=_colors[j], edgecolor="black", label=_bar_labels[j],
                    zorder=10)
            else:
                plt.bar(x + i * width, transpose(_data[0+i:9:3])[j], width=width, bottom=accumulate(_data[0+i:9:3])[j], color=_colors[j], edgecolor="black",
                    zorder=10)

    # colors = ["#26388f", "#6db8be", "#a7d5b9"]            
    # for j in range(3):
    #     plt.plot(x_ticks[3*j:3+3*j], transpose(_data[j*3:3+3*j])[5], color=colors[j], marker=_markers[j], linewidth=4, markersize=8, zorder=13)
            
    plt.xticks(x_ticks, ['1', '1', '1', '2\ngVulkan-BM', '2\ngVulkan-MT', '2\ngVulkan', '4', '4', '4'], fontsize=22)
    
    plt.hlines(y=_baseline, xmin=-2, xmax=4,
           lw=1.5,
           colors='black',
           linestyles='--',
           label="Baseline"
          )
    
    
def plot_latency(_bar_width, _x_ticks, _data, _colors, _bar_labels, _markers,
                         _filename):
    plt.subplot(221)
    plt_abar(_bar_width, _x_ticks, transpose(_data[0]), _colors, _bar_labels, _markers, 59.98155447, "(a) scene 1")

    plt.subplot(222)
    plt_abar(_bar_width, _x_ticks, transpose(_data[1]), _colors, _bar_labels, _markers, 97.93787159, "(b) scene 3")

    font_prop3 = FontProperties(family='Times New Roman', weight='bold', size=22)
    plt.legend(loc='upper center', bbox_to_anchor=(-0.1, 1.3), ncol=4, prop=font_prop3)

    plt.subplot(223)
    plt_abar(_bar_width, _x_ticks, transpose(_data[2]), _colors, _bar_labels, _markers, 39.21042746, "(c) scene 4")

    plt.subplot(224)
    plt_abar(_bar_width, _x_ticks, transpose(_data[3]), _colors, _bar_labels, _markers, 97.88897, "(d) scene 5")

    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.9, \
        wspace=None, hspace=0.3)
    plt.savefig(_filename, bbox_inches='tight')
    plt.show()
    print("Save latency.pdf")
    plt.clf()

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
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = [ "#B0CEBB", "#3D58B2", "#788FB3", "#9E93C3", "#AEC5EB", "#F9DEC9",]

    markers = ['^', 'D', 'o', 'v', 's']
    labels = ["L.P.", "S.P.", "R.W.", "I.C.", "S.B.", "PR.",]

    _data_raw = pd.read_csv('./240108/240108/gVulkan_scene_fps-deal.csv')

    _data_600_a1 = [
        _data_raw['lp'].tolist()[0:9],
        _data_raw['sp'].tolist()[0:9],
        _data_raw['rw'].tolist()[0:9],
        _data_raw['ic'].tolist()[0:9],
        _data_raw['sb'].tolist()[0:9],
        _data_raw['pr'].tolist()[0:9],
    ]

    _data_600_a2 = [
        _data_raw['lp'].tolist()[9:18],
        _data_raw['sp'].tolist()[9:18],
        _data_raw['rw'].tolist()[9:18],
        _data_raw['ic'].tolist()[9:18],
        _data_raw['sb'].tolist()[9:18],
        _data_raw['pr'].tolist()[9:18],
    ]

    _data_1000_a1 = [
        _data_raw['lp'].tolist()[18:27],
        _data_raw['sp'].tolist()[18:27],
        _data_raw['rw'].tolist()[18:27],
        _data_raw['ic'].tolist()[18:27],
        _data_raw['sb'].tolist()[18:27],
        _data_raw['pr'].tolist()[18:27],
    ]

    _data_1000_a2 = [
        _data_raw['lp'].tolist()[27:36],
        _data_raw['sp'].tolist()[27:36],
        _data_raw['rw'].tolist()[27:36],
        _data_raw['ic'].tolist()[27:36],
        _data_raw['sb'].tolist()[27:36],
        _data_raw['pr'].tolist()[27:36],
    ]

    _data = [
        _data_600_a1,
        _data_600_a2,
        _data_1000_a1,
        _data_1000_a2
    ]

    # print(transpose(_data)[0:3])
    # print(transpose(transpose(_data)[0::3]))
    
    x_ticks = ["gVulkan-BM", "gVulkan-MT", "gVulkan"]
    # labels = ["1", "2", "4"]
    plot_latency(0.1, x_ticks, _data, colors, labels, markers, "./img/Latency_v2.pdf")

    