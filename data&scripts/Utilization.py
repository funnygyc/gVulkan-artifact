import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from matplotlib.font_manager import FontProperties
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as cs

def plot_heatmap(_data, _colors, _xtick_labels, _ytick_labels, _label, _cb_range, 
               _legend_pos):
    types = len(_data)
    # Set ticks
    font_prop1 = FontProperties(family='Times New Roman', weight='normal', size=20)
    font_prop2 = FontProperties(family='Times New Roman', weight='normal', size=20)
    font_prop3 = FontProperties(family='Times New Roman', weight='bold', size=28)
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
    plt.rc('font', family='Times New Roman')
    plt.rcParams["font.weight"] = "normal"
    plt.rcParams["font.size"] = "24"

    # Set x, y labels
    plt.xticks([0, 1, 2, 3], _xtick_labels, family='Times New Roman', weight='bold', size=24)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8], _ytick_labels, family='Times New Roman', weight='normal', size=18)
    # plt.xlabel(_label, {'family': 'Times New Roman', 'weight': 'bold', 'size': 26})

    cb = ["#ddf2ff", "#9ac2e3", "#6091c8", "#2f60aa", "#013087"]
    cb = cs.LinearSegmentedColormap.from_list("", cb)
    # plot
    # R1 = np.log2(R1)
    sns_plot1 = sns.heatmap(_data, xticklabels=_xtick_labels, yticklabels=_ytick_labels, vmax=_cb_range[1], vmin=_cb_range[0],
                             cmap=cb, square=False, annot=False, fmt='.2f', lw=0)
    
    for xitem in sns_plot1.get_xticklabels():
        xitem.set_rotation(0)
    for yitem in sns_plot1.get_yticklabels():
        yitem.set_rotation(0)
    plt.xlabel(_label, fontproperties=font_prop3, labelpad=7)
    # plt.ylabel('thread ID', fontproperties=sub_font)

def plot_utilization(_data, _colors, _xtick_labels,
                    _ytick_labels, _filename, _legend_pos):
    plt.subplot(221)
    plot_heatmap(_data[0], _colors, _xtick_labels, _ytick_labels, "(a) CPU", [0, 10],
              _legend_pos)
    plt.subplot(222)
    plot_heatmap(_data[1], _colors, _xtick_labels, _ytick_labels, "(b) Memory", [0, 1],
              _legend_pos)
    plt.subplot(223)
    plot_heatmap(_data[2], _colors, _xtick_labels, _ytick_labels, "(c) GPU", [0, 100],
              _legend_pos)
    plt.subplot(224)
    plot_heatmap(_data[3], _colors, _xtick_labels, _ytick_labels, "(d) GPU Memory", [0, 5],
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
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    # draw recv side figure
    x_coordinates = np.array(range(1, 12, 1))
    x_ticks = ["4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]
    # [orange gold purple green blue]
    colors = ["#F59D56", "#93CDDD", "#7F659F", "#C4D6A0", "#FFD066"]
    markers = ['^', 'D', 'o', 'v', 's']
    # labels_2 = ["gVulkan-BM", "gVulkan-MT", "gVulkan", "gVulkan-BM", "gVulkan-MT", "gVulkan", "gVulkan-BM", "gVulkan-MT", "gVulkan"]
    labels_2 = ["BM_1", "MT_1", "gV_1", "BM_2", "MT_2", "gV_2", "BM_4", "MT_4", "gV_4"]
    labels_1 = ["scene 1", 'scene 3', 'scene 4', 'scene 5']

    # _data = [
    #   CPU[
    #       [bm1, bm2, bm4]
    #       [mt1, mt2, mt4]
    #       [gv1, gv2, gv4]
    #   ],
    #   GPU[
    #   
    #   ]
    # ]

    _data = [
        [
            np.array([1.805, 1.77, 2.71, 1.745]),
            np.array([1.98, 1.26, 2.425, 1.025]),
            np.array([2.48, 2.095, 2.66, 1.93]),
            [2.855, 2.155, 3.155, 1.985],
            [2.495, 1.79, 2.815, 1.685],
            [3.08, 2.355, 4.005, 2.33],
            [2.775, 2.1, 2.87, 2.295],
            [3.06, 2.365, 5.295, 2.31],
            [2.91, 2.915, 2.9066, 3.025]
        ],
        [
            np.array([1.0915, 1.157, 1.1205, 1.1495])-0.9,
            np.array([1.113, 1.15, 1.0905, 1.13])-0.9, 
            np.array([1.127, 1.155, 1.1, 1.1305])-0.9, 
            np.array([1.1755, 1.1805, 1.12, 1.15])-0.9,
            np.array([1.143, 1.1755, 1.12, 1.1415])-0.9,
            np.array([1.16, 1.19, 1.167, 1.18])-0.9, 
            np.array([1.2295, 1.25, 1.19, 1.22])-0.9, 
            np.array([1.22, 1.25, 1.1985, 1.2205])-0.9, 
            np.array([1.2595, 1.27, 1.1173, 1.26])-0.9
            
        ],
        [
            [21.3375, 22.625, 19.475, 22.6], 
            [23.5875, 24.05, 22.925, 24.1], 
            [25, 25, 25, 25], 
            [31.25, 34.275, 32.4625, 38.2875], 
            [36.9625, 38.425, 40.5875, 43.15],
            [49.3875, 49.4875, 49.9375, 48.4625],
            [48.1625, 51.25, 44.2, 58.125], 
            [59.0375, 59.4875, 62.0125, 68.9125], 
            [96.275, 89.4375, 64.39286, 89.3875]
        ],
        [
            np.array([0.009644, 0.015442, 0.008057, 0.008667])*25,
            np.array([0.009644, 0.015442, 0.008057, 0.008667])*25,
            np.array([0.009644, 0.015442, 0.008057, 0.008667])*25,
            np.array([0.018494, 0.032227, 0.01532, 0.018616])*25,
            np.array([0.018494, 0.032227, 0.01532, 0.018616])*25,
            np.array([0.018494, 0.032227, 0.01532, 0.018616])*25,
            np.array([0.036194, 0.065796, 0.029846, 0.038513])*25,
            np.array([0.036194, 0.065796, 0.029846, 0.038513])*25,
            np.array([0.036194, 0.065796, 0.029846, 0.038513])*25
        ],
    ]
    
    plot_utilization(_data, colors, labels_1, labels_2, "./img/Utilization.pdf",
                    'best')

    