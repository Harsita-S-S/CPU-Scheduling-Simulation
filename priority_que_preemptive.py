import pandas as pd

def preemptive_priority_scheduling(df):
    # Sort processes by Arrival Time (AT), then by Priority (lower value = higher priority)
    df = df.sort_values(by=['AT', 'Priority']).reset_index(drop=True)
    
    # Initialize variables
    current_time = 0
    ct, tat, wt = [], [], []
    pending_tasks = []  # To keep track of the pending tasks
    completed_tasks = []  # To track completed tasks

    # Task queue to track running and ready tasks
    while not df.empty or pending_tasks:
        # Add tasks that have arrived by current time
        arrived_tasks = df[df['AT'] <= current_time]
        df = df[df['AT'] > current_time]
        
        # Add these tasks to the pending_tasks queue
        pending_tasks.extend(arrived_tasks.to_dict(orient='records'))

        if pending_tasks:
            # Sort pending tasks by priority (lower priority number means higher priority)
            pending_tasks.sort(key=lambda x: x['Priority'])

            # Select the highest priority task (first task after sorting)
            current_task = pending_tasks.pop(0)

            # Start or continue the task
            if current_time < current_task['AT']:
                current_time = current_task['AT']  # Jump forward in time if CPU is idle

            # Calculate Completion Time (CT)
            ct_time = current_time + current_task['ET']
            ct.append(ct_time)

            # Calculate Turnaround Time (TAT) and Waiting Time (WT)
            tat_time = ct_time - current_task['AT']
            tat.append(tat_time)

            wt_time = tat_time - current_task['ET']
            wt.append(wt_time)

            # Mark the task as completed
            completed_tasks.append(current_task)
            
            current_time = ct_time  # Move the current time forward
        else:
            # If there are no tasks to execute, increment time (CPU idle)
            current_time += 1

    # Convert completed tasks back to a DataFrame
    completed_df = pd.DataFrame(completed_tasks)

    # Assign the computed values (CT, TAT, WT) back to the DataFrame
    completed_df['CT'] = ct
    completed_df['TAT'] = tat
    completed_df['WT'] = wt
    
    # Return the DataFrame with the final scheduling results
    return completed_df


