"""
Performance metrics calculation module for Multi-Core Processor Load Balancing Simulator.
Mathematical framework implementation (Part E).
"""

import math
from typing import List, Dict, Tuple

class PerformanceMetrics:
    """Calculates performance metrics for scheduling algorithms."""
    
    @staticmethod
    def calculate_total_workload(execution_times: List[float]) -> float:
        """
        TOTAL WORKLOAD (T): Sum of all task execution times.
        T = Σ p(i) for i=1 to n
        """
        return sum(execution_times)
    
    @staticmethod
    def calculate_average_core_workload(total_workload: float, cores: int) -> float:
        """
        AVERAGE CORE WORKLOAD: T / m
        """
        if cores <= 0:
            return 0.0
        return total_workload / cores
    
    @staticmethod
    def calculate_makespan(core_workloads: List[float]) -> float:
        """
        MAKESPAN: Maximum W(j)
        """
        if not core_workloads:
            return 0.0
        return max(core_workloads)
    
    @staticmethod
    def calculate_load_imbalance(core_workloads: List[float]) -> float:
        """
        LOAD IMBALANCE: Maximum W(j) - Minimum W(j)
        """
        if not core_workloads:
            return 0.0
        return max(core_workloads) - min(core_workloads)
    
    @staticmethod
    def calculate_utilization(total_workload: float, cores: int, makespan: float) -> float:
        """
        OVERALL PROCESSOR UTILIZATION: [T / (m × Makespan)] × 100
        """
        if cores <= 0 or makespan <= 0:
            return 0.0
        utilization = (total_workload / (cores * makespan)) * 100
        return round(utilization, 2)
    
    @staticmethod
    def calculate_speedup(total_workload: float, makespan: float) -> float:
        """
        SIMULATED SPEEDUP: T / Makespan
        """
        if makespan <= 0:
            return 0.0
        speedup = total_workload / makespan
        return round(speedup, 2)
    
    @staticmethod
    def calculate_standard_deviation(core_workloads: List[float]) -> float:
        """
        Standard deviation of core workloads (useful for analysis).
        """
        if not core_workloads:
            return 0.0
        
        n = len(core_workloads)
        mean = sum(core_workloads) / n
        variance = sum((w - mean) ** 2 for w in core_workloads) / n
        return math.sqrt(variance)
    
    @staticmethod
    def calculate_all_metrics(cores: int, execution_times: List[float], core_workloads: List[float]) -> Dict:
        """
        Calculate all metrics for a scheduling result.
        """
        total_workload = PerformanceMetrics.calculate_total_workload(execution_times)
        avg_workload = PerformanceMetrics.calculate_average_core_workload(total_workload, cores)
        makespan = PerformanceMetrics.calculate_makespan(core_workloads)
        imbalance = PerformanceMetrics.calculate_load_imbalance(core_workloads)
        utilization = PerformanceMetrics.calculate_utilization(total_workload, cores, makespan)
        speedup = PerformanceMetrics.calculate_speedup(total_workload, makespan)
        std_dev = PerformanceMetrics.calculate_standard_deviation(core_workloads)
        
        return {
            'total_workload': total_workload,
            'average_core_workload': avg_workload,
            'makespan': makespan,
            'load_imbalance': imbalance,
            'utilization': utilization,
            'speedup': speedup,
            'standard_deviation': std_dev,
            'core_workloads': core_workloads
        }


def verify_reference_values():
    """
    Verify the reference example from Part D Section 10:
    Cores: 4, Tasks: 8, Times: [10, 8, 6, 4, 2, 12, 5, 3]
    Total workload = 50, Average = 12.5
    """
    cores = 4
    execution_times = [10, 8, 6, 4, 2, 12, 5, 3]
    total = PerformanceMetrics.calculate_total_workload(execution_times)
    avg = PerformanceMetrics.calculate_average_core_workload(total, cores)
    
    print(f"Total workload: {total} (Expected: 50)")
    print(f"Average workload: {avg} (Expected: 12.5)")
    
    return total == 50 and avg == 12.5


if __name__ == "__main__":
    verify_reference_values()
