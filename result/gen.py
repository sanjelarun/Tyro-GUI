import pyspark as ps
def udf(accum, num): 
	return (( accum[0] * num[1] ) + num[0] ) / ( num[1] + 1 ),0
def check(num, i, n):
    return ((num * i) + n) / (i + 1)


def avg(numbers):
    num = 0
    b = list(range(len(numbers)))
    sc = ps.SparkContext()
    num_RDD_0 = sc.parallelize(b)
    num_RDD_1 = sc.parallelize(numbers)
    num_RDD_2 = num_RDD_1.zip(num_RDD_0)
    num = num_RDD_2.map(lambda x: (1, (x[0],  x[1]))).reduceByKey(udf).collect()
    return num

numbers = [1, 52, 3, 4, 6, 5, 10]
print(avg(numbers))
print(sum(numbers)/len(numbers))