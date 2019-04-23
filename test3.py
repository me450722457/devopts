def ntimes(n):
    def inner(f):
        def wrapper(*args, **kwargs):
            '''
            wrapper
            '''
            for _ in range(n-1):
                rv = f(*args, **kwargs)
            return rv

        return wrapper

    return inner


@ntimes(3)
def add(x, y):
    '''
    add
    '''
    print(x + y)
    return x + y


print(add(10, 20))
print(add.__doc__)
print(add.__name__)