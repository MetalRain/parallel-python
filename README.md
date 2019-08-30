# Parallel python

This repo contains my responses for challenges in course: Parallel and Concurrent Programming with Python 2.
https://www.linkedin.com/learning/parallel-and-concurrent-programming-with-python-2

## Matrix multiplication

[Code](./matrix_multiplication.py)

I created process pool that processes one row of output matrix in one task. For my machine anything over two processes was getting similar 1.34 speedup so I just used two processes.