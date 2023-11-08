# algorithm.py

def factorial(n):   #숫자가 들어가는 부분
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

