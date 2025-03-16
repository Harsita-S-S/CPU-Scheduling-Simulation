import pandas as pd

def preemptive_priority_scheduling(df):
    # Sort by Arrival Time (AT) and Priority (lower value = higher priority)
    df = df.sort_values(by=['AT', 'Priority']).reset_index(drop=True)

    # Initialize variables
    current_time = 0
    remaining_time = df['ET'].tolist()  # Store remaining execution time
    completed = [False] * len(df)  # Track completed processes
    completion_time = [0] * len(df)
    turnaround_time = [0] * len(df)
    waiting_time = [0] * len(df)

    while not all(completed):  # Loop until all processes are completed
        available_processes = [
            i for i in range(len(df))
            if df.at[i, 'AT'] <= current_time and not completed[i]
        ]

        if available_processes:
            # Select process with highest priority (lower number = higher priority)
            highest_priority_index = min(available_processes, key=lambda i: df.at[i, 'Priority'])

            # Execute for 1 unit of time
            remaining_time[highest_priority_index] -= 1
            current_time += 1

            # If the process is finished
            if remaining_time[highest_priority_index] == 0:
                completed[highest_priority_index] = True
                completion_time[highest_priority_index] = current_time
                turnaround_time[highest_priority_index] = completion_time[highest_priority_index] - df.at[highest_priority_index, 'AT']
                waiting_time[highest_priority_index] = turnaround_time[highest_priority_index] - df.at[highest_priority_index, 'ET']
        else:
            # If no process is available, CPU is idle
            current_time += 1

    # Store results in DataFrame
    df['CT'] = completion_time
    df['TAT'] = turnaround_time
    df['WT'] = waiting_time

    return df
