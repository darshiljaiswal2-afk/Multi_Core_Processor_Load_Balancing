# TECHNICAL DECISIONS AND IMPLEMENTATION NOTES

## 1. Architecture Decisions
- Modular design separating validation, scheduling, metrics, and visualization
- Object-oriented approach for maintainability
- Type hints for code clarity
- Deterministic tie-breaking in LPT algorithm (original order, lowest core ID)
- **NEW: Streamlit web application integration** (Mandatory Advanced Requirement)
  - Reuses existing scheduling engine (scheduler.py, metrics.py, validation.py)
  - Professional engineering dashboard with dark theme
  - Interactive Plotly visualizations
  - Real-time performance metrics
  - Algorithm comparison and technical insights
  - CSV import/export functionality

## 2. Algorithm Implementations
### Round Robin (Algorithm 1)
- Cyclic assignment without time quantum
- Time Complexity: O(n) where n = number of tasks
- Space Complexity: O(m) where m = number of cores

### Greedy Least Loaded Core (Algorithm 2)
- Dynamic assignment to minimum workload core
- Time Complexity: O(n × m) - searching for minimum each time
- Space Complexity: O(m)

### Longest Processing Time First (LPT) (Algorithm 3)
- Sort tasks descending, then assign to least loaded core
- Time Complexity: O(n log n + n × m)
- Space Complexity: O(n + m)

## 3. Mathematical Framework
- Total Workload (T) = Σ p(i)
- Average Core Workload = T / m
- Makespan = max(W(j))
- Load Imbalance = max(W(j)) - min(W(j))
- Utilization = [T / (m × Makespan)] × 100
- Speedup = T / Makespan

## 4. Verification Results
- Reference example matches expected values exactly
- All 18 test cases pass (TC01-TC18)
- Workload preservation verified
- Deterministic tie-breaking confirmed
- **Streamlit integration verified**: Uses existing engine, produces consistent results

## 5. Limitations
- Simplified model (no preemption, no migration overhead)
- Identical cores assumed
- No memory contention modeling
- Educational simulation only (not real hardware control)
- **Streamlit requirement**: Additional web interface for interactive demonstration

## 6. Dependencies
- Python 3.10+
- matplotlib (visualization)
- python-docx (documentation)
- pandas (CSV export)
- numpy (mathematical operations)
- streamlit (web dashboard - MANDATORY)
- plotly (interactive charts - MANDATORY)
