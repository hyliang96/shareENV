# quick sort algorithm

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for i in range(1, len(arr)):
            if arr[i] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
        return quick_sort(left) + [pivot] + quick_sort(right)

arr = [3, 7, 1, 9, 2, 5]
print(quick_sort(arr))   # Output: [1, 2, 3, 5, 7, 9]
