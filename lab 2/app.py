"""Streamlit app - Algorithm Performance Measurement and Benchmarking Tool.
Run with:  streamlit run app.py
"""
import random

import pandas as pd
import streamlit as st

from benchmark_engine import BenchmarkEngine, run_all_benchmarks
from search_analysis import linear_search, binary_search, generate_dataset
from code_benchmark import SNIPPETS
from visualization import compare_chart, complexity_table

st.set_page_config(page_title="Algorithm Performance Tool", layout="wide")
st.title("Algorithm Performance Measurement and Benchmarking Tool")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Search Analysis", "2. Code Benchmark", "3. Automated Benchmark", "4. Complexity Analysis"])

# ------------------------------------------------------------------
# Tab 1 - Search algorithms (Task 2)
# ------------------------------------------------------------------
with tab1:
    st.header("Search Algorithm Analysis")
    size = st.number_input("Dataset size", 10, 200000, 10000, step=1000)
    key_choice = st.radio("Search key", ["Random element from the data", "Key not in data", "Enter my own"])
    own_key = st.number_input("Your key", value=0, step=1)

    if st.button("Run Search"):
        data = generate_dataset(size, sorted_data=True)       # sorted so both searches work
        if key_choice == "Random element from the data":
            key = random.choice(data)
        elif key_choice == "Key not in data":
            key = -1
        else:
            key = int(own_key)
        st.write(f"Searching for **{key}** in {size} elements")

        engine = BenchmarkEngine()
        rows = []
        for name, func in [("Linear Search", linear_search), ("Binary Search", binary_search)]:
            t, mem, comps = engine.measure(func, (data, key))
            index = func(data, key)[0]
            rows.append({
                "Algorithm": name,
                "Result": f"Found at index {index}" if index != -1 else "Not found",
                "Comparisons": comps,
                "Time (s)": f"{t:.8f}",
                "Memory (KB)": round(mem, 3),
            })
        st.table(pd.DataFrame(rows))

# ------------------------------------------------------------------
# Tab 2 - Code snippets (Task 3)
# ------------------------------------------------------------------
with tab2:
    st.header("Code Benchmarking")
    chosen = st.multiselect("Select code snippets", list(SNIPPETS.keys()), default=list(SNIPPETS.keys()))
    n = st.number_input("Input size n", 1, 5000, 500, step=100,
                        help="Kept below 5000 because nested loop is O(n²) and recursion has a depth limit")

    if st.button("Run Snippets"):
        engine = BenchmarkEngine()
        rows = []
        for name in chosen:
            t, mem, ops = engine.measure(SNIPPETS[name], (n,))
            rows.append({"Snippet": name, "Time (s)": f"{t:.8f}", "Memory (KB)": round(mem, 3), "Operations": ops})
        st.subheader("Comparison table")
        st.table(pd.DataFrame(rows))

# ------------------------------------------------------------------
# Tab 3 - Automated benchmark + charts (Task 4 + 5)
# ------------------------------------------------------------------
with tab3:
    st.header("Automated Benchmarking")
    st.info("Runs every algorithm on all suggested input sizes. The nested loop with n = 10,000 takes a few seconds.")
    if st.button("Run Full Benchmark"):
        with st.spinner("Benchmarking... please wait"):
            st.session_state["df"] = run_all_benchmarks()

    if "df" in st.session_state:
        df = st.session_state["df"]
        st.dataframe(df)
        st.download_button("Download CSV", df.to_csv(index=False), "benchmark_results.csv")

        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(compare_chart(df, ["Linear Search", "Binary Search"], "Dataset Size", "Search: Size vs Time"))
            st.pyplot(compare_chart(df, ["Recursive Factorial", "Iterative Factorial"], "n", "Factorial: n vs Time"))
            st.pyplot(compare_chart(df, ["Single Loop", "Nested Loop"], "Iterations", "Loops: Iterations vs Time"))
        with col2:
            st.pyplot(compare_chart(df, ["Linear Search", "Binary Search"], "Dataset Size", "Search: Memory",
                                    "memory_kb", "Peak Memory (KB)"))
            st.pyplot(compare_chart(df, ["Recursive Factorial", "Iterative Factorial"], "n", "Factorial: Memory",
                                    "memory_kb", "Peak Memory (KB)"))
            st.pyplot(compare_chart(df, ["Single Loop", "Nested Loop"], "Iterations", "Loops: Memory",
                                    "memory_kb", "Peak Memory (KB)"))

# ------------------------------------------------------------------
# Tab 4 - Complexity table (Task 6)
# ------------------------------------------------------------------
with tab4:
    st.header("Theoretical vs Observed Complexity")
    if "df" in st.session_state:
        st.table(complexity_table(st.session_state["df"]))
        st.caption("Growth exponent = slope of log(time) vs log(n): about 1 means linear, about 2 means quadratic.")
    else:
        st.warning("Run the full benchmark in tab 3 first.")
