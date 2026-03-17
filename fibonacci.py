# Fibonacci sequence - first 10 numbers

def fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# Print the first 10 Fibonacci numbers
fib_numbers = fibonacci(10)
print("Fibonacci sequence (first 10 numbers):")
print(fib_numbers)
