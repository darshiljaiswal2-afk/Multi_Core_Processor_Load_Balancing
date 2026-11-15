"""
Advanced Streamlit Web Application for Multi-Core Processor Load Balancing Simulator.
Part of the mandatory engineering project requirements.
Uses existing scheduling engine (scheduler.py, metrics.py, validation.py, visualization.py).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Tuple
import io
import random
import os
import sys
# Import existing modules from the project
sys.path.insert(0, os.path.dirname(__file__))
from validation import InputValidator, validate_all
from scheduler import Scheduler
from metrics import PerformanceMetrics
from visualization import Visualizer

# Page configuration
st.set_page_config(
    page_title="Multi-Core Processor Load Balancing Simulator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional engineering dashboard
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
    }
    .sidebar .sidebar-content {
        background-color: #161b22;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #58a6ff;
        margin-bottom: 10px;
    }
    .header-subtitle {
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 20px;
    }
    .algorithm-card {
        background-color: #1e2130;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #58a6ff;
        margin-bottom: 15px;
    }
    .insight-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'results' not in st.session_state:
    st.session_state.results = None
if 'inputs' not in st.session_state:
    st.session_state.inputs = None

# --- SIDEBAR: PROFESSIONAL ENGINEERING DASHBOARD ---
st.sidebar.title("⚙️ Project Control")
st.sidebar.markdown("### Multi-Core Processor Load Balancing")
st.sidebar.markdown("Engineering Simulator Dashboard")

st.sidebar.divider()

# Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Algorithm Comparison", "Technical Insights", "Documentation"]
)

# Algorithm Selection
algorithm_choice = st.sidebar.selectbox(
    "Scheduling Algorithm",
    ["Round Robin", "Greedy Least Loaded Core", "Longest Processing Time First (LPT)", "Compare All Three"],
    index=3
)

# Input Configuration
st.sidebar.subheader("Input Configuration")
cores_input = st.sidebar.number_input("Number of CPU Cores", min_value=1, max_value=64, value=4)
tasks_input = st.sidebar.number_input("Number of Tasks", min_value=1, max_value=1000, value=8)

# Input Method Selection
input_method = st.sidebar.radio(
    "Task Input Method",
    ["Manual Entry", "Random Generation", "CSV Import", "Predefined Demo"]
)

# Execution Controls
if st.sidebar.button("🚀 Run Simulation", type="primary"):
    st.session_state.execute = True
else:
    st.session_state.execute = False

if st.sidebar.button("🔄 Reset"):
    st.session_state.results = None
    st.session_state.inputs = None
    st.session_state.execute = False
    st.rerun()

st.sidebar.divider()
st.sidebar.info("💡 **Engineering Note:** This dashboard uses the same scheduling engine as the CLI application. Results are mathematically verified.")

# --- MAIN DASHBOARD ---

# Header
st.markdown("<h1 class='header-title'>MULTI-CORE PROCESSOR LOAD BALANCING</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='header-subtitle'>Intelligent Workload Distribution and Scheduling Simulator</h3>", unsafe_allow_html=True)
st.markdown("""
**Project Description:** Educational engineering simulator demonstrating how independent computational tasks 
are distributed among multiple CPU cores using Round Robin, Greedy Least Loaded Core, and LPT scheduling strategies.
""")

st.divider()

# Input Handling
if st.session_state.execute or (menu == "Dashboard" and st.session_state.inputs is not None):
    
    # Get task execution times based on input method
    execution_times = []
    
    if input_method == "Manual Entry":
        st.subheader("Manual Task Entry")
        times_input = st.text_input("Enter execution times (comma-separated)", "10, 8, 6, 4, 2, 12, 5, 3")
        try:
            execution_times = InputValidator.validate_execution_times(times_input)
        except ValueError as e:
            st.error(f"Validation Error: {e}")
            st.stop()
            
    elif input_method == "Random Generation":
        st.subheader("Random Task Generation")
        min_time = st.slider("Minimum execution time", 1, 50, 1)
        max_time = st.slider("Maximum execution time", 1, 100, 20)
        execution_times = [random.uniform(min_time, max_time) for _ in range(tasks_input)]
        st.write(f"Generated {tasks_input} tasks: {[round(t, 2) for t in execution_times]}")
        
    elif input_method == "CSV Import":
        st.subheader("CSV Task Import")
        uploaded_file = st.file_uploader("Upload CSV with execution times (one column)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            try:
                # Extract first column as execution times
                execution_times = df.iloc[:, 0].dropna().astype(float).tolist()
                st.write(f"Imported {len(execution_times)} tasks from CSV")
            except Exception as e:
                st.error(f"CSV Import Error: {e}")
                st.stop()
        else:
            st.warning("Please upload a CSV file")
            st.stop()
            
    elif input_method == "Predefined Demo":
        st.subheader("Predefined Demonstration Datasets")
        demo_choice = st.selectbox("Select Demo", ["Reference Example (8 tasks)", "Large Scale (50 tasks)", "Unequal Distribution (10 tasks)"])
        
        if demo_choice == "Reference Example (8 tasks)":
            execution_times = [10, 8, 6, 4, 2, 12, 5, 3]
            tasks_input = 8
        elif demo_choice == "Large Scale (50 tasks)":
            execution_times = [random.uniform(1, 20) for _ in range(50)]
            tasks_input = 50
        elif demo_choice == "Unequal Distribution (10 tasks)":
            execution_times = [20, 1, 15, 2, 18, 3, 12, 4, 10, 5]
            tasks_input = 10

    # Validate inputs
    try:
        validator = InputValidator()
        cores, tasks, validated_times = validator.validate_consistency(cores_input, tasks_input, execution_times)
        st.session_state.inputs = {
            'cores': cores,
            'tasks': tasks,
            'times': validated_times
        }
    except ValueError as e:
        st.error(f"Input Validation Error: {e}")
        st.stop()

    # Execute scheduling
    scheduler = Scheduler()
    results = scheduler.run_all_algorithms(cores, validated_times)
    st.session_state.results = results
    
    # Calculate metrics for each algorithm
    metrics_engine = PerformanceMetrics()
    total_workload = metrics_engine.calculate_total_workload(validated_times)
    avg_workload = metrics_engine.calculate_average_core_workload(total_workload, cores)
    
    algorithm_metrics = {}
    for algo_key, algo_data in results.items():
        algorithm_metrics[algo_key] = metrics_engine.calculate_all_metrics(
            cores, validated_times, algo_data['workloads']
        )

# --- MAIN CONTENT ---

if menu == "Dashboard":
    if st.session_state.results is None:
        st.info("Please configure inputs in the sidebar and click 'Run Simulation' to begin.")
    else:
        # Performance Overview Cards
        st.subheader("📊 Performance Overview")
        
        cols = st.columns(8)
        metrics_data = algorithm_metrics.get(algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", ""), {})
        
        # Use first algorithm if comparing all (show reference values)
        if algorithm_choice == "Compare All Three":
            # Show aggregate/reference values
            total_workload = sum(st.session_state.inputs['times'])
            avg_workload = total_workload / st.session_state.inputs['cores']
            
            with cols[0]: st.metric("CPU Cores", st.session_state.inputs['cores'])
            with cols[1]: st.metric("Total Tasks", st.session_state.inputs['tasks'])
            with cols[2]: st.metric("Total Workload", f"{total_workload:.2f}")
            with cols[3]: st.metric("Avg Core Workload", f"{avg_workload:.2f}")
            with cols[4]: st.metric("Makespan", "See Comparison")
            with cols[5]: st.metric("Utilization", "See Comparison")
            with cols[6]: st.metric("Imbalance", "See Comparison")
            with cols[7]: st.metric("Speedup", "See Comparison")
        else:
            algo_key = algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", "")
            m = algorithm_metrics[algo_key]
            
            with cols[0]: st.metric("CPU Cores", st.session_state.inputs['cores'])
            with cols[1]: st.metric("Total Tasks", st.session_state.inputs['tasks'])
            with cols[2]: st.metric("Total Workload", f"{m['total_workload']:.2f}")
            with cols[3]: st.metric("Avg Core Workload", f"{m['average_core_workload']:.2f}")
            with cols[4]: st.metric("Makespan", f"{m['makespan']:.2f}")
            with cols[5]: st.metric("Utilization", f"{m['utilization']:.2f}%")
            with cols[6]: st.metric("Imbalance", f"{m['load_imbalance']:.2f}")
            with cols[7]: st.metric("Speedup", f"{m['speedup']:.2f}")

        st.divider()

        # Task Input Panel
        st.subheader("📋 Task Input Panel")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**Cores:** {st.session_state.inputs['cores']}")
            st.write(f"**Tasks:** {st.session_state.inputs['tasks']}")
            st.write(f"**Execution Times:** {[round(t, 2) for t in st.session_state.inputs['times']]}")
        with col2:
            st.dataframe(pd.DataFrame({
                "Task ID": range(len(st.session_state.inputs['times'])),
                "Execution Time": [round(t, 2) for t in st.session_state.inputs['times']]
            }))

        st.divider()

        # Algorithm Comparison & Results
        if algorithm_choice == "Compare All Three":
            st.subheader("⚖️ Algorithm Comparison")
            
            tabs = st.tabs(["Round Robin", "Greedy Least Loaded", "LPT", "Comparison Summary"])
            
            algorithms = ['round_robin', 'greedy', 'lpt']
            names = ['Round Robin', 'Greedy Least Loaded Core', 'Longest Processing Time First (LPT)']
            
            for i, (algo_key, name) in enumerate(zip(algorithms, names)):
                with tabs[i]:
                    algo_data = results[algo_key]
                    m = algorithm_metrics[algo_key]
                    
                    st.write(f"### {name}")
                    st.write(f"**Workloads:** {[round(w, 2) for w in algo_data['workloads']]}")
                    st.write(f"**Makespan:** {m['makespan']:.2f}")
                    st.write(f"**Load Imbalance:** {m['load_imbalance']:.2f}")
                    st.write(f"**Utilization:** {m['utilization']:.2f}%")
                    st.write(f"**Speedup:** {m['speedup']:.2f}")
                    
                    # Core assignments table
                    df_assignments = pd.DataFrame({
                        "Core ID": [f"Core {i+1}" for i in range(cores)],
                        "Assigned Tasks": [str(algo_data['assignments'][i]) for i in range(cores)],
                        "Total Workload": [round(w, 2) for w in algo_data['workloads']]
                    })
                    st.dataframe(df_assignments, use_container_width=True)
            
            # Comparison Summary Tab
            with tabs[3]:
                st.subheader("Comparative Analysis")
                comp_data = []
                for algo_key, name in zip(algorithms, names):
                    m = algorithm_metrics[algo_key]
                    comp_data.append({
                        "Algorithm": name,
                        "Makespan": m['makespan'],
                        "Imbalance": m['load_imbalance'],
                        "Utilization (%)": round(m['utilization'], 2),
                        "Speedup": round(m['speedup'], 2)
                    })
                
                df_comp = pd.DataFrame(comp_data)
                st.dataframe(df_comp, use_container_width=True)
                
                # Best result identification
                best_algo = df_comp.loc[df_comp['Makespan'].idxmin(), 'Algorithm']
                st.success(f"🏆 **Best Observed Result:** {best_algo} (Lowest Makespan: {df_comp['Makespan'].min()})")
                
        else:
            # Single algorithm view
            algo_key = algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", "")
            algo_data = results[algo_key]
            m = algorithm_metrics[algo_key]
            
            st.subheader(f"📊 {algorithm_choice} Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Workloads:** {[round(w, 2) for w in algo_data['workloads']]}")
                st.write(f"**Makespan:** {m['makespan']:.2f}")
                st.write(f"**Load Imbalance:** {m['load_imbalance']:.2f}")
            with col2:
                st.write(f"**Utilization:** {m['utilization']:.2f}%")
                st.write(f"**Speedup:** {m['speedup']:.2f}")
                st.write(f"**Standard Deviation:** {m['standard_deviation']:.2f}")
            
            # Core assignments table
            st.subheader("📋 Core Assignments")
            df_assignments = pd.DataFrame({
                "Core ID": [f"Core {i+1}" for i in range(cores)],
                "Assigned Tasks": [str(algo_data['assignments'][i]) for i in range(cores)],
                "Total Workload": [round(w, 2) for w in algo_data['workloads']]
            })
            st.dataframe(df_assignments, use_container_width=True)

        st.divider()

        # Interactive Workload Visualization
        st.subheader("📈 Interactive Workload Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Core-wise workload bar chart
            fig1 = go.Figure()
            
            if algorithm_choice == "Compare All Three":
                for algo_key, name in zip(algorithms, names):
                    algo_data = results[algo_key]
                    fig1.add_trace(go.Bar(
                        x=[f"Core {i+1}" for i in range(cores)],
                        y=algo_data['workloads'],
                        name=name,
                        opacity=0.8
                    ))
                fig1.update_layout(
                    title="Core-wise Workload Comparison",
                    xaxis_title="CPU Cores",
                    yaxis_title="Workload (Execution Time)",
                    barmode="group",
                    template="plotly_dark"
                )
            else:
                fig1.add_trace(go.Bar(
                    x=[f"Core {i+1}" for i in range(cores)],
                    y=algo_data['workloads'],
                    marker_color="#58a6ff"
                ))
                fig1.update_layout(
                    title=f"{algorithm_choice} Workload Distribution",
                    xaxis_title="CPU Cores",
                    yaxis_title="Workload (Execution Time)",
                    template="plotly_dark"
                )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Task distribution visualization
            fig2 = go.Figure()
            
            if algorithm_choice == "Compare All Three":
                for algo_key, name in zip(algorithms, names):
                    algo_data = results[algo_key]
                    # Flatten assignments for visualization
                    all_tasks = []
                    core_labels = []
                    for core_idx, assignments in enumerate(algo_data['assignments']):
                        for task_idx in assignments:
                            all_tasks.append(st.session_state.inputs['times'][task_idx])
                            core_labels.append(f"Core {core_idx+1}")
                    
                    fig2.add_trace(go.Scatter(
                        x=core_labels,
                        y=all_tasks,
                        mode='markers',
                        name=name,
                        marker=dict(size=10, opacity=0.8)
                    ))
                
                fig2.update_layout(
                    title="Task Distribution Across Cores",
                    xaxis_title="CPU Cores",
                    yaxis_title="Task Execution Time",
                    template="plotly_dark"
                )
            else:
                all_tasks = []
                core_labels = []
                for core_idx, assignments in enumerate(algo_data['assignments']):
                    for task_idx in assignments:
                        all_tasks.append(st.session_state.inputs['times'][task_idx])
                        core_labels.append(f"Core {core_idx+1}")
                
                fig2.add_trace(go.Scatter(
                    x=core_labels,
                    y=all_tasks,
                    mode='markers',
                    marker=dict(size=12, color="#58a6ff", opacity=0.9)
                ))
                
                fig2.update_layout(
                    title=f"{algorithm_choice} Task Distribution",
                    xaxis_title="CPU Cores",
                    yaxis_title="Task Execution Time",
                    template="plotly_dark"
                )
            
            st.plotly_chart(fig2, use_container_width=True)

        # Detailed Results Table & Download
        st.subheader("📋 Detailed Results")
        if algorithm_choice == "Compare All Three":
            # Create combined results table
            combined_data = []
            for algo_key, name in zip(algorithms, names):
                algo_data = results[algo_key]
                for core_idx, assignments in enumerate(algo_data['assignments']):
                    for task_idx in assignments:
                        combined_data.append({
                            "Algorithm": name,
                            "Core ID": f"Core {core_idx+1}",
                            "Task ID": task_idx,
                            "Execution Time": st.session_state.inputs['times'][task_idx],
                            "Total Core Workload": round(algo_data['workloads'][core_idx], 2)
                        })
            df_combined = pd.DataFrame(combined_data)
            st.dataframe(df_combined, use_container_width=True)
            
            csv_data = df_combined.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Comparison CSV",
                data=csv_data,
                file_name="multi_core_comparison_results.csv",
                mime="text/csv"
            )
        else:
            algo_data = results[algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", "")]
            df_assignments = pd.DataFrame({
                "Core ID": [f"Core {i+1}" for i in range(cores)],
                "Assigned Tasks": [str(algo_data['assignments'][i]) for i in range(cores)],
                "Total Workload": [round(w, 2) for w in algo_data['workloads']]
            })
            st.dataframe(df_assignments, use_container_width=True)
            
            csv_data = df_assignments.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {algorithm_choice} Results CSV",
                data=csv_data,
                file_name=f"{algorithm_choice.lower().replace(' ', '_')}_results.csv",
                mime="text/csv"
            )

        # Algorithm Explanation Panel
        st.subheader("📖 Algorithm Explanation")
        with st.expander("Click to view algorithm details"):
            if algorithm_choice == "Round Robin":
                st.markdown("""
                **Definition:** Assign each incoming task to successive cores in cyclic order (task allocation without time quantum).
                
                **How it works:** Tasks are distributed sequentially across cores in a round-robin fashion, wrapping around when reaching the last core.
                
                **Assignment Logic:** Task i → Core (i-1) mod m
                
                **Advantages:** Simple implementation, predictable distribution, low overhead
                **Limitations:** Ignores task duration differences, may cause imbalance with unequal times
                **Time Complexity:** O(n) where n = number of tasks
                **Space Complexity:** O(m) where m = number of cores
                """)
            elif algorithm_choice == "Greedy Least Loaded Core":
                st.markdown("""
                **Definition:** Assign each next task to the core with the minimum accumulated workload, updating workload after each assignment.
                
                **How it works:** For each task, identify the core with the lowest current workload and assign the task to that core.
                
                **Assignment Logic:** Task i → Core with minimum current workload
                
                **Advantages:** Better balance than Round Robin, adaptive to task durations
                **Limitations:** Greedy approach may not find global optimum, O(n×m) complexity
                **Time Complexity:** O(n × m) where n = tasks, m = cores
                **Space Complexity:** O(m)
                """)
            elif algorithm_choice == "Longest Processing Time First (LPT)":
                st.markdown("""
                **Definition:** Sort tasks by decreasing execution time and assign each task to the currently least-loaded core.
                
                **How it works:** Sort tasks descending, then greedily assign each to the least loaded core. Deterministic tie-breaking: equal durations retain original order, equal workloads select lowest core ID.
                
                **Assignment Logic:** Sorted tasks → Core with minimum current workload
                
                **Advantages:** Best theoretical performance, minimizes makespan
                **Limitations:** Sorting overhead, requires knowledge of all task times upfront
                **Time Complexity:** O(n log n + n × m)
                **Space Complexity:** O(n + m)
                """)
            else:
                st.markdown("""
                **Round Robin:** Cyclic assignment without time quantum. Simple but inefficient with unequal task times.
                
                **Greedy Least Loaded:** Dynamic assignment to minimum workload core. Better balance but suboptimal.
                
                **LPT:** Sort tasks descending, then assign to least loaded core. Optimal theoretical performance.
                """)

        # Technical Insights
        st.subheader("💡 Technical Insights")
        with st.container():
            if algorithm_choice == "Compare All Three":
                comp_data = []
                for algo_key, name in zip(algorithms, names):
                    m = algorithm_metrics[algo_key]
                    comp_data.append({
                        "Algorithm": name,
                        "Makespan": m['makespan'],
                        "Imbalance": m['load_imbalance'],
                        "Utilization (%)": round(m['utilization'], 2),
                        "Speedup": round(m['speedup'], 2)
                    })
                df_comp = pd.DataFrame(comp_data)
                
                best_makespan_algo = df_comp.loc[df_comp['Makespan'].idxmin(), 'Algorithm']
                best_imbalance_algo = df_comp.loc[df_comp['Imbalance'].idxmin(), 'Algorithm']
                
                st.markdown(f"""
                <div class='insight-box'>
                <strong>Best Makespan:</strong> {best_makespan_algo} ({df_comp['Makespan'].min():.2f})<br>
                <strong>Lowest Imbalance:</strong> {best_imbalance_algo} ({df_comp['Imbalance'].min():.2f})<br>
                <strong>Highest Utilization:</strong> {df_comp.loc[df_comp['Utilization (%)'].idxmax(), 'Algorithm']} ({df_comp['Utilization (%)'].max():.2f}%)<br>
                <strong>Best Speedup:</strong> {df_comp.loc[df_comp['Speedup'].idxmax(), 'Algorithm']} ({df_comp['Speedup'].max():.2f})<br>
                </div>
                """, unsafe_allow_html=True)
                
                # Core workload analysis
                all_workloads = []
                for algo_key in algorithms:
                    all_workloads.extend(results[algo_key]['workloads'])
                
                max_core = max(all_workloads)
                min_core = min(all_workloads)
                st.write(f"**Maximum Core Workload Observed:** {max_core:.2f}")
                st.write(f"**Minimum Core Workload Observed:** {min_core:.2f}")
                st.write(f"**Improvement vs Round Robin:** {((df_comp.loc[df_comp['Algorithm'] == 'Round Robin', 'Makespan'].values[0] - df_comp.loc[df_comp['Algorithm'] == 'Longest Processing Time First (LPT)', 'Makespan'].values[0]) / df_comp.loc[df_comp['Algorithm'] == 'Round Robin', 'Makespan'].values[0] * 100):.1f}% reduction in makespan with LPT")
                
            else:
                m = algorithm_metrics[algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", "")]
                algo_data = results[algorithm_choice.lower().replace(" ", "_").replace("(", "").replace(")", "")]
                
                st.markdown(f"""
                <div class='insight-box'>
                <strong>Highest Workload Core:</strong> Core {algo_data['workloads'].index(max(algo_data['workloads'])) + 1} ({max(algo_data['workloads']):.2f})<br>
                <strong>Lowest Workload Core:</strong> Core {algo_data['workloads'].index(min(algo_data['workloads'])) + 1} ({min(algo_data['workloads']):.2f})<br>
                <strong>Makespan:</strong> {m['makespan']:.2f}<br>
                <strong>Utilization:</strong> {m['utilization']:.2f}%<br>
                <strong>Speedup:</strong> {m['speedup']:.2f}<br>
                </div>
                """, unsafe_allow_html=True)

elif menu == "Algorithm Comparison":
    st.subheader("⚖️ Detailed Algorithm Comparison")
    
    if st.session_state.results is None:
        st.info("Please run simulation first to generate comparison data.")
    else:
        algorithms = ['round_robin', 'greedy', 'lpt']
        names = ['Round Robin', 'Greedy Least Loaded Core', 'Longest Processing Time First (LPT)']
        metrics_engine = PerformanceMetrics()
        
        comp_data = []
        for algo_key, name in zip(algorithms, names):
            algo_data = st.session_state.results[algo_key]
            m = metrics_engine.calculate_all_metrics(
                st.session_state.inputs['cores'],
                st.session_state.inputs['times'],
                algo_data['workloads']
            )
            comp_data.append({
                "Algorithm": name,
                "Makespan": m['makespan'],
                "Imbalance": m['load_imbalance'],
                "Utilization (%)": round(m['utilization'], 2),
                "Speedup": round(m['speedup'], 2),
                "Workloads": str([round(w, 2) for w in algo_data['workloads']])
            })
        
        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True)
        
        # Comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            for algo_key, name in zip(algorithms, names):
                algo_data = st.session_state.results[algo_key]
                fig.add_trace(go.Bar(
                    x=[f"Core {i+1}" for i in range(st.session_state.inputs['cores'])],
                    y=algo_data['workloads'],
                    name=name,
                    opacity=0.8
                ))
            fig.update_layout(
                title="Algorithm Workload Comparison",
                xaxis_title="CPU Cores",
                yaxis_title="Workload (Execution Time)",
                barmode="group",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = go.Figure()
            for algo_key, name in zip(algorithms, names):
                m = metrics_engine.calculate_all_metrics(
                    st.session_state.inputs['cores'],
                    st.session_state.inputs['times'],
                    st.session_state.results[algo_key]['workloads']
                )
                fig2.add_trace(go.Bar(
                    x=["Makespan", "Imbalance", "Utilization (%)", "Speedup"],
                    y=[m['makespan'], m['load_imbalance'], m['utilization'], m['speedup']],
                    name=name,
                    opacity=0.8
                ))
            fig2.update_layout(
                title="Performance Metrics Comparison",
                xaxis_title="Metric",
                yaxis_title="Value",
                barmode="group",
                template="plotly_dark"
            )
            st.plotly_chart(fig2, use_container_width=True)

elif menu == "Technical Insights":
    st.subheader("🔍 Advanced Technical Insights")
    
    if st.session_state.results is None:
        st.info("Please run simulation first to generate insights.")
    else:
        algorithms = ['round_robin', 'greedy', 'lpt']
        names = ['Round Robin', 'Greedy Least Loaded Core', 'Longest Processing Time First (LPT)']
        metrics_engine = PerformanceMetrics()
        
        # Generate insights from actual data
        total_workload = sum(st.session_state.inputs['times'])
        avg_workload = total_workload / st.session_state.inputs['cores']
        
        st.markdown(f"**Total Workload (T):** {total_workload:.2f}")
        st.markdown(f"**Average Core Workload (T/m):** {avg_workload:.2f}")
        
        comp_data = []
        for algo_key, name in zip(algorithms, names):
            algo_data = st.session_state.results[algo_key]
            m = metrics_engine.calculate_all_metrics(
                st.session_state.inputs['cores'],
                st.session_state.inputs['times'],
                algo_data['workloads']
            )
            comp_data.append({
                "Algorithm": name,
                "Makespan": m['makespan'],
                "Imbalance": m['load_imbalance'],
                "Utilization (%)": round(m['utilization'], 2),
                "Speedup": round(m['speedup'], 2)
            })
        
        df_comp = pd.DataFrame(comp_data)
        
        # Insight 1: Best algorithm
        best_algo = df_comp.loc[df_comp['Makespan'].idxmin(), 'Algorithm']
        st.success(f"🏆 **Best Observed Result:** {best_algo} achieves the lowest makespan ({df_comp['Makespan'].min():.2f})")
        
        # Insight 2: Core workload analysis
        all_workloads = []
        for algo_key in algorithms:
            all_workloads.extend(st.session_state.results[algo_key]['workloads'])
        
        max_core = max(all_workloads)
        min_core = min(all_workloads)
        st.info(f"📊 **Workload Range:** Highest core workload = {max_core:.2f}, Lowest core workload = {min_core:.2f}")
        
        # Insight 3: Improvement comparison
        rr_makespan = df_comp.loc[df_comp['Algorithm'] == 'Round Robin', 'Makespan'].values[0]
        lpt_makespan = df_comp.loc[df_comp['Algorithm'] == 'Longest Processing Time First (LPT)', 'Makespan'].values[0]
        improvement = ((rr_makespan - lpt_makespan) / rr_makespan) * 100
        st.write(f"**LPT Improvement vs Round Robin:** {improvement:.1f}% reduction in makespan")
        
        # Insight 4: Core utilization analysis
        empty_cores = []
        for algo_key, name in zip(algorithms, names):
            algo_data = st.session_state.results[algo_key]
            zero_cores = sum(1 for w in algo_data['workloads'] if w == 0)
            if zero_cores > 0:
                empty_cores.append(f"{name}: {zero_cores} core(s) idle")
        
        if empty_cores:
            st.warning(f"⚠️ **Idle Cores Detected:** {' | '.join(empty_cores)}")
        else:
            st.success("✅ **All cores utilized** across all algorithms")

elif menu == "Documentation":
    st.subheader("📚 Academic Documentation")
    st.markdown("""
    **Project Title:** MULTI-CORE PROCESSOR LOAD BALANCING  
    **Subtitle:** Design and Implementation of an Intelligent Multi-Core Workload Distribution and Scheduling Simulator Using Python  
    **Degree:** Bachelor of Technology, Computer Science and Engineering (AI/ML)  
    **Academic Year:** 2026-2027  
    
    ### 12 Mandatory Sections Included:
    1. **Project Title** - Cover page information
    2. **Abstract** - Technical summary and objectives
    3. **Problem Statement** - Uneven distribution, objectives
    4. **Existing System** - Limitations table
    5. **Proposed System** - Simulator features and comparison
    6. **System Architecture** - Logical flow and module responsibilities
    7. **Algorithm and Flowchart** - RR, Greedy, LPT definitions and complexity
    8. **Hardware & Software Requirements** - Tables and specifications
    9. **Source Code** - Complete modular implementation
    10. **Sample Input & Output** - Reference example verification
    11. **Testing & Results** - TC01-TC18 automated test suite
    12. **Future Enhancements** - 12 enhancement areas
    
    **References:** IEEE style citations included
    **Source Code Appendix:** Complete implementation referenced
    
    **Final Deliverables:**
    - Multi_Core_Processor_Load_Balancing_Assignment.docx (Generated)
    - Multi_Core_Processor_Load_Balancing_Assignment.md (Fallback)
    - TEST_RESULTS.md (18/18 tests passed)
    - FINAL_QUALITY_AUDIT.md (Completion verification)
    """)
    
    st.info("📄 **Download Academic Report:** [Multi_Core_Processor_Load_Balancing_Assignment.docx](http://documentation/Multi_Core_Processor_Load_Balancing_Assignment.docx)")

# --- FOOTER ---
st.divider()
st.caption("Engineering Project: Multi-Core Processor Load Balancing Simulator | Bachelor of Technology CSE (AI/ML) | Academic Year 2026-2027 | Developed on Arena.ai Agent Mode")
