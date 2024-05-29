import os
import pandas as pd
import re
import numpy as np
import csv

# 定义一个函数用于提取每个log文件的延时信息

def extract_dynamic_latency(log_file, gpu_num):
    time_dict = {'cycle_end_old': None, 'cycle_end_new' : None}
    render_dict = {i: None for i in range(gpu_num)}
    time_diffs_render = {i: [] for i in range(gpu_num)}
    time_diffs_time = []
    time_diffs_fps = []
    with open(log_file, 'r') as f:
        for line in f:
            cycle_end_match = re.match(r'\[(\d+\.\d+)\]\s+CYCLE End (\d+)', line)
            cycle_render_start = re.match(r'\[(\d+\.\d+)\]\s+GPU\s+(\d+)\s+Rendering\s+Start\s', line)
            cycle_render_end = re.match(r'\[(\d+\.\d+)\]\s+GPU\s+(\d+)\s+Rendering\s+End\s', line)

            if cycle_render_start:
                gpu_id = int(cycle_render_start.group(2))
                render_dict[gpu_id] = float(cycle_render_start.group(1))
            
            if cycle_render_end:
                gpu_id = int(cycle_render_end.group(2))
                time_diffs_render[gpu_id].append(float(cycle_render_end.group(1)) - render_dict[gpu_id])

            if cycle_end_match:
                time_dict['cycle_end_old'] = time_dict['cycle_end_new']
                time_dict['cycle_end_new'] = float(cycle_end_match.group(1))

            if None not in time_dict.values():
                # print(time_dict)
                if cycle_end_match:
                    fps = time_dict['cycle_end_new'] - time_dict['cycle_end_old']
                    time_diffs_fps.append(fps)
                    time_diffs_time.append(time_dict['cycle_end_new'])
    gpu_latency = [np.mean(time_diffs_render[i]) if time_diffs_render[i] else 0 for i in range(gpu_num)]
    return time_diffs_fps,time_diffs_time,gpu_latency,time_diffs_render

# 定义一个空 DataFrame 用于存储结果
result_df = pd.DataFrame(columns=['method_name', 'gpu_num', 'GPU0_latency', 'GPU1_latency', 'GPU2_latency', 'GPU3_latency'])


for gpu_num in [2, 4]:
    for method_name in ['Dynamic-notanything', 'Dynamic-threashold']:
        folder_path = f'./'
        server_log_file = os.path.join(folder_path, f'{gpu_num}gpu{method_name}.log')
        fps,time,gpu_latency,time_diffs_render  = extract_dynamic_latency(server_log_file, gpu_num)
        if gpu_num == 2:
            data = np.stack([fps, time, time_diffs_render[0][1:], time_diffs_render[1][1:]], axis=1)
        else:
            data = np.stack([fps, time, time_diffs_render[0][1:], time_diffs_render[1][1:], time_diffs_render[2][1:], time_diffs_render[3][1:]], axis=1)
        transposed_data = np.transpose(data)
        with open(f'{gpu_num}{method_name}fps.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            rows = [list(row) for row in zip(*transposed_data)]
            for row in rows:
                writer.writerow(row)
        # if(gpu_num == 2):
        #     time_diff_df = pd.DataFrame({'method_name': method_name,
        #                                     'gpu_num': gpu_num,
        #                                     'GPU0_latency': gpu_latency[0],
        #                                     'GPU1_latency': gpu_latency[1],
        #                                     'GPU2_latency': 0,
        #                                     'GPU3_latency': 0}, index=[0])
        # else:
        #     time_diff_df = pd.DataFrame({'method_name': method_name,
        #                                     'gpu_num': gpu_num,
        #                                     'GPU0_latency': gpu_latency[0],
        #                                     'GPU1_latency': gpu_latency[1],
        #                                     'GPU2_latency': gpu_latency[2],
        #                                     'GPU3_latency': gpu_latency[3]}, index=[0])
        # result_df = pd.concat([result_df, time_diff_df], ignore_index=True)
    

# 将结果保存为 csv 文件
# result_df.to_csv('latency.csv', index=False)