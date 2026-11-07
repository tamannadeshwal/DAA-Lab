import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import tracemalloc

st.set_page_config(page_title="Smart Optimization Assistant", page_icon="🧠", layout="wide")
st.title("Smart Optimization Assistant")
st.caption("Lab 4 — Dynamic Programming: LCS, 0/1 Knapsack and Matrix Chain Multiplication")

def lcs(x, y):
    m, n = len(x), len(y)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    i, j, seq = m, n, []
    while i > 0 and j > 0:
        if x[i-1] == y[j-1]:
            seq.append(x[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], "".join(reversed(seq)), dp

def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(capacity+1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen.append(i-1); w -= weights[i-1]
    chosen.reverse()
    return dp[n][capacity], chosen, dp

def matrix_chain(dims):
    n = len(dims)-1
    cost = [[0]*(n+1) for _ in range(n+1)]
    split = [[0]*(n+1) for _ in range(n+1)]
    for length in range(2, n+1):
        for i in range(1, n-length+2):
            j = i+length-1
            cost[i][j] = float("inf")
            for k in range(i, j):
                q = cost[i][k] + cost[k+1][j] + dims[i-1]*dims[k]*dims[j]
                if q < cost[i][j]:
                    cost[i][j], split[i][j] = q, k
    def order(i, j):
        if i == j: return f"A{i}"
        k = split[i][j]
        return "(" + order(i, k) + " × " + order(k+1, j) + ")"
    return cost[1][n], cost, split, order(1, n)

def show_table(table, title):
    st.subheader(title)
    df = pd.DataFrame(table)

    # Compact, fixed-size table. Scroll inside it if it has many rows/columns.
    st.dataframe(
        df,
        width=480,
        height=190,
        hide_index=True,
        column_config={
            col: st.column_config.NumberColumn(width="small")
            for col in df.columns
        },
    )

    # Small heatmap for screenshots.
    arr = np.array(table, dtype=float)
    fig, ax = plt.subplots(figsize=(4, 2.2), dpi=80)
    im = ax.imshow(arr, cmap="Blues", aspect="auto", interpolation="nearest")
    label_size = 5 if arr.size > 50 else 6

    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            ax.text(c, r, str(table[r][c]),
                    ha="center", va="center", fontsize=label_size)

    ax.set_title(title, fontsize=8)
    ax.tick_params(axis="both", labelsize=6)
    ax.set_xlabel("Column", fontsize=7)
    ax.set_ylabel("Row", fontsize=7)
    fig.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

tab1, tab2, tab3, tab4 = st.tabs(["Sequence Analysis — LCS", "Resource Allocation — Knapsack", "Computation Optimization — MCM", "Complexity Summary"])

with tab1:
    st.header("Longest Common Subsequence")
    x = st.text_input("First sequence", "ABCBDAB")
    y = st.text_input("Second sequence", "BDCABA")
    if st.button("Run LCS"):
        start = time.perf_counter(); tracemalloc.start()
        length, seq, table = lcs(x, y)
        current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
        elapsed = time.perf_counter()-start
        st.success(f"LCS: {seq} | Length: {length}")
        c1,c2,c3 = st.columns(3)
        c1.metric("LCS length", length); c2.metric("Execution time", f"{elapsed:.6f} s"); c3.metric("Peak traced memory", f"{peak/1024:.2f} KB")
        show_table(table, "LCS DP Table")
        st.caption(f"Subproblems/table cells: {len(x)*len(y)}. Time: O(m × n), Space: O(m × n).")

with tab2:
    st.header("0/1 Knapsack")
    weights_text = st.text_input("Item weights (comma-separated)", "2,3,4,5")
    values_text = st.text_input("Item values/profits (comma-separated)", "3,4,5,6")
    capacity = st.number_input("Knapsack capacity", min_value=0, value=5, step=1)
    if st.button("Run Knapsack"):
        try:
            weights = [int(v.strip()) for v in weights_text.split(",") if v.strip()]
            values = [int(v.strip()) for v in values_text.split(",") if v.strip()]
            if not weights or len(weights) != len(values) or any(w <= 0 for w in weights) or any(v < 0 for v in values):
                st.error("Enter equal numbers of positive weights and non-negative values.")
            else:
                start=time.perf_counter(); tracemalloc.start()
                profit, chosen, table=knapsack(weights, values, int(capacity))
                current, peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
                elapsed=time.perf_counter()-start
                st.success(f"Maximum achievable profit: {profit}")
                st.write("Selected items (1-based):", [i+1 for i in chosen])
                st.write("Selected weights:", [weights[i] for i in chosen])
                st.write("Selected values:", [values[i] for i in chosen])
                c1,c2,c3=st.columns(3)
                c1.metric("Maximum profit", profit); c2.metric("Execution time", f"{elapsed:.6f} s"); c3.metric("Peak traced memory", f"{peak/1024:.2f} KB")
                show_table(table, "Knapsack DP Table")
                st.caption(f"Subproblems/table cells: {len(weights)* (int(capacity)+1)}. Time: O(n × W), Space: O(n × W).")
        except ValueError:
            st.error("Please enter weights and values as comma-separated integers.")

with tab3:
    st.header("Matrix Chain Multiplication")
    dims_text=st.text_input("Dimension list (comma-separated)", "10,30,5,60")
    if st.button("Run Matrix Chain"):
        try:
            dims=[int(v.strip()) for v in dims_text.split(",") if v.strip()]
            if len(dims)<2 or any(d<=0 for d in dims):
                st.error("Enter at least two positive dimensions.")
            else:
                start=time.perf_counter(); tracemalloc.start()
                cost, table, split, parens=matrix_chain(dims)
                current, peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
                elapsed=time.perf_counter()-start
                st.success(f"Minimum scalar multiplications: {cost}")
                st.write("Optimal multiplication order:", parens)
                c1,c2,c3=st.columns(3)
                c1.metric("Minimum cost", cost); c2.metric("Execution time", f"{elapsed:.6f} s"); c3.metric("Peak traced memory", f"{peak/1024:.2f} KB")
                n=len(dims)-1
                show_table([row[1:] for row in table[1:]], "MCM Cost Table")
                show_table([row[1:] for row in split[1:]], "MCM Split / Parenthesization Table")
                st.caption(f"Number of matrices: {n}. Time: O(n³), Space: O(n²).")
        except ValueError:
            st.error("Please enter dimensions as comma-separated positive integers.")

with tab4:
    st.header("Theoretical Complexity Comparison")
    data=[
        ["Longest Common Subsequence", "O(m × n)", "O(m × n)", "m × n"],
        ["0/1 Knapsack", "O(n × W)", "O(n × W)", "n × W"],
        ["Matrix Chain Multiplication", "O(n³)", "O(n²)", "O(n²) table entries"],
    ]
    st.dataframe(pd.DataFrame(data, columns=["Algorithm","Time Complexity","Space Complexity","DP Subproblems"]), hide_index=True, use_container_width=True)
    st.info("Execution time and memory depend on input size and the computer. Run each module with different inputs and record the displayed measurements for your experiment.")
