import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import fifo
import round_robin
import sjf
import srtf
import priority_que_non_preemptive as p1
import priority_que_preemptive as p2
import mlfq

matplotlib.use("QtAgg") 

file_path = 'process.xlsx'
df = pd.read_excel(file_path)


results = {
    "FIFO": fifo.fifo_scheduling(df.copy()),
    "RR": round_robin.round_robin_scheduling(df.copy(), Q=2),
    "SJF": sjf.sjf_scheduling(df.copy()),
    "SRTF": srtf.srtf_scheduling(df.copy()),
    "PQ_NP": p1.priority_scheduling(df.copy()),
    "PQ_P": p2.preemptive_priority_scheduling(df.copy()),
    "MLFQ": mlfq.mlfq_scheduler(df.copy())
}


metrics = {}
for name, result in results.items():
    if 'CT' not in result or result['CT'].empty:
        continue

    throughput = len(result) / result['CT'].max()
    avg_tat = result['TAT'].mean()
    cpu_idle = max(result['CT'].max() - result['AT'].min() - result['ET'].sum(), 0)
    metrics[name] = {"Throughput": throughput, "Avg TAT": avg_tat, "CPU Idle": cpu_idle}

metrics_df = pd.DataFrame(metrics).T


fig, ax = plt.subplots(1, 3, figsize=(15, 5))
colors = plt.cm.Set1(range(len(metrics_df)))


ax[0].bar(metrics_df.index, metrics_df['Throughput'], color=colors, label='Throughput')
ax[0].set_title("Throughput Comparison")
ax[0].set_ylabel("Processes per Time Unit")
ax[0].plot(metrics_df.index, metrics_df['Throughput'], color='black', marker='o', linestyle='-', label='Line for Throughput')
ax[0].legend()


ax[1].bar(metrics_df.index, metrics_df['Avg TAT'], color=colors, label='Avg TAT')
ax[1].set_title("Average Turnaround Time (TAT)")
ax[1].set_ylabel("Time Units")
ax[1].plot(metrics_df.index, metrics_df['Avg TAT'], color='black', marker='o', linestyle='-', label='Line for Avg TAT')
ax[1].legend()


ax[2].bar(metrics_df.index, metrics_df['CPU Idle'], color=colors, label='CPU Idle')
ax[2].set_title("CPU Idle Time")
ax[2].set_ylabel("Idle Time Units")
ax[2].plot(metrics_df.index, metrics_df['CPU Idle'], color='black', marker='o', linestyle='-', label='Line for CPU Idle')
ax[2].legend()

manager = plt.get_current_fig_manager()
try:
    manager.window.showMaximized()
except AttributeError:
    fig.set_size_inches(18, 7)

plt.tight_layout()
plt.show()


best_algorithm = metrics_df.idxmin()['Avg TAT']  
print(f"\nBest Algorithm Based on Avg TAT: {best_algorithm}")


with open('algorithm_comparison_report.txt', 'w') as f:
    f.write("CPU Scheduling Algorithm Comparison Report\n")
    f.write("=" * 50 + "\n\n")
    f.write(metrics_df.to_string())
    f.write("\n\nBest Algorithm Based on Avg TAT: " + best_algorithm)
    f.write("\nBest Algorithm Based on Throughput: " + metrics_df.idxmax()['Throughput'])
    f.write("\nBest Algorithm Based on CPU Idle: " + metrics_df.idxmin()['CPU Idle'])
    f.write("\n")
