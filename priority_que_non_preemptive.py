import pandas as pd

def priority_scheduling(df):
    # Sort processes by Arrival Time (AT), then by Priority (lower value = higher priority)
    df = df.sort_values(by=['AT', 'Priority']).reset_index(drop=True)  
    
    current_time = 0
    ct, tat, wt = [], [], []

    for _, row in df.iterrows():
        if current_time < row['AT']:  # If CPU is idle, jump to process arrival
            current_time = row['AT']
        
        ct_time = current_time + row['ET']
        ct.append(ct_time)
        
        tat_time = ct_time - row['AT']
        tat.append(tat_time)
        
        wt_time = tat_time - row['ET']
        wt.append(wt_time)

        current_time = ct_time  # Move time forward

    # Store computed values in DataFrame
    df['CT'] = ct
    df['TAT'] = tat
    df['WT'] = wt
    
    return df
