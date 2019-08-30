# Parallel python

This repo contains my responses for challenges in course: *Parallel and Concurrent Programming with Python 2*.
https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2

## Matrix multiplication

Challenge: https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2/challenge-matrix-multiply-in-python

[Code](./matrix_multiplication.py)

Run with `python matrix_multiplication.py`

Output from my machine:
```
(venv) otto@otto-VirtualBox:~/repos/parallel-python$ python matrix_multiplication.py
Measuring matrix multiplication speedup with 500x500 matrices using 4 processes.
Running Sequential for 3 times
Sequential run for 21585 ms on average.
Running Parallel for 3 times
Parallel run for 5600 ms on average.
Saved 15984 ms Speedup was 3.85 Efficiency 96.35 %
```

When I split work into more tasks (per row) I got much worse speedups. Splitting work even more finely (per cell) made parallel version slower than sequential one.