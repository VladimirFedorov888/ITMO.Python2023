import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread


# Генерация матриц заданного размера с элементами в указанном диапазоне и сохранение их в файлы
def generate_matrices(size, min_val, max_val, dtype=np.float64):
    A = np.random.randint(min_val, max_val, (size, size)).astype(dtype)
    B = np.random.randint(min_val, max_val, (size, size)).astype(dtype)
    np.savetxt("A.csv", A, delimiter=",")
    np.savetxt("B.csv", B, delimiter=",")

# Загрузка матриц из файлов
def load_matrices():
    A = np.loadtxt("A.csv", delimiter=",")
    B = np.loadtxt("B.csv", delimiter=",")
    return A, B

# Реализация DGEMM без многопоточности
def dgemm(A, B):
    return np.dot(A, B)

# Реализация DGEMM с использованием многопоточности
def dgemm_threaded(A, B, num_threads):
    size = len(A)
    result = np.zeros((size, size))

    # Рабочая функция для потоков
    def worker(start_row, end_row):
        for i in range(start_row, end_row):
            result[i, :] = np.dot(A[i, :], B)

    threads = []
    chunk_size = size // num_threads

    # Создание и запуск потоков
    for i in range(num_threads):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size if i < num_threads - 1 else size
        t = Thread(target=worker, args=(start_row, end_row))
        threads.append(t)
        t.start()

    # Ожидание завершения всех потоков
    for t in threads:
        t.join()

    return result

# Функция для выполнения экспериментов с указанными параметрами
def run_experiment(dgemm_func, num_runs, dtype=np.float64):
    A, B = load_matrices()
    timings = []

    for _ in range(num_runs):
        start = time.time()
        result = dgemm_func(A.astype(dtype), B.astype(dtype))
        end = time.time()
        timings.append(end - start)

    return timings

# Сохранение результатов эксперимента в файл CSV
def save_to_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["run", "time"])
        for i, t in enumerate(data):
            writer.writerow([i + 1, t])

# Создание графиков времени выполнения и сохранение их в виде файлов
def plot_timings(timings, xlabel, ylabel, title, save_to_file):
    plt.figure()
    plt.plot(timings)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.savefig(save_to_file)


# Функция для вывода сводной статистики по времени выполнения экспериментов
def print_summary(timings, description):
    # Вычисление минимального, максимального, среднего времени выполнения, стандартного отклонения и медианы из списка timings
    min_time = min(timings)
    max_time = max(timings)
    avg_time = np.mean(timings)
    std_dev = np.std(timings)
    median = np.median(timings)

    # Вывод описания реализации DGEMM
    print(f"  Min time: {min_time:.6f} s")     # Вывод минимального времени выполнения
    print(f"  Max time: {max_time:.6f} s")  # Вывод максимального времени выполнения
    print(f"  Avg time: {avg_time:.6f} s") # Вывод среднего времени выполнения
    print(f"  Std deviation: {std_dev:.6f} s") # Вывод стандартного отклонения времени выполнения
    print(f"  Median: {median:.6f} s") # Вывод медианы времени выполнения

def main():
    size = 1000  # Размер матрицы
    min_val = -10  # Минимальный диапазон значений элементов матриц
    max_val = 10 # Максимальный диапазон значений элементов матриц
    num_runs = 10 # Количество запусков
    num_threads = 5 # Количество потоков
    # Генерация матриц с заданными размерами и диапазоном значений
    generate_matrices(size, min_val, max_val)

    # Запуск экспериментов для каждой реализации DGEMM и запись времени выполнения
    timings_float = run_experiment(dgemm, num_runs)
    timings_float_threaded = run_experiment(lambda A, B: dgemm_threaded(A, B, num_threads), num_runs)
    timings_int = run_experiment(dgemm, num_runs, dtype=np.int64)
    timings_int_threaded = run_experiment(lambda A, B: dgemm_threaded(A, B, num_threads), num_runs, dtype=np.int64)

    # Сохранение результатов эксперимента в файлы CSV
    save_to_csv("float.csv", timings_float)
    save_to_csv("float_threaded.csv", timings_float_threaded)
    save_to_csv("int.csv", timings_int)
    save_to_csv("int_threaded.csv", timings_int_threaded)

    # Построение графиков времени выполнения для каждой реализации DGEMM и сохранение их в виде файлов
    plot_timings(timings_float, "Runs", "Time (s)", "DGEMM (Float)", "float.png")
    plot_timings(timings_float_threaded, "Runs", "Time (s)", f"DGEMM (Float, {num_threads} Threads)",
                 "float_threaded.png")
    plot_timings(timings_int, "Runs", "Time (s)", "DGEMM (Int)", "int.png")
    plot_timings(timings_int_threaded, "Runs", "Time (s)", f"DGEMM (Int, {num_threads} Threads)", "int_threaded.png")
    print_summary(timings_float, "DGEMM (Float)")
    print_summary(timings_float_threaded, f"DGEMM (Float, {num_threads} Threads)")
    print_summary(timings_int, "DGEMM (Int)")
    print_summary(timings_int_threaded, f"DGEMM (Int, {num_threads} Threads)")

if __name__ == "__main__":
    main()
    # Вывод времени выполнения экспериментов для каждой реализации DGEMM в консоль

