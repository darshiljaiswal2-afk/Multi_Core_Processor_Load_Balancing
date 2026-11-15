"""
Visualization module for Multi-Core Processor Load Balancing Simulator.
Generates charts and diagrams for workload comparison and algorithm analysis.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Dict, List

class Visualizer:
    """Handles generation of visualizations and charts."""
    
    @staticmethod
    def create_workload_comparison_chart(results: Dict, output_path: str, cores: int, execution_times: List[float]):
        """
        Create comparison chart of workloads across three algorithms.
        
        Args:
            results: Dictionary with algorithm results
            output_path: Path to save the image
            cores: Number of cores
            execution_times: Original execution times
        """
        algorithms = ['Round Robin', 'Greedy', 'LPT']
        makespans = [
            max(results['round_robin']['workloads']),
            max(results['greedy']['workloads']),
            max(results['lpt']['workloads'])
        ]
        
        imbalances = [
            max(results['round_robin']['workloads']) - min(results['round_robin']['workloads']),
            max(results['greedy']['workloads']) - min(results['greedy']['workloads']),
            max(results['lpt']['workloads']) - min(results['lpt']['workloads'])
        ]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Subplot 1: Workload distribution per core
        core_indices = [f'Core {i+1}' for i in range(cores)]
        
        x = range(len(core_indices))
        width = 0.25
        
        ax1.bar([i - width for i in x], results['round_robin']['workloads'], width, label='Round Robin', alpha=0.8)
        ax1.bar(x, results['greedy']['workloads'], width, label='Greedy', alpha=0.8)
        ax1.bar([i + width for i in x], results['lpt']['workloads'], width, label='LPT', alpha=0.8)
        
        ax1.set_xlabel('CPU Cores')
        ax1.set_ylabel('Workload (Execution Time)')
        ax1.set_title('Core-wise Workload Distribution Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(core_indices)
        ax1.legend()
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Subplot 2: Performance metrics comparison
        metrics = ['Makespan', 'Load Imbalance']
        rr_metrics = [makespans[0], imbalances[0]]
        greedy_metrics = [makespans[1], imbalances[1]]
        lpt_metrics = [makespans[2], imbalances[2]]
        
        x2 = range(len(metrics))
        width2 = 0.25
        
        ax2.bar([i - width2 for i in x2], rr_metrics, width2, label='Round Robin', alpha=0.8)
        ax2.bar(x2, greedy_metrics, width2, label='Greedy', alpha=0.8)
        ax2.bar([i + width2 for i in x2], lpt_metrics, width2, label='LPT', alpha=0.8)
        
        ax2.set_xlabel('Performance Metrics')
        ax2.set_ylabel('Values')
        ax2.set_title('Algorithm Performance Comparison')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(metrics)
        ax2.legend()
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Workload comparison chart saved to: {output_path}")
    
    @staticmethod
    def export_results_to_csv(results: Dict, execution_times: List[float], cores: int, output_path: str):
        """
        Export results to CSV format.
        """
        data = []
        
        # Add original tasks
        for idx, time in enumerate(execution_times):
            data.append({
                'Algorithm': 'Original Tasks',
                'Core': 'N/A',
                'Task_ID': idx,
                'Execution_Time': time,
                'Assigned_Core': 'N/A',
                'Total_Core_Workload': 'N/A'
            })
        
        # Add algorithm results
        for algo_name, algo_data in results.items():
            workloads = algo_data['workloads']
            assignments = algo_data['assignments']
            
            for core_idx, core_workload in enumerate(workloads):
                for task_idx in assignments[core_idx]:
                    data.append({
                        'Algorithm': algo_name.capitalize(),
                        'Core': f'Core {core_idx + 1}',
                        'Task_ID': task_idx,
                        'Execution_Time': execution_times[task_idx],
                        'Assigned_Core': f'Core {core_idx + 1}',
                        'Total_Core_Workload': core_workload
                    })
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Results exported to CSV: {output_path}")


def generate_sample_diagrams(output_dir: str):
    """
    Generate sample diagrams for the project documentation (Part G).
    Note: These are programmatic representations. In a real scenario, 
    we'd use Graphviz or Mermaid for flowcharts, but here we use Matplotlib
    for consistency.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. System Architecture Diagram (simplified)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Flow boxes
    boxes = [
        ('USER INPUT', 0.5, 0.9),
        ('INPUT VALIDATION', 0.5, 0.8),
        ('TASK CREATION', 0.5, 0.7),
        ('SCHEDULING ENGINE', 0.5, 0.6),
        ('ROUND ROBIN / LEAST LOADED / LPT', 0.5, 0.5),
        ('MULTI-CORE WORKLOAD DISTRIBUTION', 0.5, 0.4),
        ('PERFORMANCE METRICS ENGINE', 0.5, 0.3),
        ('ALGORITHM COMPARISON', 0.5, 0.2),
        ('VISUALIZATION AND CSV EXPORT', 0.5, 0.1),
        ('FINAL RESULTS', 0.5, 0.0)
    ]
    
    for text, x, y in boxes:
        ax.text(x, y, text, ha='center', va='center', 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='black'),
                fontsize=9, fontweight='bold')
        if y > 0:
            ax.annotate('', xy=(x, y-0.08), xytext=(x, y-0.02),
                        arrowprops=dict(arrowstyle='->', color='black'))
    
    plt.title('System Architecture Flow', fontsize=14)
    plt.savefig(os.path.join(output_dir, 'system_architecture.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"System architecture diagram saved to: {os.path.join(output_dir, 'system_architecture.png')}")
    
    # Note: Other flowcharts (RR, Greedy, LPT, Overall) would be generated similarly
    # For brevity in this initial setup, we'll focus on the core functionality first


if __name__ == "__main__":
    # Test visualization
    sample_results = {
        'round_robin': {'workloads': [12, 20, 11, 7], 'assignments': [[0, 4], [1, 5], [2, 6], [3, 7]]},
        'greedy': {'workloads': [10, 11, 18, 11], 'assignments': [[0, 7], [1, 6], [2, 5], [3, 4]]},
        'lpt': {'workloads': [12, 13, 12, 13], 'assignments': [[5, 2], [1, 6], [0, 7], [3, 4]]}
    }
    
    Visualizer.create_workload_comparison_chart(
        sample_results, 
        'Multi_Core_Processor_Load_Balancing/output/workload_comparison.png',
        4,
        [10, 8, 6, 4, 2, 12, 5, 3]
    )
    
    Visualizer.export_results_to_csv(
        sample_results,
        [10, 8, 6, 4, 2, 12, 5, 3],
        4,
        'Multi_Core_Processor_Load_Balancing/output/results.csv'
    )
    
    generate_sample_diagrams('Multi_Core_Processor_Load_Balancing/diagrams')
