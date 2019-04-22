> 面向对象设计原则-开放封闭原则，对于扩展是开放的，对于修改是封闭的。
> <a>https://www.cnblogs.com/songwenjie/p/9559889.html</a>

在`Python`中，函数是一种非常灵活的结构，我们可以把它赋值给变量、当作参数传递给另一个函数，或者当成某个函数的输出。装饰器本质上也是一种函数，它可以让其它函数在不经过修改的情况下增加一些功能。

这也就是「装饰」的意义，这种「装饰」本身代表着一种功能，如果用它修饰不同的函数，那么也就是为这些函数增加这种功能。

一般而言，我们可以使用装饰器提供的`@`语法糖(`Syntactic Sugar`)来修饰其它函数或对象。如下所示我们用`@dec`装饰器修饰函数`func ()`
```python
@dec
def func():
    pass
```
#### 1. 设置问题
为了解装饰器的目的，接下来我们来看一个简单的示例。假如你有一个简单的加法函数`dec.py`，第二个参数的默认值为 10：
```python
def add(x, y=10):
    return x + y
```
我们来更认真的看一下这个加法函数：
```python
>>> add(10, 20)
30
>>> add
<function add at 0x7fce0da2fe18>
>>> add.__name__
'add'
>>> add.__module__
'__main__'
>>> add.__defaults__ # default value of the `add` function
(10,)
>>> add.__code__.co_varnames # the variable names of the `add` function
('x', 'y')
```
我们无需理解这些都是什么，只需要记住`Python`中的每个函数都是对象，它们有各种属性和方法。你还可以通过`inspect`模块查看`add()`函数的源代码：
```python
>>> from inspect import getsource
>>> print(getsource(add))

def add(x, y=10):
    return x + y
```
现在你以某种方式使用该加法函数，比如你使用一些操作来测试该函数：
```python
def add(x, y=10):
    return x + y

print('add(10)', add(10))
print('add(20, 30)', add(20, 30))
print('add("a", "b")', add("a", "b"))

Output：
add(10) 20
add(20, 30) 50
add("a", "b") ab
```
假设你想了解每个`print`执行所花费的时间，可以调用time模块：
```python
from time import time

def add(x, y=10):
    return x + y

before = time()
print('add(10)',         add(10))
after = time()
print('time taken: ', after - before)
before = time()
print('add(20, 30)',     add(20, 30))
after = time()
print('time taken: ', after - before)
before = time()
print('add("a", "b")',   add("a", "b"))
after = time()
print('time taken: ', after - before)
Output:

add(10) 20
time taken:  0.00019693374633789062
add(20, 30) 50
time taken:  1.0013580322265625e-05
add("a", "b") ab
time taken:  6.9141387939453125e-06
```
现在代码可读性不强，如果你想改变什么，你就得修改所有地方。
我们也可以按照如下方法，直接在add函数中捕捉运行时间：
```python
from time import time

def add(x, y=10):
    before = time()
    rv = x + y
    after = time()
    print('time taken: ', after - before)
    return rv

print('add(10)',         add(10))
print('add(20, 30)',     add(20, 30))
print('add("a", "b")',   add("a", "b"))
```
这种方法肯定比前一种要好。但是如果你还有另一个函数，那么这似乎就不方便了。当我们有多个函数时，就要全部修改，这并不是你想要的：
```python
from time import time

def add(x, y=10):
    before = time()
    rv = x + y
    after = time()
    print('time taken: ', after - before)
    return rv

def sub(x, y=10):
    return x - y

print('add(10)', add(10))
print('add(20, 30)', add(20, 30))
print('add("a", "b")', add("a", "b"))
print('sub(10)', sub(10))
print('sub(20, 30)', sub(20, 30))
```
因为`add`和`sub`都是函数，我们可以利用这一点写一个`timer`函数。我们希望`timer`能计算一个函数的运算时间。如何做到呢，分析一下：
这个`timer`函数需要传入3个值：
- 1. 需要传入`需要计算运行时间的函数`
- 2. 需要传入`需要计算运行时间的函数的参数x`
- 3. 需要传入`需要计算运行时间的函数的参数y`
这并不难理解
```python
def timer(func, x, y=10):
    before = time()
    rv = func(x, y)
    after = time()
    print('time taken: ', after - before)
    return rv
```
这很不错，不过我们必须调用`timer`函数来包装不同的函数：
```python
from time import time


def add(x, y=10):
    return x + y


def sub(x, y=10):
    return x - y


def timer(func, x, y=10):
    before = time()
    rv = func(x, y)
    after = time()
    print('time taken: ', after - before)
    return rv


print('add(10)', timer(add, 10))
print('sub(10)', timer(sub, 10))
```
这样看上去清爽很多了吧，但是你有没有发现问题？如果`y`的默认值不是10咋办？试着修改`y`的默认值，你会发现得不到你想要的结果了。如何做的更好呢？

