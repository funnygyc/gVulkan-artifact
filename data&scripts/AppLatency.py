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

def plt_abar(_bar_width, _x_ticks, _data, _colors, _bar_labels, 
             _markers):
    x = np.arange(len(_data[0]))
    # plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=20)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=20)
    font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=20)
    plt.xticks(x, _x_ticks)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    
    plt.ylabel("Latency(ms)", {'family': 'Times New Roman', 'weight': 'bold', 'size': 20})
    # plt.xlabel("", {'family': 'Times New Roman', 'weight': 'bold', 'size': 20})
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    # plt.xlim(-0.5, 2.5)

    total_width, bar_num = 0.7, len(_bar_labels)
    width = total_width / bar_num
    x = x - (total_width - width) / 2
    plt.rc('hatch', color=_colors[2], linewidth=3)

    for i in range(bar_num):
        plt.bar(x + i * width, _data[i], width=width, color=_colors[i], label=_bar_labels[i], edgecolor="black",
            zorder=11)
    
    plt.legend(loc='best', prop=font_prop3)
    
def plot_latency(_bar_width, _x_ticks, _data, _colors, _bar_labels, _markers,
                         _filename):
    plt_abar(_bar_width, _x_ticks, _data, _colors, _bar_labels, _markers)

    plt.savefig(_filename, bbox_inches='tight')
    plt.show()
    print("Save latency.pdf")
    plt.clf()

if __name__ == "__main__":
    plt.rc('font', family='Times New Roman', weight='normal', size=15)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (10.0, 5.0)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # draw recv side figure
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = ["#788FB3","#B0CEBB", "#AEC5EB",  "#9E93C3","#F9DEC9"]
    markers = ['^', 'D', 'o', 'v', 's']

    _data = [
        [0.897202187, 1.777, 1.799, 1.806, 1.777, 1.712, 1.851, 2.119, 1.838],
        [6.032755375, 1.991, 4.185, 2.716, 2.06, 3.581, 3.1, 2.255, 1.922]
    ]
    
    x_ticks = ["Triangle", "Reflections", "Motionblur", "Scissor", "Gltf", "Anyhit", "Advance", "Animation", "Compilation"]
    x_ticks_abb = ['Tr.', "Rf.", "Mb.", "Sc.", "Gl.", "Ah.", "Ad.", "An.", "Cp."]
    labels = ["Rasterization", "Ray Tracing"]
    plot_latency(0.1, x_ticks_abb, _data, colors, labels, markers, "./img/applatency.pdf")

    