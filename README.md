# ⚙️ Multi-Core Processor Load Balancing Simulator

### Intelligent Workload Distribution and Scheduling Across Multiple CPU Cores

A Python-based engineering project that simulates, analyzes, and compares workload distribution across multiple CPU cores using different scheduling algorithms. Includes a professional **Streamlit dashboard**, interactive visualizations, performance analytics, and a command-line interface.

---

## 📌 Overview

Multi-Core Processor Load Balancing is a software simulation project designed to demonstrate how computational tasks can be distributed across multiple processor cores to improve workload balance and reduce simulated task completion time.

When multiple tasks are assigned to multiple CPU cores, an inefficient distribution can leave some cores overloaded while others remain underutilized. This project explores different scheduling strategies and evaluates their effectiveness using mathematical performance metrics.

The simulator implements three scheduling algorithms:

1. **Round Robin (RR)** – Distributes tasks sequentially among available cores.
2. **Greedy Least Loaded Core** – Assigns each incoming task to the core with the lowest accumulated workload.
3. **Longest Processing Time First (LPT)** – Prioritizes longer tasks and assigns them to the currently least-loaded core.

The project provides two ways to interact with the system:

- **Command-Line Interface (CLI):** Execute scheduling simulations and inspect results.
- **Advanced Streamlit Dashboard:** Interactively configure workloads, compare algorithms, visualize core utilization, and explore performance metrics.

The CLI and Streamlit application share the same scheduling engine, ensuring consistent algorithm implementations and calculations.

---

## 🎯 Project Objectives

- Understand multi-core processor architecture and workload distribution.
- Implement multiple processor load-balancing algorithms.
- Compare scheduling strategies using different task workloads.
- Analyze simulated processor utilization and workload imbalance.
- Visualize task distribution across multiple CPU cores.
- Build an interactive dashboard for scheduling analysis.
- Demonstrate software engineering concepts through modular Python development.

---

## ✨ Key Features

### 1. Scheduling Algorithms

| Algorithm | Description |
|---|---|
| Round Robin | Assigns tasks sequentially across CPU cores. |
| Greedy Least Loaded Core | Assigns the next task to the core with the lowest current workload. |
| Longest Processing Time First | Sorts tasks by execution time and assigns longer tasks first to the least-loaded core. |

### 2. Advanced Streamlit Dashboard

An interactive engineering dashboard designed for workload analysis and algorithm comparison.

Features include:

- Professional dark-themed dashboard interface.
- Interactive CPU core and task configuration.
- Manual task execution-time input.
- Comma-separated task input.
- Random task generation.
- CSV task import.
- Real-time simulation results after execution.
- Algorithm selection and comparison.
- Performance metric cards.
- Core-wise workload analysis.
- Interactive Plotly visualizations.
- Detailed task allocation tables.
- Automatically generated technical insights.
- CSV results export.
- Educational algorithm explanations.

### 3. Performance Analytics

The application calculates:

- Total Workload
- Average Core Workload
- Makespan
- Load Imbalance
- Simulated Processor Utilization
- Simulated Speedup

### 4. Interactive Visualizations

The dashboard provides visual analysis through:

- Core-wise workload distribution.
- Task assignment across CPU cores.
- Scheduling algorithm comparison.
- Workload imbalance analysis.
- Core utilization visualization.
- Before-and-after workload comparison.

### 5. Software Engineering Features

- Modular Python architecture.
- Reusable scheduling functions.
- Centralized performance calculations.
- Input validation and error handling.
- CSV import and export.
- Automated test suite.
- Command-line and web-based interfaces.

---

## 🏗️ System Architecture

The application follows a modular architecture that separates user interaction, scheduling logic, mathematical calculations, validation, and visualization.

