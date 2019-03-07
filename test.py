def person(name, age, *, city, addr):
    print('name:', name, 'age:', age, 'other:', kw, city, age)
    kw['m'] = '7'
    print('name:', name, 'age:', age, 'other:', kw)


dict = {'m': 1}

person('Bob', 35, **dict)
print(dict)