"""
Scheduling algorithms module for Multi-Core Processor Load Balancing Simulator.
Implements:
1. Round Robin Task Distribution (Algorithm 1)
2. Greedy Least Loaded Core Scheduling (Algorithm 2)
3. Longest Processing Time First (LPT) (Algorithm 3)
"""

from typing import List, Dict, Tuple
import copy

class Scheduler:
    """Implements the three scheduling algorithms."""
    
    @staticmethod
    def round_robin(cores: int, execution_times: List[float]) -> Tuple[List[float], List[List[int]]]:
        """
        Algorithm 1: Round Robin Task Distribution
        Assign each incoming task to successive cores in cyclic order.
        No time quantum (task allocation, not preemptive scheduling).
        
        Args:
            cores: Number of CPU cores
            execution_times: List of task execution times
            
        Returns:
            Tuple: (core_workloads, task_assignments)
        """
        core_workloads = [0.0] * cores
        task_assignments = [[] for _ in range(cores)]
        
        for task_idx, time in enumerate(execution_times):
            core_idx = task_idx % cores
            core_workloads[core_idx] += time
            task_assignments[core_idx].append(task_idx)
        
        return core_workloads, task_assignments
    
    @staticmethod
    def greedy_least_loaded(cores: int, execution_times: List[float]) -> Tuple[List[float], List[List[int]]]:
        """
        Algorithm 2: Greedy Least Loaded Core
        Assign each next task to the core with the minimum accumulated workload.
        Update workload after each assignment.
        
        Args:
            cores: Number of CPU cores
            execution_times: List of task execution times
            
        Returns:
            Tuple: (core_workloads, task_assignments)
        """
        core_workloads = [0.0] * cores
        task_assignments = [[] for _ in range(cores)]
        
        for task_idx, time in enumerate(execution_times):
            # Find core with minimum workload (tie-break: lowest core ID)
            min_workload = min(core_workloads)
            min_core_idx = core_workloads.index(min_workload)
            
            core_workloads[min_core_idx] += time
            task_assignments[min_core_idx].append(task_idx)
        
        return core_workloads, task_assignments
    
    @staticmethod
    def lpt(cores: int, execution_times: List[float]) -> Tuple[List[float], List[List[int]]]:
        """
        Algorithm 3: Longest Processing Time First (LPT)
        Sort tasks by decreasing execution time and assign each task to the currently least-loaded core.
        Deterministic tie-breaking:
        - Equal task durations: retain original task order
        - Equal core workloads: select the lowest core ID
        
        Args:
            cores: Number of CPU cores
            execution_times: List of task execution times
            
        Returns:
            Tuple: (core_workloads, task_assignments)
        """
        # Create task list with original indices for tie-breaking
        tasks = [(time, idx) for idx, time in enumerate(execution_times)]
        
        # Sort by decreasing time, then by original index (stable sort preserves order)
        # Using negative time for descending sort
        sorted_tasks = sorted(tasks, key=lambda x: (-x[0], x[1]))
        
        core_workloads = [0.0] * cores
        task_assignments = [[] for _ in range(cores)]
        
        for time, original_idx in sorted_tasks:
            # Find core with minimum workload (tie-break: lowest core ID)
            min_workload = min(core_workloads)
            min_core_idx = core_workloads.index(min_workload)
            
            core_workloads[min_core_idx] += time
            task_assignments[min_core_idx].append(original_idx)
        
        return core_workloads, task_assignments
    
    @staticmethod
    def run_all_algorithms(cores: int, execution_times: List[float]) -> Dict:
        """
        Run all three algorithms and return results.
        """
        rr_workloads, rr_assignments = Scheduler.round_robin(cores, execution_times)
        greedy_workloads, greedy_assignments = Scheduler.greedy_least_loaded(cores, execution_times)
        lpt_workloads, lpt_assignments = Scheduler.lpt(cores, execution_times)
        
        return {
            'round_robin': {
                'workloads': rr_workloads,
                'assignments': rr_assignments
            },
            'greedy': {
                'workloads': greedy_workloads,
                'assignments': greedy_assignments
            },
            'lpt': {
                'workloads': lpt_workloads,
                'assignments': lpt_assignments
            }
        }


def verify_reference_example():
    """
    Verify reference example from Part D Section 10:
    Cores: 4, Tasks: 8, Times: [10, 8, 6, 4, 2, 12, 5, 3]
    Expected:
    Round Robin: [12, 20, 11, 7], Makespan=20, Imbalance=13, Utilization=62.50%
    Greedy: [10, 11, 18, 11], Makespan=18, Imbalance=8, Utilization=69.44%
    LPT: [12, 13, 12, 13], Makespan=13, Imbalance=1, Utilization=96.15%
    Speedup LPT: ~3.85
    """
    cores = 4
    execution_times = [10, 8, 6, 4, 2, 12, 5, 3]
    
    results = Scheduler.run_all_algorithms(cores, execution_times)
    
    print("=== REFERENCE EXAMPLE VERIFICATION ===")
    print(f"Cores: {cores}, Tasks: {len(execution_times)}, Times: {execution_times}")
    print(f"Total workload: {sum(execution_times)}")
    print()
    
    # Round Robin
    rr = results['round_robin']
    print(f"Round Robin Workloads: {rr['workloads']}")
    print(f"Expected: [12, 20, 11, 7]")
    print(f"Assignments: {rr['assignments']}")
    print()
    
    # Greedy
    greedy = results['greedy']
    print(f"Greedy Workloads: {greedy['workloads']}")
    print(f"Expected: [10, 11, 18, 11]")
    print(f"Assignments: {greedy['assignments']}")
    print()
    
    # LPT
    lpt = results['lpt']
    print(f"LPT Workloads: {lpt['workloads']}")
    print(f"Expected: [12, 13, 12, 13]")
    print(f"Assignments: {lpt['assignments']}")
    print()
    
    return results


if __name__ == "__main__":
    verify_reference_example()
