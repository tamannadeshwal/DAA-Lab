"""Task 5 + 6 - Charts and complexity table."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # lets us save charts without opening a window
import matplotlib.pyplot as plt

# Theoretical complexity (Task 6)
THEORY = {
    "Linear Search": ("O(n)", "O(1)"),
    "Binary Search": ("O(log n)", "O(1)"),
    "Recursive Factorial": ("O(n)", "O(n)"),
    "Iterative Factorial": ("O(n)", "O(1)"),
    "Single Loop": ("O(n)", "O(1)"),
    "Nested Loop": ("O(n²)", "O(1)"),
}


def compare_chart(df, algos, x_label, title, column="time_sec", y_label="Execution Time (seconds)", filename=None):
    """Line chart comparing the given algorithms on one graph."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in algos:
        part = df[df["algorithm"] == algo]
        if len(part) > 0:
            ax.plot(part["input_size"], part[column], marker="o", label=algo)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    if filename:
        fig.savefig(filename, dpi=150, bbox_inches="tight")
    return fig


def make_all_charts(df, folder="."):
    """Creates the 3 time charts + 3 memory charts. Returns list of file names."""
    groups = [
        ("search", ["Linear Search", "Binary Search"], "Dataset Size", "Linear Search vs Binary Search"),
        ("factorial", ["Recursive Factorial", "Iterative Factorial"], "Input Size (n)", "Recursive vs Iterative Factorial"),
        ("loops", ["Single Loop", "Nested Loop"], "Number of Iterations (n)", "Single Loop vs Nested Loop"),
    ]
    files = []
    for key, algos, xlabel, title in groups:
        f1 = f"{folder}/graph_{key}_time.png"
        compare_chart(df, algos, xlabel, title + " - Time", filename=f1)
        f2 = f"{folder}/graph_{key}_memory.png"
        compare_chart(df, algos, xlabel, title + " - Memory", "memory_kb", "Peak Memory (KB)", f2)
        files += [f1, f2]
        plt.close("all")
    return files


def growth_exponent(sizes, times):
    """Slope of log(time) vs log(n).  ~1 = linear, ~2 = quadratic, ~0 = very flat."""
    slope = np.polyfit(np.log(sizes), np.log(times), 1)[0]
    return slope


def trend_name(exponent):
    if exponent < 0.4:
        return "Almost constant / logarithmic"
    if exponent < 1.6:
        return "Linear growth"
    return "Quadratic growth"


def complexity_table(df):
    """Theoretical vs observed table (Task 6)."""
    rows = []
    for algo, (time_c, space_c) in THEORY.items():
        part = df[df["algorithm"] == algo]
        if len(part) < 2:
            continue
        exp = growth_exponent(part["input_size"], part["time_sec"])
        biggest = part.iloc[-1]
        rows.append({
            "Algorithm": algo,
            "Time Complexity": time_c,
            "Space Complexity": space_c,
            "Largest n": int(biggest["input_size"]),
            "Time at largest n (s)": round(biggest["time_sec"], 6),
            "Memory at largest n (KB)": round(biggest["memory_kb"], 2),
            "Growth exponent": round(exp, 2),
            "Observed trend": trend_name(exp),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv("benchmark_results.csv")
    print(make_all_charts(df))
    print(complexity_table(df).to_string(index=False))
