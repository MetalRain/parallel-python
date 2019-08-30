# Parallel python

This repo contains my responses for challenges in course: *Parallel and Concurrent Programming with Python 2*.
https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2

## Matrix multiplication

Challenge: https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2/challenge-matrix-multiply-in-python

[Code](./matrix_multiplication.py)

Run with `python matrix_multiplication.py`

I created process pool that processes one row of output matrix in one task. I precalculated transpose for second matrix so that each element of output was just dot product.

When I ran this program in my machine (VM) with 4 cores I got speedup of 3.9 to 4.8 Since speedup is bigger than number of cores, there must be some changes in parallel version could benefit the sequential version as well.