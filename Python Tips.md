#### 1.条件判断
```python
condition=True
if condition:
    x=1
else:
    x=2
print (x)
```
改成
```python
x = 1 if condition else 2
```

#### 2.大数字分割
如果几个非常大的数字比如相加的时候，一个数字后面很多零点时候，我们很难去点这个0，比如：
```python
num1=10000000000
num2=100000000
print (num1+num2)
```
上面的几个大数字，很多零，点的眼都花了！怎么办呢，Python里面有一个奇淫技巧，可以加下划线分割：
```python
num1=10_000_000_000
num2=100_000_000
total=num1+num2
print (f'{total:,}')
>>10,100,000,000
```

#### 3.文件的关闭
```python
f=open('log.txt','r')
file_contents=f.read()
f.close()

words=file_contents.split(' ')
word_count=len(words)
print (word_count)
```
用with来处理更简便
```python
with open('log.txt','r') as f:
    file_contents=f.read()
    words=file_contents.split(' ')
    word_count=len(words)
    print(word_count)
```

#### 4.下标
```python
names=['Corey','Chris','Dave','Apple']
index=0
for name in names:
    print (index,name)
index+=1
```
使用enumerate来计算下标
```python
names=['Corey','Chris','Dave','Apple']
for index,name in enumerate(names):
    print (index,name)
```

#### 5.遍历多个序列
```python
names=['Leo','Lili','Sam','Tom']
ages=[30,20,28,25]
for index,name in enumerate(names):
    age=ages[index]
    print (f'{name} is {age} old')
```
太麻烦了，用`zip`更方便
```python
for name ,age in zip(names,ages):
    print (f'{name} is {age} old')
```
有的同学说如果我有3个序列呢，怎么办，一样可以操作
```python
names=['Leo','Lili','Sam','Tom']
ages=[30,20,28,25]
habits=['Movies','Dance','Reading','Singing']
for name ,age,habit in zip(names,ages,habits):
    print (f'{name} is {age} old and like {habit}')
```

#### 6.巧妙的使用单下划线

我们在一个序列的时候，有的时候，只想取头和尾，巧妙的用单下划线
```python
a,_,b=(1,2,3)
print (a)
print (b)
>>
1
3
```
但是如果有一个很长的序列的时候，我们想取头和尾怎么办呢，传统的做法是:
```python
nums=(1,2,3,4,5,6,7,8,9)
head=nums[0]
tail=nums[-1]
print (head)
print (tail)
```
如果能巧妙的利用`unpack`方法，就会很简便:
```python
nums=(1,2,3,4,5,6,7,8,9)
head,*_,tail=nums
print (head)
print (tail)
```

#### 7.类的属性封装
```python
class Person():
    pass
person=Person()
```
如果你有一个字典需要来初始化这个类
```python
person_info={'first':'leo','last':'sam'}
```
你希望最后能`print (person.first)`,怎么办？有没有什么巧妙的方法处理？

用`setattr`函数
```python
for k,v in person_info.items():
    setattr(person,k,v)
```
还有`getattr()`,可以方便的获取类的属性
```python
for k in person_info.keys():
    print (getattr(person,k))
```

#### 8.输入加密的密码
```python
username=input('Username: ')
passwd=input('Passwd:')
print ('Logging In...')
>>
Username: user
Passwd:admin
Logging In...
```
密码是显示出来的，这样肯定不太好，有没有其他优雅的方法的，用`Python`自带的函数`getpass`
```python
from getpass import getpass
username=input('Username: ')
passwd=getpass('Passwd:')
print ('Logging In...')
>>
Username: aa
Passwd:
Logging In...
```
这里`passwd`后面会显示一个钥匙的图片