# User Defined Function to add two numbers similar to a reducer
def add(a,b):
    return a + b

nums = [1,2,3,4,5]
s = 0
for i in nums:
    s += add(s,i)
print(s)
