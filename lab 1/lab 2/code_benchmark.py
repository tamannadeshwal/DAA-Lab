"""Task 3 - Code snippets to benchmark.

Every function returns (result, operations) where `operations`
is a simple count of how many basic steps were done.
"""


def single_loop(n):
    """Sums 0..n-1 using a single loop. O(n)"""
    total = 0
    operations = 0
    for i in range(n):
        total += i
        operations += 1
    return total, operations


def nested_loop(n):
    """Counts all (i, j) pairs using a nested loop. O(n^2)"""
    total = 0
    operations = 0
    for i in range(n):
        for j in range(n):
            total += 1
            operations += 1
    return total, operations


def factorial_recursive(n):
    """n! using recursion. O(n) time, O(n) stack space."""
    if n <= 1:
        return 1, 1
    value, ops = factorial_recursive(n - 1)
    return n * value, ops + 1


def factorial_iterative(n):
    """n! using a loop. O(n) time, O(1) space."""
    result = 1
    operations = 0
    for i in range(2, n + 1):
        result *= i
        operations += 1
    return result, operations


# Names shown in the app -> function
SNIPPETS = {
    "Single Loop Traversal": single_loop,
    "Nested Loop Traversal": nested_loop,
    "Recursive Factorial": factorial_recursive,
    "Iterative Factorial": factorial_iterative,
}

if __name__ == "__main__":
    for name, func in SNIPPETS.items():
        print(name, "(n=10) ->", func(10))
