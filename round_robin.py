import pandas as pd
from collections import deque

def round_robin_scheduling(df, Q):
    current_time = 0
    queue = deque()
    remaining_time = {row['ID']: row['ET'] for _, row in df.iterrows()}
    completed_processes = set()
    ct, tat, wt = {}, {}, {}

    while len(completed_processes) < len(df):
        for index, row in df.iterrows():
            if row['AT'] <= current_time and row['ID'] not in queue and row['ID'] not in completed_processes:
                queue.append(row['ID'])

        if not queue:
            current_time += 1
            continue

        process_id = queue.popleft()
        execute_time = min(Q, remaining_time[process_id])
        current_time += execute_time
        remaining_time[process_id] -= execute_time

        if remaining_time[process_id] == 0:
            completed_processes.add(process_id)
            ct[process_id] = current_time
            tat[process_id] = ct[process_id] - df.loc[df['ID'] == process_id, 'AT'].values[0]
            wt[process_id] = tat[process_id] - df.loc[df['ID'] == process_id, 'ET'].values[0]
        else:
            queue.append(process_id)

    df['CT'] = df['ID'].map(ct)
    df['TAT'] = df['ID'].map(tat)
    df['WT'] = df['ID'].map(wt)
    return df

