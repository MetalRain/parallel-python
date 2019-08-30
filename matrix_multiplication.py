#!/usr/bin/env python3

import random
import time
import math
import multiprocessing as mp
from concurrent.futures import Future, ProcessPoolExecutor, as_completed

from typing import Any, List, Optional, Tuple

Vector = List[int]
Matrix = List[Vector]

def matrix_dims(a: Matrix) -> Tuple[int, int]:
    return (len(a), len(a[0]))

def seq_matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    rows_a, cols_a = matrix_dims(a)
    rows_b, cols_b = matrix_dims(b)
    if cols_a != rows_b:
        raise ArithmeticError("Cannot multiply {}x{} with {}x{} matrix".format(rows_a, cols_a, rows_b, cols_b))

    b_T = matrix_transpose(b)
    return _matrix_multiply(a, b_T)

def matrix_transpose(a: Matrix) -> Matrix:
    rows, cols = matrix_dims(a)
    return [ [ a[i][j] for i in range(rows) ] for j in range(cols) ]

def _matrix_multiply(a_rows: Matrix, b_rows: Matrix) -> Matrix:
    return [
        [
            # dot product
            sum(i * j for i,j in zip(a_row, b_row))
            for b_row in b_rows
        ]
        for a_row in a_rows
    ]

def par_matrix_multiply(a: Matrix, b: Matrix, num_processes: Optional[int] = None) -> Matrix:
    rows_a, cols_a = matrix_dims(a)
    rows_b, cols_b = matrix_dims(b)

    if (not num_processes or num_processes < 2) or rows_a * cols_a * rows_b * cols_b < pow(60, 4) :
        return seq_matrix_multiply(a, b)

    if cols_a != rows_b:
        raise ArithmeticError("Cannot multiply {}x{} with {}x{} matrix".format(rows_a, cols_a, rows_b, cols_b))
    
    # Precalculate transposes
    b_T = matrix_transpose(b)
    with ProcessPoolExecutor(max_workers=num_processes) as pool:
        rows_per_process = int(rows_a / num_processes)
        matrix_chunks: List[Future] = []
        start = 0

        # Fork
        for _ in range(num_processes - 1):
            end = start + rows_per_process
            rows = a[start:end]
            start = end
            matrix_chunks.append(pool.submit(_matrix_multiply, rows, b_T))

        # Last chunk
        matrix_chunks.append(pool.submit(_matrix_multiply, a[start:], b_T))

        # Join
        result: Matrix = []
        for chunk in matrix_chunks:
            result.extend(chunk.result())

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
    NUMBER_OF_RUNS = 3
    PROCESS_COUNT = mp.cpu_count()
    MATRIX_SIZE = 500

    print('Measuring matrix multiplication speedup with {}x{} matrices using {} processes.'.format(MATRIX_SIZE, MATRIX_SIZE, PROCESS_COUNT))
    a = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]
    b = [[random.random() for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]

    seq_time = time_it("Sequential", NUMBER_OF_RUNS, seq_matrix_multiply, a, b)
    par_time = time_it("Parallel", NUMBER_OF_RUNS, par_matrix_multiply, a, b, PROCESS_COUNT)

    time_saved = seq_time - par_time
    speedup = seq_time / par_time
    efficiency  =  speedup / PROCESS_COUNT
    print('Saved', int(time_saved * 1000), 'ms', 'Speedup was', round(speedup, 2), 'Efficiency', round(efficiency * 100, 2), '%')
