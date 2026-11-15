"""
Main application entry point for Multi-Core Processor Load Balancing Simulator.
Part F: Advanced Software Quality - Clean CLI implementation.
"""

import sys
import os
from typing import List
from validation import InputValidator, validate_all
from scheduler import Scheduler
from metrics import PerformanceMetrics
from visualization import Visualizer

class LoadBalancingSimulator:
    """Main simulator class coordinating all components."""
    
    def __init__(self):
        self.validator = InputValidator()
        self.scheduler = Scheduler()
        self.metrics = PerformanceMetrics()
        self.visualizer = Visualizer()
    
    def display_welcome(self):
        """Display welcome screen and project description."""
        print("=" * 70)
        print(" MULTI-CORE PROCESSOR LOAD BALANCING SIMULATOR ")
        print(" Design and Implementation of an Intelligent Multi-Core ")
        print(" Workload Distribution and Scheduling Simulator ")
        print("=" * 70)
        print("\nProject Description:")
        print("Educational simulator demonstrating workload distribution among")
        print("multiple CPU cores using Round Robin, Greedy Least Loaded Core,")
        print("and Longest Processing Time First (LPT) scheduling strategies.")
        print("\n" + "=" * 70 + "\n")
    
    def get_user_input(self) -> tuple:
        """Get and validate user input."""
        print("--- INPUT INSTRUCTIONS ---")
        print("1. Enter number of CPU cores (e.g., 4)")
        print("2. Enter number of tasks (e.g., 8)")
        print("3. Enter execution times separated by commas (e.g., 10, 8, 6, 4, 2, 12, 5, 3)")
        print("--------------------------\n")
        
        while True:
            try:
                cores_input = input("Number of CPU cores: ").strip()
                tasks_input = input("Number of tasks: ").strip()
                times_input = input("Execution times (comma-separated): ").strip()
                
                # Validate all inputs
                cores, tasks, execution_times = validate_all(cores_input, tasks_input, times_input)
                
                if len(execution_times) != tasks:
                    print(f"Error: Expected {tasks} execution times, got {len(execution_times)}")
                    continue
                
                return cores, tasks, execution_times
                
            except ValueError as e:
                print(f"Validation Error: {e}")
                print("Please try again.\n")
            except KeyboardInterrupt:
                print("\nSimulation cancelled by user.")
                sys.exit(0)
    
    def run_simulation(self, cores: int, tasks: int, execution_times: List[float]):
        """Execute the simulation and display results."""
        print("\n" + "=" * 70)
        print(" SIMULATION EXECUTION ")
        print("=" * 70)
        
        # Run algorithms
        results = self.scheduler.run_all_algorithms(cores, execution_times)
        
        # Calculate metrics for each algorithm
        total_workload = self.metrics.calculate_total_workload(execution_times)
        avg_workload = self.metrics.calculate_average_core_workload(total_workload, cores)
        
        print(f"\nINPUT SUMMARY:")
        print(f"  Cores: {cores}")
        print(f"  Tasks: {tasks}")
        print(f"  Execution Times: {execution_times}")
        print(f"  Total Workload (T): {total_workload}")
        print(f"  Average Core Workload (T/m): {avg_workload:.2f}")
        print("-" * 70)
        
        algorithm_names = {
            'round_robin': 'Round Robin',
            'greedy': 'Greedy Least Loaded Core',
            'lpt': 'Longest Processing Time First (LPT)'
        }
        
        best_makespan = float('inf')
        best_algo = ""
        
        for algo_key, algo_name in algorithm_names.items():
            algo_data = results[algo_key]
            workloads = algo_data['workloads']
            assignments = algo_data['assignments']
            
            metrics = self.metrics.calculate_all_metrics(cores, execution_times, workloads)
            
            print(f"\n{algo_name.upper()}:")
            print(f"  Core Workloads: {[round(w, 2) for w in workloads]}")
            print(f"  Task Assignments: {assignments}")
            print(f"  Makespan: {metrics['makespan']}")
            print(f"  Load Imbalance: {metrics['load_imbalance']}")
            print(f"  Utilization: {metrics['utilization']:.2f}%")
            print(f"  Speedup: {metrics['speedup']}")
            print(f"  Standard Deviation: {metrics['standard_deviation']:.2f}")
            
            if metrics['makespan'] < best_makespan:
                best_makespan = metrics['makespan']
                best_algo = algo_name
        
        print("\n" + "=" * 70)
        print(f" BEST OBSERVED RESULT: {best_algo.upper()} (Makespan: {best_makespan})")
        print("=" * 70 + "\n")
        
        # Generate visualizations and exports
        output_dir = "Multi_Core_Processor_Load_Balancing/output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create comparison chart
        chart_path = os.path.join(output_dir, "workload_comparison.png")
        self.visualizer.create_workload_comparison_chart(results, chart_path, cores, execution_times)
        
        # Export CSV
        csv_path = os.path.join(output_dir, "results.csv")
        self.visualizer.export_results_to_csv(results, execution_times, cores, csv_path)
        
        print(f"\nOutputs generated:")
        print(f"  - Chart: {chart_path}")
        print(f"  - CSV: {csv_path}")
        
        return results
    
    def run(self):
        """Main application loop."""
        self.display_welcome()
        
        # Option to run reference example or custom input
        choice = input("Run reference example (4 cores, 8 tasks: 10,8,6,4,2,12,5,3) or custom? (r/c): ").strip().lower()
        
        if choice == 'r':
            cores, tasks, execution_times = 4, 8, [10, 8, 6, 4, 2, 12, 5, 3]
            print(f"\nRunning reference example: {cores} cores, {tasks} tasks, times: {execution_times}")
        else:
            cores, tasks, execution_times = self.get_user_input()
        
        self.run_simulation(cores, tasks, execution_times)
        
        print("\nSimulation completed successfully!")


if __name__ == "__main__":
    simulator = LoadBalancingSimulator()
    simulator.run()
