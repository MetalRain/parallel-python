import random
import time
import math
import multiprocessing as mp

def matrix_dims(a):
    return (len(a), len(a[0]))

def seq_matrix_multiply(a, b):
    rows_a, cols_a = matrix_dims(a)
    rows_b, cols_b = matrix_dims(b)
    if cols_a != rows_b:
        raise ArithmeticError("Cannot multiply {}x{} with {}x{} matrix".format(rows_a, cols_a, rows_b, cols_b))
    
    c = [[0] * cols_b for i in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                c[i][j] += a[i][k] * b[k][j]
    return c

def par_matrix_multiply(a, b):
    pass

def time_it(name, NUMBER_OF_RUNS, fn, *args) -> int:
    print('Running', name, 'for', NUMBER_OF_RUNS, 'times')
    # Warmup
    _ = fn(*args)
    total_time = 0
    # Timed runs
    for _ in range(NUMBER_OF_RUNS):
        start = time.perf_counter()
        fn(*args)
        total_time += time.perf_counter() - start
    # Avg times
    total_time /= NUMBER_OF_RUNS
    print(name, 'run for', int(total_time * 1000), 'ms on average.')
    return total_time

if __name__ == '__main__':
    NUMBER_OF_RUNS = 1
    MATRIX_SIZE = 200
    a = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]
    b = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]

    time_it("Sequential", NUMBER_OF_RUNS, seq_matrix_multiply, a, b)
