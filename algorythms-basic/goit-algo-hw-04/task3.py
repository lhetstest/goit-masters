import random
import timeit

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def insertion_sort(arr):
    a = arr[:]  # копія щоб не міняти вхідний список
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def time_algorithm(alg, data):
    """
    Замір часу виконання алгоритму alg на копії data.
    """
    return timeit.timeit(lambda: alg(data), number=1)

if __name__ == "__main__":
    sizes = [100, 1000, 3000]
    for size in sizes:
        data = [random.randint(0, size) for _ in range(size)]
        print(f"\nРозмір масиву: {size}")

        t_merge = time_algorithm(merge_sort, data)
        print(f"Merge sort: {t_merge:.5f} сек")

        t_insertion = time_algorithm(insertion_sort, data)
        print(f"Insertion sort: {t_insertion:.5f} сек")

        t_timsort = time_algorithm(sorted, data)
        print(f"Timsort (built-in sorted): {t_timsort:.5f} сек")
