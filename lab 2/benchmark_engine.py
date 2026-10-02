import time
import tracemalloc
import pandas as pd

class PerformanceEvaluator:
    """
    Core profiling engine that executes routines across multiple input dimensions 
    and collects high-precision operational runtime and memory footprints.
    """
    def __init__(self):
        self.metrics_log = []

    def execute_profile(self, target_routine, data_scales, display_name=None, input_generator=lambda size: (size,)):
        """
        Runs the specified routine over a sequence of sizes and records system usage.
        """
        label = display_name or target_routine.__name__
        
        for scale in data_scales:
            arguments = input_generator(scale)
            
            # Initialize diagnostics
            tracemalloc.start()
            timestamp_start = time.perf_counter()
            
            # Execute target logic
            target_routine(*arguments)
            
            # Capture diagnostics
            duration = time.perf_counter() - timestamp_start
            _, maximum_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            self.metrics_log.append({
                "Algorithm": label,
                "Input Dimension": scale,
                "Runtime (Sec)": duration,
                "Peak Memory (KB)": maximum_memory / 1024.0
            })
        return self

    def export_summary(self):
        return pd.DataFrame(self.metrics_log)
