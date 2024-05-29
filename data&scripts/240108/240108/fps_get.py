import os
import pandas as pd
import re
import numpy as np

# 定义一个函数用于提取每个log文件的延时信息
def extract_latency(log_file):
    latency = None
    with open(log_file, 'r') as f:
        for line in f:
            if 'latency' in line:
                latency = float(line.split()[-1])
                break
    return latency

def extract_layer_latency(log_file):
    time_diffs = []
    with open(log_file, 'r') as f:
        for line in f:
            start_match = re.match(r'\[(\d+\.\d+)\]\s+SOCKET START (\d)', line)
            end_match = re.match(r'\[(\d+\.\d+)\]\s+SOCKET END (\d)', line)
            if start_match:
                if start_match.group(2) == '1':
                    start_time = float(start_match.group(1))
                    try:
                        next_line = next(f)
                        end_match = re.match(r'\[(\d+\.\d+)\]\s+SOCKET END (\d)', next_line)
                        if end_match and end_match.group(2) == '1':
                            end_time = float(end_match.group(1))
                            time_diffs.append(end_time - start_time)
                        else:
                            raise StopIteration
                    except StopIteration:
                        continue
    # 计算平均值
    mean_time_diff = np.mean(time_diffs)
    return mean_time_diff

def extract_server_latency(log_file):
    time_dict = {'cycle_end_old': None,'cycle_end_new': None}
    time_diffs_present = []
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
    mean_time_diff_present = np.mean(time_diffs_present[10:-10])
    return mean_time_diff_present

def extract_localOneGPU_latency(log_file):
    time_dict = {'parallel_render': None, 'cycle_end': None, 'primary_device_copy': None}
    time_diffs_preprocess = []
    time_diffs_render = []
    time_diffs_present = []
    with open(log_file, 'r') as f:
        for line in f:
            parallel_render_match = re.match(r'\[(\d+\.\d+)\]\s+Parrallel Render (\d+)', line)
            cycle_end_match = re.match(r'\[(\d+\.\d+)\]\s+CYCLE End (\d+)', line)
            primary_device_present_match = re.match(r'\[(\d+\.\d+)\]\s+Primary Device Copy the Image in Swapchin (\d+)', line)
            if parallel_render_match:
                time_dict['parallel_render'] = float(parallel_render_match.group(1))
            elif cycle_end_match:
                time_dict['cycle_end'] = float(cycle_end_match.group(1))
            elif primary_device_present_match:
                time_dict['primary_device_copy'] = float(primary_device_present_match.group(1))
            if None not in time_dict.values():
                print(time_dict)
                if parallel_render_match:
                    pre_process = time_dict['parallel_render'] - time_dict['cycle_end']
                    time_diffs_preprocess.append(pre_process)
                elif primary_device_present_match:
                    render = time_dict['primary_device_copy'] - time_dict['parallel_render']
                    time_diffs_render.append(render)
                elif cycle_end_match:
                    present = time_dict['cycle_end'] - time_dict['primary_device_copy']
                    time_diffs_present.append(present)
    mean_time_diff_preprocess = np.mean(time_diffs_preprocess)
    mean_time_diff_render = np.mean(time_diffs_render)
    mean_time_diff_present = np.mean(time_diffs_present)
    return mean_time_diff_preprocess,mean_time_diff_render,mean_time_diff_present

# 定义一个空 DataFrame 用于存储结果
result_df = pd.DataFrame(columns=['latency', 'batch', 'single'])


for latency in ['0', '01', '03', '05', '1', '2', '3', '4', '5', '8', '10']:
    # for method_name in ['rasterization', 'raytracing']:
    folder_path = f'./'
    batch_log_file = os.path.join(folder_path, f'{latency}batch.log')
    single_log_file = os.path.join(folder_path, f'{latency}single.log')
    batch  = extract_server_latency(batch_log_file)
    single = extract_server_latency(single_log_file)
    if latency[0] == '0':
        latencyname = f'0.{latency[1:]}'
    else:
        latencyname = latency
    time_diff_df = pd.DataFrame({'latency': latencyname,
                                    'batch': 1000/batch,
                                    'single': 1000/single}, index=[0])
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
result_df.to_csv('fps_batchandsingle.csv', index=False)