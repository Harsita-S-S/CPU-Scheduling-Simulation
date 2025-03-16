import pandas as pd
from collections import deque

def mlfq_scheduler(df, time_quantum=4):
    # Sorting processes by arrival time
    df = df.sort_values(by=['AT']).reset_index(drop=True)
    
    # Setup the queues (3 priority levels, each with a different time slice)
    high_priority_queue = deque()  # Queue 1
    medium_priority_queue = deque()  # Queue 2
    low_priority_queue = deque()  # Queue 3
    
    # Track the tasks
    completed_tasks = []
    current_time = 0
    task_counter = 0  # To handle task promotion and demotion
    
    # Add all tasks to the high priority queue initially
    for _, row in df.iterrows():
        high_priority_queue.append(row.to_dict())
    
    while high_priority_queue or medium_priority_queue or low_priority_queue:
        # Fetch the next task to execute (from the highest priority non-empty queue)
        if high_priority_queue:
            current_task = high_priority_queue.popleft()
        elif medium_priority_queue:
            current_task = medium_priority_queue.popleft()
        else:
            current_task = low_priority_queue.popleft()
        
        # Execute the task
        arrival_time = current_task['AT']
        execution_time = current_task['ET']
        task_id = current_task['ID']
        
        if current_time < arrival_time:
            current_time = arrival_time  # Skip to arrival time if needed
        
        # Determine how long the task will run (time slice based on priority)
        time_slice = time_quantum  # Default time slice for higher-priority tasks
        if current_task in medium_priority_queue:
            time_slice = time_quantum * 2  # Longer time slice for medium priority
        elif current_task in low_priority_queue:
            time_slice = time_quantum * 4  # Even longer time slice for lower priority
        
        # Run the task for its time slice (or finish it if it has less remaining time)
        run_time = min(execution_time, time_slice)
        
        # Update task execution time and current time
        execution_time -= run_time
        current_time += run_time
        
        # Check if the task has completed
        if execution_time > 0:
            # Task is not finished, move it to the next lower priority queue
            if current_task in high_priority_queue:
                medium_priority_queue.append(current_task)
            elif current_task in medium_priority_queue:
                low_priority_queue.append(current_task)
            # If it's already in low priority queue, leave it there
        else:
            # Task has finished execution
            current_task['CT'] = current_time
            current_task['TAT'] = current_time - current_task['AT']
            current_task['WT'] = current_task['TAT'] - current_task['ET']
            completed_tasks.append(current_task)
    
    # Convert completed tasks to a DataFrame
    completed_df = pd.DataFrame(completed_tasks)
    
    return completed_df
