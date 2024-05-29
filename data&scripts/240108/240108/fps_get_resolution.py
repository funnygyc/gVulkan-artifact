import os
import pandas as pd
import re
import numpy as np

def extract_server_latency(log_file):
    time_dict = {'cycle_end_old': None,'cycle_end_new': None}
    time_diffs_present = []
    times = 0
    with open(log_file, 'r') as f:
        for line in f:
            cycle_end_match = re.match(r'\[(\d+\.\d+)\]\s+CYCLE End (\d+)', line)
            if cycle_end_match:
                time_dict['cycle_end_old'] = time_dict['cycle_end_new']
                time_dict['cycle_end_new'] = float(cycle_end_match.group(1))
            if None not in time_dict.values():
                # print(time_dict)
                if cycle_end_match:
                    present = time_dict['cycle_end_new'] - time_dict['cycle_end_old']
                    time_diffs_present.append(present)
                    times += 1
    print(times)
    mean_time_diff_present = np.mean(time_diffs_present[10:100])
    return mean_time_diff_present

def extract_ben_server_latency(log_file):
    time_dict = {'cycle_end_old': None,'cycle_end_new': None, 'API_1000': None, 'API_1002': None, 'wait_render': None, 'copy_device': None, 'sendback_start': None, 'sendback_end': None, 'API_22': None}
    time_diffs_totallatency = []
    time_diffs_layerpreprocess = []
    time_diffs_render = []
    time_diffs_copy = []
    time_diffs_sendback = []
    time_diffs_present = []

    times = 0
    with open(log_file, 'r') as f:
        for line in f:
            API_1000_match = re.match(r'\[(\d+\.\d+)\]\s+API 1000 run', line)
            API_1002_match = re.match(r'\[(\d+\.\d+)\]\s+API 1002 run', line)
            parallel_render_match = re.match(r'\[(\d+\.\d+)\]\s+Parrallel Render (\d+)', line)
            wait_render_match = re.match(r'\[(\d+\.\d+)\]\s+Wait Synchronization after Render (\d+)', line)
            copy_device_match = re.match(r'\[(\d+\.\d+)\]\s+Copy Device to Device (\d+)', line)
            sendback_start_match = re.match(r'\[(\d+\.\d+)\]\s+SENDBACK START 0', line)
            sendback_end_match = re.match(r'\[(\d+\.\d+)\]\s+SENDBACK END 0', line)
            primary_device_copy_match = re.match(r'\[(\d+\.\d+)\]\s+Primary Device Copy the Image in Swapchin (\d+)', line)
            API_22_match = re.match(r'\[(\d+\.\d+)\]\s+API 22 run', line)
            cycle_end_match = re.match(r'\[(\d+\.\d+)\]\s+CYCLE End (\d+)', line)
            if cycle_end_match:
                time_dict['cycle_end_old'] = time_dict['cycle_end_new']
                time_dict['cycle_end_new'] = float(cycle_end_match.group(1))
            elif API_1000_match:
                time_dict['API_1000'] = float(API_1000_match.group(1))
            elif API_1002_match:
                time_dict['API_1002'] = float(API_1002_match.group(1))
            elif wait_render_match:
                time_dict['wait_render'] = float(wait_render_match.group(1))
            elif copy_device_match:
                time_dict['copy_device'] = float(copy_device_match.group(1))
            elif sendback_start_match:
                time_dict['sendback_start'] = float(sendback_start_match.group(1))
            elif sendback_end_match:
                time_dict['sendback_end'] = float(sendback_end_match.group(1))
            elif API_22_match:
                time_dict['API_22'] = float(API_22_match.group(1))
            if None not in time_dict.values():
                # print(time_dict)
                if cycle_end_match:
                    totallatency = time_dict['cycle_end_new'] - time_dict['cycle_end_old']
                    time_diffs_totallatency.append(totallatency)
                    present = time_dict['cycle_end_new'] - time_dict['API_22']
                    time_diffs_present.append(present)
                    times += 1
                elif API_1002_match:
                    layer_preprocess = time_dict['API_1002'] - time_dict['API_1000']
                    time_diffs_layerpreprocess.append(layer_preprocess)
                elif copy_device_match:
                    render_wait = time_dict['copy_device'] - time_dict['wait_render']
                    time_diffs_render.append(render_wait)
                elif sendback_start_match:
                    copy = time_dict['sendback_start'] - time_dict['copy_device']
                    time_diffs_copy.append(copy)
                elif sendback_end_match:
                    sendback = time_dict['sendback_end'] - time_dict['sendback_start']
                    time_diffs_sendback.append(sendback)
                
    print(times)
    mean_time_diff_totallatency = np.mean(time_diffs_totallatency[10:100])
    mean_time_diff_layer_preprocess = np.mean(time_diffs_layerpreprocess[20:200])*2
    mean_time_diff_render_wait = np.mean(time_diffs_render[10:100])
    mean_time_diff_image_copy = np.mean(time_diffs_copy[10:100])
    mean_time_diff_sendback = np.mean(time_diffs_sendback[10:100])
    mean_time_diff_present = np.mean(time_diffs_present[10:100])
    return mean_time_diff_totallatency,mean_time_diff_layer_preprocess,mean_time_diff_render_wait,mean_time_diff_image_copy,mean_time_diff_sendback,mean_time_diff_present

