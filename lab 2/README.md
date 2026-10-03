# Algorithm Performance Measurement and Benchmarking Tool

**Course:** ENCA351 - Design and Analysis of Algorithms Lab (BCA AI&DS, Semester V)
**Lab Assignment 2** | **Name:** `<your name>` | **Roll No:** `<your roll no>`

A simple Python tool that runs algorithms and code snippets, measures **execution time**, **peak memory** and **number of operations**, compares theory with experiment, and draws charts. It has a Streamlit web app and a Jupyter notebook.

## Project files
| File | Purpose |
|---|---|
| `app.py` | Streamlit web app (4 tabs) |
| `search_analysis.py` | Linear Search, Binary Search, dataset generator (counts comparisons) |
| `code_benchmark.py` | Single loop, nested loop, recursive & iterative factorial |
| `benchmark_engine.py` | Reusable engine: time (`perf_counter`), memory (`tracemalloc`), operations |
| `visualization.py` | Charts + theoretical vs observed complexity table |
| `project_notebook.ipynb` | Whole project step by step with outputs |
| `graphs/`, `screenshots/`, `reports/` | Charts, output images, CSVs and the final report |

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py            # web app
jupyter notebook                # open project_notebook.ipynb
python benchmark_engine.py      # command line: saves benchmark_results.csv
```

## Input sizes used
* Search: 100, 1,000, 10,000, 50,000
* Factorial: n = 100, 500, 1000
* Single loop: 100, 1,000, 10,000, 50,000
* Nested loop: 100, 1,000, 5,000, 10,000 (50,000 would need 2.5 billion steps and take minutes in Python)

## Notes
* Memory and time are measured in separate runs, because `tracemalloc` slows the code down.
* Search benchmarks use the worst case (key not present).
* Python's recursion limit is raised to 5000 so recursive factorial works for n = 1000.

## References
Python docs (time, tracemalloc), Streamlit docs, memory_profiler docs, Horowitz-Sahni-Rajasekaran *Fundamentals of Computer Algorithms*.
