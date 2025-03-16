import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import fifo
import round_robin
import sjf
import srtf
import priority_que_non_preemptive
import priority_que_preemptive
import mlfq

file_path = ""
selected_algorithm = None
tree = None
time_quantum_entry = None
best_algo_text = None

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
    else:
        messagebox.showinfo("Success", "File uploaded successfully!")

def run_algorithm():
    global file_path, selected_algorithm, tree, time_quantum_entry
    
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    algorithm = selected_algorithm.get()
    
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading Excel file: {e}")
        return

    if algorithm == "FIFO":
        df = fifo.fifo_scheduling(df)
    elif algorithm == "Round Robin":
        time_quantum = time_quantum_entry.get()
        if not time_quantum.isdigit():
            messagebox.showerror("Error", "Invalid Time Quantum! Please enter a number.")
            return
        time_quantum = int(time_quantum)
        df = round_robin.round_robin_scheduling(df, time_quantum)
    elif algorithm == "SJF":
        df = sjf.sjf_scheduling(df)
    elif algorithm == "SRTF":
        df = srtf.srtf_scheduling(df)
    elif algorithm == "Priority Non-Preemptive":
        df = priority_que_non_preemptive.priority_scheduling(df)
    elif algorithm == "Priority Preemptive":
        df = priority_que_preemptive.preemptive_priority_scheduling(df)
    elif algorithm == "MLFQ":
        df = mlfq.mlfq_scheduler(df)
    else:
        messagebox.showerror("Error", "Invalid algorithm selected!")
        return

    display_results(df)

def display_results(df):
    global tree
    for row in tree.get_children():
        tree.delete(row)
    
    for i, row in df.iterrows():
        color = "#d9eaff" if i % 2 == 0 else "#b0d0ff"
        tree.insert("", tk.END, values=list(row), tags=("even" if i % 2 == 0 else "odd"))

def compare_all():
    os.system("python visualization.py")
    determine_best_algorithm()

def determine_best_algorithm():
    global best_algo_text
    report_file = "algorithm_comparison_report.txt"
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            report_content = f.read()
            best_algo_text.delete("1.0", tk.END)
            best_algo_text.insert(tk.END, report_content)
    else:
        best_algo_text.insert(tk.END, "Comparison report not found!")

# ========== Tkinter UI Setup ==========
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("900x650")
root.configure(bg='#e6f7ff') 


tk.Label(root, text="CPU Scheduling Algorithm Simulator", font=("Arial", 16, "bold"), bg='#e6f7ff', fg="black").pack(pady=10)

# Upload Section
upload_frame = tk.Frame(root, bg='#e6f7ff')
upload_frame.pack(pady=5)
tk.Label(upload_frame, text="Upload Process File:", font=("Arial", 12, "bold"), bg='#e6f7ff', fg="black").pack(side=tk.LEFT)
tk.Button(upload_frame, text="Upload", command=upload_file, font=("Arial", 10, "bold"), bg='#d1d1d1').pack(side=tk.LEFT, padx=10)

# Algorithm Selection
algo_frame = tk.Frame(root, bg='#e6f7ff')
algo_frame.pack(pady=5)
tk.Label(algo_frame, text="Select Scheduling Algorithm:", font=("Arial", 12, "bold"), bg='#e6f7ff', fg="black").pack(side=tk.LEFT)

algorithm_options = ["FIFO", "Round Robin", "Priority Non-Preemptive", "Priority Preemptive", "SJF", "SRTF", "MLFQ"]
selected_algorithm = tk.StringVar()
selected_algorithm.set(algorithm_options[0])
algo_dropdown = ttk.Combobox(algo_frame, textvariable=selected_algorithm, values=algorithm_options, font=("Arial", 10))
algo_dropdown.pack(side=tk.LEFT, padx=10)

# Buttons
button_frame = tk.Frame(root, bg='#e6f7ff')
button_frame.pack(pady=5)
tk.Button(button_frame, text="Run Algorithm", command=run_algorithm, font=("Arial", 10, "bold"), bg='#d1d1d1').pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Compare All", command=compare_all, font=("Arial", 10, "bold"), bg='#d1d1d1').pack(side=tk.LEFT, padx=10)

# Result Table
tree = ttk.Treeview(root, columns=("ID", "AT", "ET", "Priority", "CT", "TAT", "WT"), show="headings")
for col in ("ID", "AT", "ET", "Priority", "CT", "TAT", "WT"):
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.tag_configure("even", background="#d9eaff")
tree.tag_configure("odd", background="#b0d0ff")
tree.pack(pady=10)

# Best Algorithm Report (Blended Background)
tk.Label(root, text="Best Algorithm Report:", font=("Arial", 12, "bold"), bg='#e6f7ff', fg="black").pack()
best_algo_text = tk.Text(root, height=5, width=80, font=("Arial", 10), bg="#ffffff")
best_algo_text.pack(pady=5)

# Time Quantum Input (only for Round Robin)
time_quantum_frame = tk.Frame(root, bg='#e6f7ff')
time_quantum_frame.pack(pady=5)
tk.Label(time_quantum_frame, text="Enter Time Quantum:", font=("Arial", 12, "bold"), bg='#e6f7ff', fg="black").pack(side=tk.LEFT)
time_quantum_entry = tk.Entry(time_quantum_frame, font=("Arial", 10))
time_quantum_entry.pack(side=tk.LEFT, padx=10)

root.mainloop()
