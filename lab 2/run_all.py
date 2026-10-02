import os
from benchmark_engine import PerformanceEvaluator
from search_analysis import sequential_lookup, logarithmic_lookup
from code_benchmark import traverse_single_tier, traverse_double_tier, compute_factorial_recur, compute_factorial_iter
from plotting import generate_trend_plots

def execute_pipeline():
    for folder in ["data", "results", "graphs", "report"]:
        os.makedirs(folder, exist_ok=True)
        
    runner = PerformanceEvaluator()
    scales = [100, 500, 1000, 2000]

    runner.execute_profile(traverse_single_tier, scales, "Linear Loop")
    runner.execute_profile(traverse_double_tier, [100, 200, 300, 400], "Quadratic Loop")
    runner.execute_profile(compute_factorial_recur, [100, 300, 500, 700], "Factorial (Stack)")
    runner.execute_profile(compute_factorial_iter, scales, "Factorial (Loop)")
    
    runner.execute_profile(sequential_lookup, scales, "Sequential Search", 
                           input_generator=lambda n: (list(range(n)), -1))
    runner.execute_profile(logarithmic_lookup, scales, "Logarithmic Search", 
                           input_generator=lambda n: (list(range(n)), -1))

    summary_df = runner.export_summary()
    summary_df.to_csv("results/runtime_metrics.csv", index=False)
    generate_trend_plots(summary_df)
    print("Pipeline verification complete. Benchmarks stored successfully.")

if __name__ == "__main__":
    execute_pipeline()
