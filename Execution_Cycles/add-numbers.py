def myadd(a=1, b=2, c=3):
    return a + b + c


s = 0
for i in range(10):
    s += myadd(i, i * i, i ** 3)

print(s)
