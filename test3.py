# def f(x):
#     return x * x

# l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# a = map(f, l)
# print(list(a))


def ntimes(n):
    def inner(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                rv = func(*args, **kwargs)
                return rv
            return wrapper
    return inner


# 使用装饰器之后
@ntimes(3)
def add(x, y=10):
    return x + y


print('add(10)', add(10))
