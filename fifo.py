import pandas as pd

def fifo_scheduling(df):
    current_time = 0
    ct, tat, wt = [], [], []

    for _, row in df.iterrows():
        if current_time < row['AT']:
            current_time = row['AT']
        
        ct_time = current_time + row['ET']
        ct.append(ct_time)
        
        tat_time = ct_time - row['AT']
        tat.append(tat_time)
        
        wt_time = tat_time - row['ET']
        wt.append(wt_time)

        current_time = ct_time

    df['CT'] = ct
    df['TAT'] = tat
    df['WT'] = wt
    return df