这里有一个主意：创建一个新的`timer`函数，并包装其他函数，然后返回包装后的函数：
```python
def timer(func):
    def f(x, y=10):
        before = time()
        rv = func(x, y)
        after = time()
        print('time taken: ', after - before)
        return rv
    return f
```
现在，你只需要用`timer`包装一下`add`和`sub`函数,这样一来新的`add`和`sub`函数都具有了计算运行时间的功能：
```python
add = timer(add)
sub = timer(sub)
```
以下是完整代码：
```python
from time import time


def timer(func):
    def f(x, y=10):
        before = time()
        rv = func(x, y)
        after = time()
        print('time taken: ', after - before)
        return rv
    return f


def add(x, y=10):
    return x + y
add = timer(add)


def sub(x, y=10):
    return x - y
sub = timer(sub)

print('add(10)', add(10))
print('add(20, 30)', add(20, 30))
print('add("a", "b")', add("a", "b"))
print('sub(10)', sub(10))
print('sub(20, 30)', sub(20, 30))


Output:

time taken:  1.1920928955078125e-06
add(10) 20
time taken:  1.1920928955078125e-06
add(20, 30) 50
time taken:  9.5367431640625e-07
add("a", "b") ab
time taken:  9.5367431640625e-07
sub(10) 0
time taken:  0.0
sub(20, 30) -10
```
我们来总结一下这个过程：我们有一个函数（比如`add`函数），然后用一个动作（比如计时）包装该函数。包装的结果是一个新函数，能实现某些新功能。

当然了，默认值还有点问题，稍后我们会解决它。

#### 2. 装饰器
现在，上面的解决方案以及非常接近装饰器的思想了，使用常见行为包装某个具体的函数，这种模式就是装饰器在做的事。我们可以使用`@`语法糖来修饰一个函数或者对象，对比一下使用装饰器前后的代码：
```python
from time import time

def timer(func):
    def f(x, y=10):
        before = time()
        rv = func(x, y)
        after = time()
        print('time taken: ', after - before)
        return rv
    return f

# 使用装饰器之前
def add_1(x, y=10):
    return x + y
add_1 = timer(add_1)

# 使用装饰器之后
@timer
def add_2(x, y=10):
    return x + y

print('add_1(10)', add_1(10))
print('add_2(10)', add_2(10))

Output:
time taken:  9.5367431640625e-07
add_1(10) 20
time taken:  9.5367431640625e-07
add_2(10) 20
```
它们的作用是一样的，这就是`Python`装饰器的作用。它实现的作用类似于 `add = timer(add)`，只不过装饰器把句法放在函数上面，且句法更加简单`@timer`。现在你计算`sub`函数的运行时间，只需使用`timer`装饰器了。
```python
@timer
def sub(x, y=10):
    return x - y
```

#### 3. 参数和关键字参数
现在，还有一个小问题没有解决。在`timer`函数中，我们将参数`x`和`y`写死了，即指定`y`的默认值为`10`。有一种方法可以传输该函数的参数和关键字参数，即`*args`和`**kwargs`。参数是函数的标准参数（在本例中`x`为参数），关键字参数是已具备默认值的参数（本例中是`y=10）。代码如下：
```python
from time import time
def timer(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print('time taken: ', after - before)
        return rv
    return f

@timer
def add(x, y=10):
    return x + y

@timer
def sub(x, y=10):
    return x - y
```
现在，该`timer`函数可以处理任意函数、任意参数和任意默认值设置了，因为它仅仅将这些参数传输到函数中。

#### 4. 高阶装饰器
你可能会疑惑：如果我们可以用一个函数包装另一个函数来添加有用的行为，那么我们可以再进一步吗？我们用一个函数包装另一个函数，再被另一个函数包装吗？

可以！事实上，函数的深度可以随你的意。
<a>https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014318435599930270c0381a3b44db991cd6d858064ac0000</a>
