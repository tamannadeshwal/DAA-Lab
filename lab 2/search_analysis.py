def sequential_lookup(dataset, element_key):
    """
    Iteratively scans elements one-by-one to discover the index of element_key.
    """
    for position in range(len(dataset)):
        if dataset[position] == element_key:
            return position
    return -1

def logarithmic_lookup(sorted_dataset, element_key):
    """
    Performs a binary split search over an ordered dataset to extract the target key.
    """
    left_bound, right_bound = 0, len(sorted_dataset) - 1
    
    while left_bound <= right_bound:
        median_idx = (left_bound + right_bound) // 2
        if sorted_dataset[median_idx] == element_key:
            return median_idx
        elif sorted_dataset[median_idx] < element_key:
            left_bound = median_idx + 1
        else:
            right_bound = median_idx - 1
    return -1
