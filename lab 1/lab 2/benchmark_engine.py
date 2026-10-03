"""Task 1 + 4 - Reusable benchmarking engine.

Measures execution time (time.perf_counter), peak memory (tracemalloc)
and number of operations for any function and many input sizes.
"""
import sys
import time
import tracemalloc

import pandas as pd

from search_analysis import linear_search, binary_search, generate_dataset
from code_benchmark import single_loop, nested_loop, factorial_recursive, factorial_iterative

# Recursive factorial with n = 1000 needs a deeper stack than the default
sys.setrecursionlimit(5000)


class BenchmarkEngine:
    def __init__(self):
        self.results = []

    def measure(self, func, args, repeats=5):
        """Run func once for memory and `repeats` times for time.
        Returns (avg_time_sec, peak_memory_kb, operations)."""
        # 1) memory (separate run, because tracemalloc slows code down)
        tracemalloc.start()
        output = func(*args)
        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        # 2) time (average of several runs)
        total = 0
        for _ in range(repeats):
            start = time.perf_counter()
            func(*args)
            total += time.perf_counter() - start

        # functions return (result, operations)
        operations = output[1] if isinstance(output, tuple) else None
        return total / repeats, peak / 1024, operations

    def run(self, func, input_sizes, name=None, arg_builder=lambda n: (n,), repeats=5):
        """Benchmark func for every n in input_sizes."""
        name = name or func.__name__
        for n in input_sizes:
            t, mem, ops = self.measure(func, arg_builder(n), repeats)
            self.results.append({
                "algorithm": name,
                "input_size": n,
                "time_sec": t,
                "memory_kb": mem,
                "operations": ops,
            })
        return self

    def as_dataframe(self):
        return pd.DataFrame(self.results)


# ---- Input sizes used by the automated run (Task 4) ----
SEARCH_SIZES = [100, 1000, 10000, 50000]
FACTORIAL_SIZES = [100, 500, 1000]
LOOP_SIZES = [100, 1000, 10000, 50000]
NESTED_SIZES = [100, 1000, 5000, 10000]   # 50,000 would need 2.5 billion steps


def run_all_benchmarks():
    """Runs every algorithm for every input size and returns a DataFrame."""
    engine = BenchmarkEngine()

    # Worst case for both searches: the key is NOT in the list
    engine.run(linear_search, SEARCH_SIZES, name="Linear Search",
               arg_builder=lambda n: (generate_dataset(n), -1))
    engine.run(binary_search, SEARCH_SIZES, name="Binary Search",
               arg_builder=lambda n: (generate_dataset(n, sorted_data=True), -1))

    engine.run(factorial_recursive, FACTORIAL_SIZES, name="Recursive Factorial")
    engine.run(factorial_iterative, FACTORIAL_SIZES, name="Iterative Factorial")

    engine.run(single_loop, LOOP_SIZES, name="Single Loop")
    engine.run(nested_loop, NESTED_SIZES, name="Nested Loop", repeats=1)
    return engine.as_dataframe()


if __name__ == "__main__":
    df = run_all_benchmarks()
    print(df)
    df.to_csv("benchmark_results.csv", index=False)
    print("Saved benchmark_results.csv")
