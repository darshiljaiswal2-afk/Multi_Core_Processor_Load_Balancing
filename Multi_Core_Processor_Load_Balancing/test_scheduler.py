"""
Automated test suite for Multi-Core Processor Load Balancing Simulator.
Part D Section 11: Testing and Results (TC01-TC18).
"""

import unittest
from validation import InputValidator, validate_all
from scheduler import Scheduler
from metrics import PerformanceMetrics

class TestLoadBalancingSimulator(unittest.TestCase):
    """Test suite covering TC01-TC18."""
    
    def setUp(self):
        """Set up test data."""
        self.validator = InputValidator()
        self.scheduler = Scheduler()
        self.metrics = PerformanceMetrics()
    
    # TC01: Normal task allocation
    def test_tc01_normal_allocation(self):
        """TC01: Normal task allocation"""
        cores, tasks, times = 4, 8, [10, 8, 6, 4, 2, 12, 5, 3]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # Verify all algorithms produce results
        self.assertIn('round_robin', results)
        self.assertIn('greedy', results)
        self.assertIn('lpt', results)
        
        # Verify task count preservation
        total_assigned = sum(len(assign) for assign in results['round_robin']['assignments'])
        self.assertEqual(total_assigned, tasks)
    
    # TC02: Single CPU core
    def test_tc02_single_core(self):
        """TC02: Single CPU core"""
        cores, tasks, times = 1, 5, [5, 3, 8, 2, 7]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # All tasks should go to core 0
        self.assertEqual(len(results['round_robin']['assignments'][0]), 5)
        self.assertEqual(sum(results['round_robin']['workloads']), sum(times))
    
    # TC03: More cores than tasks
    def test_tc03_more_cores_than_tasks(self):
        """TC03: More cores than tasks"""
        cores, tasks, times = 8, 3, [10, 5, 8]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # Verify no errors and correct task distribution
        rr_workloads = results['round_robin']['workloads']
        self.assertEqual(sum(rr_workloads), sum(times))
        
        # Some cores should have 0 workload
        zero_cores = sum(1 for w in rr_workloads if w == 0)
        self.assertGreater(zero_cores, 0)
    
    # TC04: Equal task durations
    def test_tc04_equal_durations(self):
        """TC04: Equal task durations"""
        cores, tasks, times = 3, 6, [5, 5, 5, 5, 5, 5]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # Round Robin should distribute evenly
        rr_workloads = results['round_robin']['workloads']
        self.assertEqual(rr_workloads, [10, 10, 10])  # 2 tasks per core
    
    # TC05: Unequal task durations
    def test_tc05_unequal_durations(self):
        """TC05: Unequal task durations"""
        cores, tasks, times = 2, 4, [10, 1, 8, 3]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # Verify workloads sum to total
        total = sum(times)
        for algo in ['round_robin', 'greedy', 'lpt']:
            self.assertAlmostEqual(sum(results[algo]['workloads']), total)
    
    # TC06: Single task
    def test_tc06_single_task(self):
        """TC06: Single task"""
        cores, tasks, times = 4, 1, [15]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # All algorithms should assign the single task to one core
        for algo in ['round_robin', 'greedy', 'lpt']:
            workloads = results[algo]['workloads']
            self.assertEqual(sum(1 for w in workloads if w > 0), 1)
            self.assertEqual(sum(workloads), 15)
    
    # TC07: Large number of tasks
    def test_tc07_large_number_tasks(self):
        """TC07: Large number of tasks"""
        cores = 4
        times = [i % 10 + 1 for i in range(100)]  # 100 tasks
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # Verify all tasks assigned
        for algo in ['round_robin', 'greedy', 'lpt']:
            total_assigned = sum(len(assign) for assign in results[algo]['assignments'])
            self.assertEqual(total_assigned, 100)
    
    # TC08: Invalid number of cores
    def test_tc08_invalid_cores(self):
        """TC08: Invalid number of cores"""
        with self.assertRaises(ValueError):
            self.validator.validate_cores(0)
        with self.assertRaises(ValueError):
            self.validator.validate_cores(-1)
        with self.assertRaises(ValueError):
            self.validator.validate_cores("invalid")
    
    # TC09: Negative task execution time
    def test_tc09_negative_time(self):
        """TC09: Negative task execution time"""
        with self.assertRaises(ValueError):
            self.validator.validate_execution_times("-5, 10, 3")
    
    # TC10: Zero task execution time
    def test_tc10_zero_time(self):
        """TC10: Zero task execution time (allowed in simulation)"""
        times = self.validator.validate_execution_times("0, 10, 5")
        self.assertEqual(times, [0.0, 10.0, 5.0])
    
    # TC11: Empty input
    def test_tc11_empty_input(self):
        """TC11: Empty input"""
        with self.assertRaises(ValueError):
            self.validator.validate_execution_times("")
    
    # TC12: Non-numeric input
    def test_tc12_non_numeric(self):
        """TC12: Non-numeric input"""
        with self.assertRaises(ValueError):
            self.validator.validate_execution_times("10, abc, 5")
    
    # TC13: Floating-point execution times
    def test_tc13_floating_point(self):
        """TC13: Floating-point execution times"""
        times = self.validator.validate_execution_times("10.5, 8.25, 3.75")
        self.assertEqual(times, [10.5, 8.25, 3.75])
    
    # TC14: Deterministic tie-breaking (LPT)
    def test_tc14_tie_breaking(self):
        """TC14: Deterministic tie-breaking"""
        # Equal task durations: retain original order
        # Equal core workloads: select lowest core ID
        cores = 2
        times = [5, 5, 5, 5]  # All equal
        results = self.scheduler.run_all_algorithms(cores, times)
        
        # LPT should distribute evenly with deterministic tie-breaking
        lpt_workloads = results['lpt']['workloads']
        self.assertEqual(lpt_workloads, [10, 10])
    
    # TC15: No lost or duplicated tasks
    def test_tc15_no_lost_duplicated(self):
        """TC15: No lost or duplicated tasks"""
        cores, tasks, times = 3, 7, [10, 8, 6, 4, 2, 12, 5]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        for algo in ['round_robin', 'greedy', 'lpt']:
            assignments = results[algo]['assignments']
            # Flatten assignments
            all_tasks = [task for core_assign in assignments for task in core_assign]
            self.assertEqual(len(all_tasks), tasks)
            self.assertEqual(len(set(all_tasks)), tasks)  # No duplicates
            self.assertEqual(min(all_tasks), 0)
            self.assertEqual(max(all_tasks), tasks - 1)
    
    # TC16: Workload preservation
    def test_tc16_workload_preservation(self):
        """TC16: Workload preservation"""
        cores, tasks, times = 4, 8, [10, 8, 6, 4, 2, 12, 5, 3]
        total_expected = sum(times)
        
        results = self.scheduler.run_all_algorithms(cores, times)
        
        for algo in ['round_robin', 'greedy', 'lpt']:
            total_actual = sum(results[algo]['workloads'])
            self.assertAlmostEqual(total_actual, total_expected)
    
    # TC17: Makespan consistency
    def test_tc17_makespan_consistency(self):
        """TC17: Makespan consistency"""
        cores, tasks, times = 4, 8, [10, 8, 6, 4, 2, 12, 5, 3]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        metrics = {}
        for algo in ['round_robin', 'greedy', 'lpt']:
            metrics[algo] = self.metrics.calculate_all_metrics(cores, times, results[algo]['workloads'])
        
        # LPT should have lowest makespan (best performance)
        self.assertLessEqual(metrics['lpt']['makespan'], metrics['greedy']['makespan'])
        self.assertLessEqual(metrics['greedy']['makespan'], metrics['round_robin']['makespan'])
    
    # TC18: Valid utilization
    def test_tc18_valid_utilization(self):
        """TC18: Valid utilization (0-100%)"""
        cores, tasks, times = 4, 8, [10, 8, 6, 4, 2, 12, 5, 3]
        results = self.scheduler.run_all_algorithms(cores, times)
        
        for algo in ['round_robin', 'greedy', 'lpt']:
            metrics = self.metrics.calculate_all_metrics(cores, times, results[algo]['workloads'])
            utilization = metrics['utilization']
            self.assertTrue(0 <= utilization <= 100)


