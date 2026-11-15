# Multi-Core Processor Load Balancing Simulator
## Requirements
- Python 3.10+
- matplotlib (for visualization)
- python-docx (for Word documentation)
- pandas (for CSV handling)
- numpy (for mathematical operations)
- streamlit (for interactive web dashboard)
- plotly (for interactive charts)

## Installation
```bash
cd Multi_Core_Processor_Load_Balancing
pip install -r requirements.txt
```

## Usage

### 1. Command-Line Interface (CLI)
```bash
cd Multi_Core_Processor_Load_Balancing
python main.py
```

### 2. Advanced Streamlit Web Application (Mandatory Requirement)
```bash
cd Multi_Core_Processor_Load_Balancing
streamlit run app.py
```

## Project Structure
- main.py: CLI entry point and user interaction
- app.py: Streamlit web dashboard (Advanced Engineering Requirement)
- scheduler.py: RR, Greedy, LPT algorithms
- metrics.py: Performance calculations
- validation.py: Input validation and error handling
- visualization.py: Workload charts and comparisons
- test_scheduler.py: Automated tests (TC01-TC18)
- requirements.txt: Dependencies
- README.md: Usage instructions

## Engineering Features
- Professional Streamlit dashboard with dark theme
- Interactive workload visualizations (Plotly)
- Real-time performance metrics
- Algorithm comparison and insights
- CSV import/export functionality
- Educational algorithm explanations
- Technical insights generation
