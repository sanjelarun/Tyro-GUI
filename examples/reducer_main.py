def check(num, i, n):
    return ((num * i) + n) / (i + 1)


def avg(numbers):
    num = 0
    b = list(range(len(numbers)))
    for i in b:
        num = check(num, i, numbers[i])
    return num

numbers = [1, 52, 3, 4, 6, 5, 10]
print(avg(numbers))
print(sum(numbers)/len(numbers))