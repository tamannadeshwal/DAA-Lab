"""Task 2 - Search algorithms (Linear Search and Binary Search).

Both functions return (index, comparisons) so we can show the
number of comparisons made.
"""
import random


def generate_dataset(size, sorted_data=False):
    """Make a list of `size` unique random numbers."""
    data = random.sample(range(size * 10), size)
    if sorted_data:
        data.sort()
    return data


def linear_search(arr, target):
    """Returns (index of target or -1, number of comparisons)."""
    comparisons = 0
    for i, value in enumerate(arr):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons


def binary_search(arr, target):
    """arr MUST be sorted. Returns (index of target or -1, comparisons)."""
    comparisons = 0
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


if __name__ == "__main__":
    data = generate_dataset(10, sorted_data=True)
    print("Data:", data)
    print("Linear search for", data[3], "->", linear_search(data, data[3]))
    print("Binary search for", data[3], "->", binary_search(data, data[3]))
