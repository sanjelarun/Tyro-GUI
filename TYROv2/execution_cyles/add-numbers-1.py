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
