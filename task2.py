def binary_search_with_upper_bound(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return (iterations, upper_bound)

arr = [0.1, 1.5, 3.2, 4.8, 5.6, 7.9]
target = 4.0

print(binary_search_with_upper_bound(arr, target))