```text
                 USER INPUT
                     |
          +----------+----------+
          |                     |
      CLI Interface       Streamlit Dashboard
       (main.py)               (app.py)
          |                     |
          +----------+----------+
                     |
              INPUT VALIDATION
               (validation.py)
                     |
              SCHEDULING ENGINE
                (scheduler.py)
                     |
          +----------+----------+
          |          |          |
       Round      Greedy       LPT
       Robin      Least       Scheduling
                  Loaded
          |          |          |
          +----------+----------+
                     |
              PERFORMANCE METRICS
                 (metrics.py)
                     |
             RESULTS PROCESSING
                     |
          +----------+----------+
          |                     |
     Visualization        CSV Export
    (visualization.py)
          |
     Matplotlib / Plotly
```

**Important:** Both interfaces reuse the same scheduling engine and metric calculations. Scheduling algorithms are not duplicated inside the Streamlit application.

---

## 🧠 Scheduling Algorithms Explained

### 1. Round Robin Scheduling

Round Robin distributes tasks sequentially across the available CPU cores.

**Working principle:**
- Initialize all core workloads.
- Assign the first task to the first core.
- Assign the next task to the next core.
- Continue cyclically until all tasks are allocated.

This project's Round Robin implementation performs cyclic task assignment without a time quantum. It is not the same as preemptive Round Robin CPU scheduling.

### 2. Greedy Least Loaded Core

This algorithm attempts to keep the accumulated workload of the cores balanced.

**Working principle:**
- Initialize all core workloads to zero.
- Select the next task.
- Identify the core with the smallest accumulated workload.
- Assign the task to that core.
- Update its workload.
- Repeat until all tasks are assigned.

### 3. Longest Processing Time First (LPT)

LPT prioritizes longer tasks to improve workload distribution.

**Working principle:**
- Sort tasks in descending order of execution time.
- Select the longest remaining task.
- Assign it to the currently least-loaded core.
- Update the workload.
- Repeat until all tasks are allocated.

LPT is a scheduling heuristic and does not guarantee an optimal result for every possible workload.

---

## 📐 Performance Metrics

The simulator uses mathematical metrics to evaluate scheduling performance.

| Metric | Formula | Purpose |
|---|---|---|
| Total Workload | Sum of all task durations | Measures total computational work. |
| Average Workload | Total Workload / Number of Cores | Calculates average assigned workload. |
| Makespan | Maximum Core Workload | Estimates total parallel completion time. |
| Load Imbalance | Maximum Workload − Minimum Workload | Measures the workload range between cores. |
| Simulated Utilization | Total Workload / (Cores × Makespan) × 100 | Measures the proportion of available core-time occupied by assigned work. |
| Simulated Speedup | Sequential Time / Makespan | Estimates improvement over sequential execution. |

**Note:** These metrics are based on an idealized scheduling simulation using estimated task durations. They do not represent actual hardware CPU utilization or benchmarked processor performance.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive charts and visualizations |
| Matplotlib | Workload visualization |
| NumPy | Mathematical operations |
| Pandas | Data handling and CSV processing |
| python-docx | Word document generation |

---

## 📂 Project Structure

