# Parallel python

This repo contains my responses for challenges in course: *Parallel and Concurrent Programming with Python 2*.
https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2

## Matrix multiplication

Challenge: https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2/challenge-matrix-multiply-in-python

[Code](./matrix_multiplication.py)

Run with `python matrix_multiplication.py`

I created process pool that processes one row of output matrix in one task. I precalculated transpose for second matrix so that each element of output was just dot product.

Output from my machine:
```
(venv) otto@otto-VirtualBox:~/repos/parallel-python$ python matrix_multiplication.py 
Measuring matrix multiplication speedup with 500x500 matrices using 4 processes.
Running Sequential for 3 times
Sequential run for 21664 ms on average.
Running Parallel for 3 times
Parallel run for 8675 ms on average.
Saved 12988 ms Speedup was 2.5 Efficiency 62.43 %
```

I saw smaller speedups with smaller matrix sizes, like speedup of 2 with 100x100 matrix. Current implementation probably crates too many tasks and keeps copying more data (row and matrix) over and over again.