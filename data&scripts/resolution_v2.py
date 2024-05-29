import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

def autolabel(rects, array, heights):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for i in range(len(rects)):
        rect = rects[i]
        height = heights[i]
        s = "{:.1f}%".format(array[i])
        l = len(s)
        if l == 5:
            offset = -0.01
        else:
            offset = 0
        plt.text(s=s,
                x=rect.get_x()+0.12, y=height - offset,
                va='bottom', ha="center", family='Times New Roman', weight='normal', size=12, zorder=100)

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
    x = np.arange(9)
    # plt.grid(b=True, axis='x', linewidth=0.7, linestyle='--', zorder=0)
    font_prop1 = FontProperties(family='Times New Roman', weight='bold', size=22)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=22)
    font_prop3 = FontProperties(family='Times New Roman', weight='normal', size=20)
    xtick_labels = plt.gca().get_xticklabels()
    ytick_labels = plt.gca().get_yticklabels()
    [xtick_label.set_fontproperties(font_prop1) for xtick_label in xtick_labels]
    [ytick_label.set_fontproperties(font_prop2) for ytick_label in ytick_labels]
    
    plt.ylabel("Latency (ms)", {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    plt.xlabel("", {'family': 'Times New Roman', 'weight': 'bold', 'size': 24})
    plt.grid(linewidth=0.4, axis="y", zorder=0)
    plt.ylim(0, 163)
    plt.xlim(-0.5, 8.5)

    total_width, bar_num = 0.7, 4
    width = total_width / bar_num
    x = x - (total_width - width) / 2
    plt.rc('hatch', color='white', linewidth=1)
    
    _data = transpose(_data)
    x_loc = []
    hatch = ['||', 'x', 'o', '//', ]
    re_label = ['360P', '480P', '720P', '1080P']
    handles = []

    for i in range(bar_num):
        x_loc = x_loc + list(x + i * width)
        for j in range(6):
            # print(x + i * width)
            # print(transpose(_data[9*i:9*i+9:3]))
            print("\n")
            if i == 0:
                plt.bar(x[0:3] + i * width, transpose(_data[9*i:9*i+9:3])[j], width=width, bottom=accumulate(_data[9*i:9*i+9:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
                plt.bar(x[3:6] + i * width, transpose(_data[9*i+1:9*i+10:3])[j], width=width, bottom=accumulate(_data[9*i+1:9*i+10:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
                plt.bar(x[6:9] + i * width, transpose(_data[9*i+2:9*i+11:3])[j], width=width, bottom=accumulate(_data[9*i+2:9*i+11:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
                handle = plt.bar(-1, 1, color=_colors[j], edgecolor="black", label=_bar_labels[j])
                handles.append(handle)
            else:
                plt.bar(x[0:3] + i * width, transpose(_data[9*i:9*i+9:3])[j], width=width, bottom=accumulate(_data[9*i:9*i+9:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
                plt.bar(x[3:6] + i * width, transpose(_data[9*i+1:9*i+10:3])[j], width=width, bottom=accumulate(_data[9*i+1:9*i+10:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
                plt.bar(x[6:9] + i * width, transpose(_data[9*i+2:9*i+11:3])[j], width=width, bottom=accumulate(_data[9*i+2:9*i+11:3])[j], color=_colors[j], hatch=hatch[i], edgecolor="black",
                    zorder=10)
        
    for i in range(bar_num):
        handle = plt.bar(-1, 1, color='white', hatch=hatch[i], edgecolor="black", label=re_label[i])
        handles.append(handle)
        
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], _x_ticks, fontsize=22)

    plt.vlines(x=2.5, ymin=-2, ymax=250,
           lw=1.5,
           colors='black',
           linestyles='-.',
           alpha=0.3
          )
    
    plt.vlines(x=5.5, ymin=-2, ymax=250,
           lw=1.5,
           colors='black',
           linestyles='-.',
           alpha=0.3
          )
    
    plt.hlines(y=12.98364061, xmin=-2, xmax=250,
           lw=3,
           colors="#E49574",
           linestyles='--',
           alpha=0.6
          )
    
    plt.hlines(y=22.18032605, xmin=-2, xmax=250,
           lw=3,
           colors="#E49574",
           linestyles='--',
           alpha=0.6
          )
    
    plt.hlines(y=59.98155447, xmin=-2, xmax=250,
           lw=3,
           colors="#E49574",
           linestyles='--',
           alpha=0.6
          )
    
    handle = plt.hlines(y=136.0044609, xmin=-2, xmax=250,
           lw=3,
           colors="#E49574",
           linestyles='--',
           label="Baseline",
           alpha=0.6
          )

    handles.append(handle)
    
    # plt.text(s="360P",
    #     x=x_loc[0], y=18,
    #     va='bottom', ha="center", family='Times New Roman', weight='normal', rotation=90, size=20, zorder=100)
    # plt.text(s="480P",
    #     x=x_loc[9], y=28,
    #     va='bottom', ha="center", family='Times New Roman', weight='normal', rotation=90, size=20, zorder=100)
    # plt.text(s="720P",
    #     x=x_loc[18], y=70,
    #     va='bottom', ha="center", family='Times New Roman', weight='normal', rotation=90, size=20, zorder=100)
    # plt.text(s="1080P",
    #     x=x_loc[27], y=155,
    #     va='bottom', ha="center", family='Times New Roman', weight='normal', rotation=90, size=20, zorder=100)
    
    plt.text(s="360P",
        x=8.52, y=11.5,
        va='bottom', ha="left", family='Times New Roman', weight='normal', size=20, zorder=100)
    plt.text(s="480P",
        x=8.52, y=22,
        va='bottom', ha="left", family='Times New Roman', weight='normal', size=20, zorder=100)
    plt.text(s="720P",
        x=8.52, y=59,
        va='bottom', ha="left", family='Times New Roman', weight='normal', size=20, zorder=100)
    plt.text(s="1080P",
        x=8.52, y=136,
        va='bottom', ha="left", family='Times New Roman', weight='normal', size=20, zorder=100)
    
    plt.legend(loc='best', handles=handles, prop=font_prop3, ncol=2)
    
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
    plt.rcParams['figure.figsize'] = (25.0, 6.0)
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

    _data_raw = pd.read_csv('./240108/240108/gVulkan_resolution_fps-deal.csv')

    _data = [
        _data_raw['lp'].tolist()[0:36],
        _data_raw['sp'].tolist()[0:36],
        _data_raw['rw'].tolist()[0:36],
        _data_raw['ic'].tolist()[0:36],
        _data_raw['sb'].tolist()[0:36],
        _data_raw['pr'].tolist()[0:36]
    ]
    
    labels = ["L.P.", "S.P.", "R.W.", "I.C.", "S.B.", "PR.",]
    x_ticks_abb = ['gVulkan-BM', "gVulkan-MT\n\n1 GPU", "gVulkan", 'gVulkan-BM', "gVulkan-MT\n\n2 GPU", "gVulkan", 'gVulkan-BM', "gVulkan-MT\n\n4 GPU", "gVulkan"]
    plot_latency(0.1, x_ticks_abb, _data, colors, labels, markers, "./img/resolution.pdf")

    