def extract_gvulkan_server_latency(log_file):
    time_dict = {'cycle_end_old': None,'cycle_end_new': None, 'API_1000': None, 'API_1002': None, 'API_3': None, 'copy_device': None, 'sendback_start': None, 'sendback_end': None, 'parallel_render': None}
    time_diffs_totallatency = []
    time_diffs_layerpreprocess = []
    time_diffs_render = []
    time_diffs_copy = []
    time_diffs_sendback = []
    time_diffs_present = []

    times = 0
    with open(log_file, 'r') as f:
        for line in f:
            API_1000_match = re.match(r'\[(\d+\.\d+)\]\s+API 1000 run', line)
            API_1002_match = re.match(r'\[(\d+\.\d+)\]\s+API 1002 run', line)

            API_3_match = re.match(r'\[(\d+\.\d+)\]\s+API 3 run', line)
            wait_render_match = re.match(r'\[(\d+\.\d+)\]\s+Wait Synchronization after Render (\d+)', line)
            copy_device_match = re.match(r'\[(\d+\.\d+)\]\s+Copy Device to Device (\d+)', line)
            sendback_start_match = re.match(r'\[(\d+\.\d+)\]\s+SENDBACK START 0', line)
            sendback_end_match = re.match(r'\[(\d+\.\d+)\]\s+SENDBACK END 0', line)
            primary_device_copy_match = re.match(r'\[(\d+\.\d+)\]\s+Primary Device Copy the Image in Swapchin (\d+)', line)
            API_22_match = re.match(r'\[(\d+\.\d+)\]\s+API 22 run', line)
            parallel_render_match = re.match(r'\[(\d+\.\d+)\]\s+Parrallel Render (\d+)', line)
            cycle_end_match = re.match(r'\[(\d+\.\d+)\]\s+CYCLE End (\d+)', line)
            if cycle_end_match:
                time_dict['cycle_end_old'] = time_dict['cycle_end_new']
                time_dict['cycle_end_new'] = float(cycle_end_match.group(1))
            elif API_1000_match:
                time_dict['API_1000'] = float(API_1000_match.group(1))
            elif API_1002_match:
                time_dict['API_1002'] = float(API_1002_match.group(1))
            elif API_3_match:
                time_dict['API_3'] = float(API_3_match.group(1))
            elif copy_device_match:
                time_dict['copy_device'] = float(copy_device_match.group(1))
            elif sendback_start_match:
                time_dict['sendback_start'] = float(sendback_start_match.group(1))
            elif sendback_end_match:
                time_dict['sendback_end'] = float(sendback_end_match.group(1))
            elif parallel_render_match:
                time_dict['parallel_render'] = float(parallel_render_match.group(1))
            if None not in time_dict.values():
                # print(time_dict)
                if cycle_end_match:
                    totallatency = time_dict['cycle_end_new'] - time_dict['cycle_end_old']
                    time_diffs_totallatency.append(totallatency)
                    present = time_dict['cycle_end_new'] - time_dict['parallel_render']
                    time_diffs_present.append(present)
                    times += 1
                elif API_1002_match:
                    layer_preprocess = time_dict['API_1002'] - time_dict['API_1000']
                    time_diffs_layerpreprocess.append(layer_preprocess)
                elif copy_device_match:
                    render_wait = time_dict['copy_device'] - time_dict['API_3']
                    time_diffs_render.append(render_wait)
                elif sendback_start_match:
                    copy = time_dict['sendback_start'] - time_dict['copy_device']
                    time_diffs_copy.append(copy)
                elif sendback_end_match:
                    sendback = time_dict['sendback_end'] - time_dict['sendback_start']
                    time_diffs_sendback.append(sendback)
                
    print(times)
    mean_time_diff_totallatency = np.mean(time_diffs_totallatency[10:100])
    mean_time_diff_layer_preprocess = np.mean(time_diffs_layerpreprocess[20:200])*2
    mean_time_diff_render_wait = np.mean(time_diffs_render[10:100])
    mean_time_diff_image_copy = np.mean(time_diffs_copy[10:100])
    mean_time_diff_sendback = np.mean(time_diffs_sendback[10:100])
    mean_time_diff_present = np.mean(time_diffs_present[10:100])
    return mean_time_diff_totallatency,mean_time_diff_layer_preprocess,mean_time_diff_render_wait,mean_time_diff_image_copy,mean_time_diff_sendback,mean_time_diff_present


