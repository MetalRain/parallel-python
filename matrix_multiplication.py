#!/usr/bin/env python3

import random
import time
import math
import multiprocessing as mp
from concurrent.futures import Future, ProcessPoolExecutor, as_completed

from typing import Any, List, Optional, Tuple

Vector = List[float]
Matrix = List[Vector]

def matrix_dims(a: Matrix) -> Tuple[int, int]:
    return (len(a), len(a[0]))

def empty_matrix(*, rows: int, cols: int) -> Matrix:
    return [[0.0] * cols for i in range(rows)]

def seq_matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    rows_a, cols_a = matrix_dims(a)
    rows_b, cols_b = matrix_dims(b)
    if cols_a != rows_b:
        raise ArithmeticError("Cannot multiply {}x{} with {}x{} matrix".format(rows_a, cols_a, rows_b, cols_b))

    c = empty_matrix(rows=rows_a, cols=cols_b)
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                c[i][j] += a[i][k] * b[k][j]
    return c

def matrix_transpose(a: Matrix) -> Matrix:
    rows, cols = matrix_dims(a)
    return [ [ a[i][j] for i in range(rows) ] for j in range(cols) ]

def dot_product(a: Vector, b: Vector) -> float:
    return sum(i * j for i,j in zip(a, b))

def multiple_row(a_row: Vector, b_rows: Matrix) -> Vector:
    return [ dot_product(a_row, b_row) for b_row in b_rows ]

def par_matrix_multiply(a: Matrix, b: Matrix, num_processes: Optional[int] = None) -> Matrix:
    rows_a, cols_a = matrix_dims(a)
    rows_b, cols_b = matrix_dims(b)
    if cols_a != rows_b:
        raise ArithmeticError("Cannot multiply {}x{} with {}x{} matrix".format(rows_a, cols_a, rows_b, cols_b))
    
    # Precalculate transposes
    b_T = matrix_transpose(b)
    with ProcessPoolExecutor(max_workers=num_processes) as pool:
        # Fork
        row_futures: List[Future] = [ pool.submit(multiple_row, a_row, b_T) for i, a_row in enumerate(a) ]
        # Join
        result: Matrix = [ row.result() for row in row_futures ]

    return result

def time_it(name, NUMBER_OF_RUNS, fn, *args) -> float:
    print('Running', name, 'for', NUMBER_OF_RUNS, 'times')
    # Warmup
    _ = fn(*args)
    total_time = 0.0
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
    NUMBER_OF_RUNS = 2
    PROCESS_COUNT = 2
    MATRIX_SIZE = 300
    print('Measuring matrix multiplication speedup with {}x{} matrices using {} processes.'.format(MATRIX_SIZE, MATRIX_SIZE, PROCESS_COUNT))
    a = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]
    b = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]

    seq_time = time_it("Sequential", NUMBER_OF_RUNS, seq_matrix_multiply, a, b)
    par_time = time_it("Parallel", NUMBER_OF_RUNS, par_matrix_multiply, a, b, PROCESS_COUNT)

    time_saved = seq_time - par_time
    speedup = seq_time / par_time
    efficiency  =  speedup / PROCESS_COUNT
    print('Saved', int(time_saved * 1000), 'ms', 'Speedup was', round(speedup, 2), 'Efficiency', round(efficiency * 100, 2), '%')