def run_tests_and_report():
    """Run tests and generate report (Part D Section 11)."""
    print("=" * 70)
    print(" AUTOMATED TEST SUITE EXECUTION ")
    print("=" * 70)
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoadBalancingSimulator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    report = []
    report.append("# TEST RESULTS REPORT")
    report.append(f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Tests Run: {result.testsRun}")
    report.append(f"Failures: {len(result.failures)}")
    report.append(f"Errors: {len(result.errors)}")
    report.append(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    report.append("\n## Test Case Summary")
    report.append("| Test ID | Objective | Status |")
    report.append("|---------|-----------|--------|")
    
    # Map test methods to TC IDs
    tc_mapping = {
        'test_tc01_normal_allocation': 'TC01: Normal task allocation',
        'test_tc02_single_core': 'TC02: Single CPU core',
        'test_tc03_more_cores_than_tasks': 'TC03: More cores than tasks',
        'test_tc04_equal_durations': 'TC04: Equal task durations',
        'test_tc05_unequal_durations': 'TC05: Unequal task durations',
        'test_tc06_single_task': 'TC06: Single task',
        'test_tc07_large_number_tasks': 'TC07: Large number of tasks',
        'test_tc08_invalid_cores': 'TC08: Invalid number of cores',
        'test_tc09_negative_time': 'TC09: Negative task execution time',
        'test_tc10_zero_time': 'TC10: Zero task execution time',
        'test_tc11_empty_input': 'TC11: Empty input',
        'test_tc12_non_numeric': 'TC12: Non-numeric input',
        'test_tc13_floating_point': 'TC13: Floating-point execution times',
        'test_tc14_tie_breaking': 'TC14: Deterministic tie-breaking',
        'test_tc15_no_lost_duplicated': 'TC15: No lost or duplicated tasks',
        'test_tc16_workload_preservation': 'TC16: Workload preservation',
        'test_tc17_makespan_consistency': 'TC17: Makespan consistency',
        'test_tc18_valid_utilization': 'TC18: Valid utilization'
    }
    
    for test_method, tc_desc in tc_mapping.items():
        # Check if test passed
        test_passed = True
        for failure in result.failures:
            if test_method in str(failure[0]):
                test_passed = False
                break
        for error in result.errors:
            if test_method in str(error[0]):
                test_passed = False
                break
        
        status = "PASS" if test_passed else "FAIL"
        report.append(f"| {tc_desc.split(':')[0]} | {tc_desc.split(':', 1)[1].strip()} | {status} |")
    
    # Save report
    report_path = "Multi_Core_Processor_Load_Balancing/TEST_RESULTS.md"
    with open(report_path, 'w') as f:
        f.write("\n".join(report))
    
    print(f"\nTest report saved to: {report_path}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests_and_report()
    sys.exit(0 if success else 1)