```text
Multi_Core_Processor_Load_Balancing/
│
├── main.py                  # CLI entry point and user interaction
│
├── app.py                   # Advanced Streamlit web dashboard
│
├── scheduler.py             # RR, Greedy and LPT algorithms
│
├── metrics.py               # Performance calculations
│
├── validation.py            # Input validation and error handling
│
├── visualization.py         # Workload charts and comparisons
│
├── test_scheduler.py        # Automated tests (TC01–TC18)
│
├── requirements.txt         # Project dependencies
│
└── README.md                # Project documentation
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or above
- pip package manager
- VS Code or PyCharm (recommended)

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### Step 2: Navigate to the Project Directory

```bash
cd Multi_Core_Processor_Load_Balancing
```

### Step 3: Create a Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 🚀 Running the Application

The project provides two execution modes.

### 1. Command-Line Interface (CLI)

Run the Python simulator:

```bash
python main.py
```

The CLI allows you to:

- Enter the number of CPU cores.
- Enter the number of computational tasks.
- Provide task execution times.
- Execute scheduling algorithms.
- View core-wise workload distribution.
- Compare algorithm performance.

### 2. Advanced Streamlit Web Dashboard

The interactive dashboard is a mandatory component of the project.

Launch it using:

```bash
streamlit run app.py
```

After successful execution, Streamlit provides a local browser address, normally:

```text
http://localhost:8501
```

Open this address in your browser to access the dashboard.

The dashboard supports interactive input, scheduling execution, algorithm comparison, visual analytics, technical insights, and CSV export.

---

## 🧪 Testing

The project includes an automated test suite covering scheduling functionality, workload calculations, validation, and edge cases.

Run the tests using:

```bash
python -m unittest test_scheduler.py -v
```

The test suite is designed to cover:

| Test ID | Test Scenario |
|---|---|
| TC01 | Normal task distribution |
| TC02 | Single CPU core |
| TC03 | More cores than tasks |
| TC04 | Equal task durations |
| TC05 | Unequal task durations |
| TC06 | Single task |
| TC07 | Large task collection |
| TC08 | Invalid number of cores |
| TC09 | Negative task duration |
| TC10 | Zero task duration |
| TC11 | Empty task input |
| TC12 | Non-numeric input |
| TC13 | Floating-point task durations |
| TC14 | Deterministic tie-breaking |
| TC15 | Task preservation |
| TC16 | No duplicated assignments |
| TC17 | Workload preservation |
| TC18 | Makespan and utilization consistency |

Run the complete test suite before submitting changes.

Test results should be based on actual execution rather than assumed outcomes.

---

## 📊 Project Applications

The concepts demonstrated by this project are relevant to:

- Multi-core operating systems.
- Parallel computing.
- CPU task scheduling.
- Cloud computing infrastructure.
- Data centre workload distribution.
- Scientific computing.
- Artificial Intelligence and Machine Learning workloads.
- Performance optimization.

The simulator provides an educational model of workload distribution rather than a real-time production scheduler.

---

## 🔬 Limitations

The current simulation uses a simplified scheduling model.

Assumptions include:

- Identical processor cores.
- Independent computational tasks.
- Known task execution-time estimates.
- Non-preemptive task allocation.
- No task dependencies.
- No cache contention in the basic model.
- No actual hardware scheduling or execution measurements.

Therefore, the results should be interpreted as simulated scheduling outcomes, not real processor benchmarks.

---

## 🔮 Future Enhancements

Potential extensions include:

- Work Stealing Algorithm.
- Work Sharing Algorithm.
- Dynamic Load Balancing.
- Priority-Based Scheduling.
- Processor Affinity-Aware Scheduling.
- NUMA-Aware Scheduling.
- Energy-Aware Scheduling.
- AI-Assisted Predictive Load Balancing.
- Real-Time Processor Monitoring.
- Heterogeneous CPU Core Scheduling.

---

## 🎓 Academic Project Information

**Project:** Multi-Core Processor Load Balancing Simulator

**Degree:** Bachelor of Technology (B.Tech)

**Branch:** Computer Science and Engineering – Artificial Intelligence and Machine Learning

**Project Category:** Operating Systems / Computer Architecture / Python Application Development

**Purpose:** College Internal Assessment

---

## 👨‍💻 Contribution

Contributions and suggestions are welcome.

For improvements or bug reports:

1. Fork the repository.
2. Create a new feature branch.
3. Implement your changes.
4. Test your modifications.
5. Submit a Pull Request.

Please keep the scheduling engine modular and avoid duplicating existing functionality.

---

## 📜 License

A license has not yet been specified for this project. Add an appropriate license file before distributing or reusing the code publicly.

---

## ⭐ Support

If you find this project useful for learning multi-core scheduling, Python development, or operating-system concepts, consider giving the repository a star!

**Built to demonstrate how intelligent task distribution can improve workload balance across multiple processor cores.**
