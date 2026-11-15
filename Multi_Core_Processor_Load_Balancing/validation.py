"""
Input validation and error handling module for Multi-Core Processor Load Balancing Simulator.
"""

from typing import List, Tuple, Union, Optional

class InputValidator:
    """Handles validation of user inputs for the simulator."""
    
    @staticmethod
    def validate_cores(cores: Union[int, str]) -> int:
        """
        Validate number of CPU cores.
        
        Args:
            cores: Number of cores (int or string)
            
        Returns:
            int: Validated number of cores
            
        Raises:
            ValueError: If cores are invalid (<= 0, non-numeric, etc.)
        """
        try:
            cores_int = int(cores)
        except (ValueError, TypeError):
            raise ValueError("Number of cores must be a positive integer.")
        
        if cores_int <= 0:
            raise ValueError("Number of cores must be greater than 0.")
        
        return cores_int
    
    @staticmethod
    def validate_tasks(tasks: Union[int, str]) -> int:
        """
        Validate number of tasks.
        
        Args:
            tasks: Number of tasks (int or string)
            
        Returns:
            int: Validated number of tasks
            
        Raises:
            ValueError: If tasks are invalid (<= 0, non-numeric, etc.)
        """
        try:
            tasks_int = int(tasks)
        except (ValueError, TypeError):
            raise ValueError("Number of tasks must be a positive integer.")
        
        if tasks_int <= 0:
            raise ValueError("Number of tasks must be greater than 0.")
        
        return tasks_int
    
    @staticmethod
    def validate_execution_times(times_input: Union[str, List[float]]) -> List[float]:
        """
        Validate task execution times.
        
        Args:
            times_input: Comma-separated string or list of execution times
            
        Returns:
            List[float]: Validated execution times
            
        Raises:
            ValueError: If times are invalid (negative, non-numeric, empty)
        """
        if isinstance(times_input, str):
            # Parse comma-separated string
            times_str = times_input.split(',')
            times = []
            for t in times_str:
                t_clean = t.strip()
                if not t_clean:
                    continue
                try:
                    time_val = float(t_clean)
                except ValueError:
                    raise ValueError(f"Invalid execution time: '{t_clean}'. Must be numeric.")
                
                if time_val < 0:
                    raise ValueError(f"Execution time cannot be negative: {time_val}")
                
                times.append(time_val)
        else:
            # Already a list
            times = []
            for t in times_input:
                try:
                    time_val = float(t)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid execution time: {t}. Must be numeric.")
                
                if time_val < 0:
                    raise ValueError(f"Execution time cannot be negative: {time_val}")
                
                times.append(time_val)
        
        if not times:
            raise ValueError("At least one task execution time is required.")
        
        return times
    
    @staticmethod
    def validate_consistency(cores: int, tasks: int, execution_times: List[float]) -> Tuple[int, int, List[float]]:
        """
        Validate consistency between cores, tasks, and execution times.
        
        Args:
            cores: Number of cores
            tasks: Number of tasks
            execution_times: List of execution times
            
        Returns:
            Tuple: (cores, tasks, execution_times) if valid
            
        Raises:
            ValueError: If inconsistent
        """
        if len(execution_times) != tasks:
            raise ValueError(f"Number of execution times ({len(execution_times)}) "
                             f"does not match number of tasks ({tasks}).")
        
        if cores <= 0:
            raise ValueError("Number of cores must be positive.")
        
        if tasks <= 0:
            raise ValueError("Number of tasks must be positive.")
        
        return cores, tasks, execution_times
    
    @staticmethod
    def validate_float_times(times: List[float]) -> List[float]:
        """Validate that all times are floats (handles TC13)."""
        return [float(t) for t in times]


def validate_all(cores_input, tasks_input, times_input) -> Tuple[int, int, List[float]]:
    """
    Comprehensive validation for all inputs.
    
    Returns:
        Tuple[int, int, List[float]]: (cores, tasks, execution_times)
    """
    validator = InputValidator()
    
    cores = validator.validate_cores(cores_input)
    tasks = validator.validate_tasks(tasks_input)
    times = validator.validate_execution_times(times_input)
    
    return validator.validate_consistency(cores, tasks, times)
