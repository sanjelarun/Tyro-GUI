def myadd(a=1, b=2, c=3):
    if a > 7:
        return -1
    return a + b + c

## MAIN STARTS HERE
s = 0
for i in range(10):
    for k in range(i):
        print(k)
        for z in range(k):
            print ("Hello")
            for hello in range(z):
                print("3rd level")
        a = 10
        d = 1000
    b = 2 + 3
    j = 0
    if i > 5:
        s += myadd(i, i * i, i ** 3)
    else:
        s -= myadd(i, i * i, i ** 3)
        for j in range(i):
            s *= 2
    for j in range(100):
        print(j)
        for h in range(i):
            print("Now this is complex")
print(s)
