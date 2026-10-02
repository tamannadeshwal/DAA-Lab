import streamlit as st
import pandas as pd
from benchmark_engine import PerformanceEvaluator
from search_analysis import sequential_lookup, logarithmic_lookup
from code_benchmark import traverse_single_tier, traverse_double_tier, compute_factorial_recur, compute_factorial_iter
from complexity import fetch_complexity_matrix

st.set_page_config(page_title="AlgoMetrics: Benchmarking Station", layout="wide")
st.title("🔬 AlgoMetrics: Architecture Performance Tool")

sidebar_selection = st.sidebar.selectbox("Navigation Panel", ["Dashboard Analytics", "Theoretical Matrix"])

if sidebar_selection == "Dashboard Analytics":
    st.header("⚡ Live Routine Diagnostics")
    chosen_paradigm = st.selectbox("Choose Routine Family", ["Search Implementations", "Iterative Micro-Loops", "Factorial Processing"])
    input_dimension = st.slider("Target Scale Dimension (N)", min_value=10, max_value=2000, value=500, step=50)
    
    if st.button("Trigger Diagnostic Benchmark"):
        evaluator = PerformanceEvaluator()
        if chosen_paradigm == "Search Implementations":
            arr = list(range(input_dimension))
            evaluator.execute_profile(sequential_lookup, [input_dimension], "Linear Search", lambda n: (arr, -1))
            evaluator.execute_profile(logarithmic_lookup, [input_dimension], "Binary Search", lambda n: (arr, -1))
        elif chosen_paradigm == "Iterative Micro-Loops":
            evaluator.execute_profile(traverse_single_tier, [input_dimension], "Single Loop")
            evaluator.execute_profile(traverse_double_tier, [min(input_dimension, 400)], "Nested Loop")
        else:
            evaluator.execute_profile(compute_factorial_recur, [min(input_dimension, 700)], "Recursive Stack")
            evaluator.execute_profile(compute_factorial_iter, [input_dimension], "Iterative Accumulator")
            
        report_df = evaluator.export_summary()
        st.success("Profiling Successfully Finalized!")
        st.dataframe(report_df, use_container_width=True)
else:
    st.header("📋 Algorithmic Blueprint Matrix")
    st.table(fetch_complexity_matrix())
