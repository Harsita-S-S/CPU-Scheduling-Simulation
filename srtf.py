import pandas as pd
from collections import deque

def srtf_scheduling(df):
    current_time = 0
    queue = deque()
    remaining_time = {row['ID']: row['ET'] for _, row in df.iterrows()}
    completed_processes = set()
    ct, tat, wt = {}, {}, {}

    active_process = None  

    while len(completed_processes) < len(df):
    
        for index, row in df.iterrows():
            if row['AT'] <= current_time and row['ID'] not in queue and row['ID'] not in completed_processes:
                queue.append(row['ID'])

        if not queue:
            current_time += 1
            continue

       
        queue = deque(sorted(queue, key=lambda pid: remaining_time[pid]))
        process_id = queue.popleft()

        if active_process and remaining_time[process_id] < remaining_time[active_process]:
           
            queue.appendleft(active_process) 
            active_process = process_id
        else:
            active_process = process_id

        remaining_time[active_process] -= 1
        current_time += 1


        if remaining_time[active_process] == 0:
            completed_processes.add(active_process)
            ct[active_process] = current_time
            tat[active_process] = ct[active_process] - df.loc[df['ID'] == active_process, 'AT'].values[0]
            wt[active_process] = tat[active_process] - df.loc[df['ID'] == active_process, 'ET'].values[0]

            active_process = None  

    df['CT'] = df['ID'].map(ct)
    df['TAT'] = df['ID'].map(tat)
    df['WT'] = df['ID'].map(wt)
    
    return df
