import random
import timeit
import statistics
from tabulate import tabulate

from insert_sort import insertion_sort
from merge_sort import merge_sort
from timsort import timsort

if __name__ == "__main__":
    # Генерація тестових даних
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

    repeats = 5
    results = []

    # Збір результатів
    for name, data in datasets.items():
        for algo_name, algo in algorithms.items():
            times = timeit.repeat(lambda: algo(data.copy()), repeat=repeats, number=1)
            avg_time = statistics.mean(times)
            results.append([name, algo_name, f"{avg_time:.6f}"])

    # Формування Markdown-таблиці
    table_md = tabulate(results, headers=["Dataset", "Algorithm", "Avg Time (s)"], tablefmt="github")

    # Формування фінального тексту для README.md
    content = f"""# Висновки

Нижче наведені результати порівняння алгоритмів сортування:

{table_md}
"""

    # Запис у README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("Результати збережено у README.md")


    



