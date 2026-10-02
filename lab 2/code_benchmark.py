def traverse_single_tier(limit):
    """Computes a basic cumulative sum over a linear dimension."""
    accumulator = 0
    for value in range(limit):
        accumulator += value
    return accumulator

def traverse_double_tier(limit):
    """Executes a quadratic O(n^2) operation across matrix indices."""
    counter = 0
    for row_idx in range(limit):
        for col_idx in range(limit):
            counter += 1
    return counter

def compute_factorial_recur(value):
    """Computes value! via top-down functional call stack invocation."""
    if value <= 1:
        return 1
    return value * compute_factorial_recur(value - 1)

def compute_factorial_iter(value):
    """Computes value! smoothly using an iterative low-overhead accumulation loop."""
    product_total = 1
    for step in range(2, value + 1):
        product_total *= step
    return product_total
