import pandas as pd
from collections import deque

def sjf_scheduling(df):
    current_time = 0
    queue = deque()
    completed_processes = set()
    ct, tat, wt = {}, {}, {}

    df = df.sort_values(by=['AT']).reset_index(drop=True)
    remaining_processes = {row['ID']: row['ET'] for _, row in df.iterrows()}

    while len(completed_processes) < len(df):

        for index, row in df.iterrows():
            if row['AT'] <= current_time and row['ID'] not in queue and row['ID'] not in completed_processes:
                queue.append(row['ID'])

        if not queue:
            current_time += 1
            continue

        queue = deque(sorted(queue, key=lambda pid: remaining_processes[pid]))
        process_id = queue.popleft()
        burst_time = remaining_processes[process_id]

        current_time += burst_time
        completed_processes.add(process_id)

        ct[process_id] = current_time
        tat[process_id] = ct[process_id] - df.loc[df['ID'] == process_id, 'AT'].values[0]
        wt[process_id] = tat[process_id] - df.loc[df['ID'] == process_id, 'ET'].values[0]

    df['CT'] = df['ID'].map(ct)
    df['TAT'] = df['ID'].map(tat)
    df['WT'] = df['ID'].map(wt)
    
    return df
