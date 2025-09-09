import random
import timeit
import statistics

from insert_sort import insertion_sort
from merge_sort import merge_sort
from timsort import timsort

if __name__ == "__main__":
    # Генерація даних
    data_small = [random.randint(0, 1000) for _ in range(1000)]
    data_medium = [random.randint(0, 1000) for _ in range(5000)]
    data_big = [random.randint(0, 1000) for _ in range(10000)]

    datasets = {
        "Small (1k)": data_small,
        "Medium (5k)": data_medium,
        "Big (10k)": data_big,
    }

    algorithms = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Timsort": timsort,
    }

    repeats = 5  # скільки разів повторювати замір для середнього

    print(f"{'Dataset':15s} | {'Algorithm':15s} | {'Avg Time (s)':>12s}")
    print("-" * 50)

    for name, data in datasets.items():
        for algo_name, algo in algorithms.items():
            times = timeit.repeat(lambda: algo(data.copy()), repeat=repeats, number=1)
            avg_time = statistics.mean(times)
            print(f"{name:15s} | {algo_name:15s} | {avg_time:12.6f}")

    



