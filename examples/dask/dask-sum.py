import dask
import dask.bag as db


def myadd(a=1, b=2, c=3):
    return a + b + c


a = db.from_sequence(range(60), npartitions=2)
x = a.sum().compute(scheduler='threads')
print(x)
