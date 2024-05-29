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

# 定义一个空 DataFrame 用于存储结果
result_df = pd.DataFrame(columns=['networklatency', 'method', 'fps'])


for networklatency in ['00', '01', '02', '03', '05', '1', '2', '3', '4', '5']:
    for method in ['benchmark', 'multithread', 'gvulkan', 'single']:
        # for method_name in ['rasterization', 'raytracing']:
        folder_path = f'./Network/'
        server_log_file = os.path.join(folder_path, f'{networklatency}scene1{method}720p16_server.log')
        server  = extract_server_latency(server_log_file)
        time_diff_df = pd.DataFrame({'networklatency': networklatency,
                                        'method': method,
                                        'fps': 1000/server},  index=[0])
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
result_df.to_csv('gVulkan_network_fps.csv', index=False)