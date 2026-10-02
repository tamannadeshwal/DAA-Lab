import pandas as pd

def fetch_complexity_matrix():
    """Returns the theoretical runtime and space limits for evaluation."""
    matrix_records = {
        "Routine / Paradigm": [
            "Sequential Lookup", "Logarithmic Lookup", 
            "Single Tier Loop", "Double Tier Loop", 
            "Recursive Factorial", "Iterative Factorial"
        ],
        "Theoretical Time Complexity": ["O(n)", "O(log n)", "O(n)", "O(n²)", "O(n)", "O(n)"],
        "Theoretical Space Complexity": ["O(1)", "O(1)", "O(1)", "O(1)", "O(n)", "O(1)"]
    }
    return pd.DataFrame(matrix_records)
