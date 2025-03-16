# 🖥️ CPU Scheduling Simulator 🚀

This project is a **CPU Scheduling Algorithm Simulator** implemented using Python and Tkinter. It allows users to upload a process scheduling dataset, apply different scheduling algorithms, and compare their performance visually.

## ✨ Features
- Supports multiple scheduling algorithms:
  - ⏳ First Come First Serve (**FIFO**)
  - 🔄 Round Robin (**RR**)
  - 🕒 Shortest Job First (**SJF**)
  - ⏬ Shortest Remaining Time First (**SRTF**)
  - 🎖️ Priority Scheduling (**Preemptive & Non-Preemptive**)
  - 📊 Multi-Level Feedback Queue (**MLFQ**)
- Upload process data via an Excel file. (use the sample input process.xlsx, large_processes_data.xlsx, or any input of your own)
- Run a selected scheduling algorithm and display results in a table.
- Compare all algorithms with visualization and detailed performance metrics.
- Automatically determine the best algorithm based on turnaround time, throughput, and CPU idle time.

## Installation & Requirements
### 📌 Prerequisites
Ensure you have Python installed (preferably Python 3.x) and install the required dependencies:
```bash
pip install pandas openpyxl matplotlib
```

### ▶️ Running the Simulator
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/cpu-scheduling-simulator.git
   cd cpu-scheduling-simulator
   ```
2. Run the main application:
   ```bash
   python main.py
   ```

## 🛠️ Usage
1. **📤 Upload an Excel file** containing process scheduling data (with columns: ID, AT, ET, Priority).
2. **🎛️ Select a scheduling algorithm** from the dropdown menu.
3. **▶️ Run the algorithm** to see computed values (CT, TAT, WT) in the table.
4. **📊 Use "Compare All"** to visualize multiple scheduling algorithms and generate a report.

## 📁 Project Structure
```
├── fifo.py                        # First Come First Serve scheduling
├── round_robin.py                 # Round Robin scheduling
├── sjf.py                         # Shortest Job First scheduling
├── srtf.py                        # Shortest Remaining Time First scheduling
├── priority_que_non_preemptive.py  # Non-Preemptive Priority scheduling
├── priority_que_preemptive.py      # Preemptive Priority scheduling
├── mlfq.py                        # Multi-Level Feedback Queue scheduling
├── visualization.py                # Performance comparison & visualization
├── main.py                        # Tkinter-based GUI application
├── README.md                       # Project documentation
```

## 📊 Visualization & Comparison
When you select **"Compare All"**, `visualization.py` generates:
- A bar chart comparing **Throughput, Average Turnaround Time, and CPU Idle Time**.
- A **detailed report** determining the best algorithm based on performance metrics.