# 定义一个空 DataFrame 用于存储结果
result_df = pd.DataFrame(columns=['resolution', 'method', 'gpunum', 'total_latency','lp','rw','ic','sb','pr'])


for resolution in ['360', '480', '720', '1080']:
    for method in ['benchmark', 'multithread', 'gvulkan']:
        for gpunum in ['1', '2', '4']:

            # for method_name in ['rasterization', 'raytracing']:
            if resolution == '720':
                folder_path = f'./scene/'
            else:
                folder_path = f'./resolution/'

            server_log_file = os.path.join(folder_path, f'{gpunum}gpu/{gpunum}GPU_scene1{method}{resolution}p32_server.log')
            if method == 'gvulkan':
                total_latency,layer_preprocess,render_wait,image_copy,sendback,present  = extract_gvulkan_server_latency(server_log_file)
            else:
                total_latency,layer_preprocess,render_wait,image_copy,sendback,present  = extract_ben_server_latency(server_log_file)
            time_diff_df = pd.DataFrame({'resolution': resolution,
                                            'method': method,
                                            'gpunum': gpunum,
                                            'total_latency': total_latency,
                                            'lp': layer_preprocess,
                                            'rw': render_wait,
                                            'ic': image_copy,
                                            'sb': sendback,
                                            'pr': present,},  index=[0])
            result_df = pd.concat([result_df, time_diff_df], ignore_index=True)


# # local one GPU
# folder_path = f'1gpu/'
# server_log_file = os.path.join(folder_path, f'oneGPU.log')
# present  = extract_server_latency(server_log_file)
# time_diff_df = pd.DataFrame({'method_name': "local_oneGPU",
#                                 'gpu_num': 1,
#                                 'fps': present}, index=[0])
# result_df = pd.concat([result_df, time_diff_df], ignore_index=True)
    

# 将结果保存为 csv 文件
result_df.to_csv('gVulkan_resolution_fps.csv', index=False)