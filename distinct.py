# 1.获取list
# 2.遍历list，取对应md5值，存入dict

import os
import shutil
from hashlib import sha1

dir = os.path.abspath('/Users/gujin/Downloads/图灵程序设计丛书')


# 定义计算shasum
def getSha1(filename):
    sha1Obj = sha1()
    with open(filename, 'rb') as f:
        sha1Obj.update(f.read())
    return sha1Obj.hexdigest()


# 获取pdf路径并计算出对应md5值，存储到pdf_dict
pdf_name = os.listdir(dir)
pdf_dict = {}
pdf_list = []
# 获取pdf的绝对路径
for i in pdf_name:
    pdf_list.append(os.path.join(dir, i))

# 计算sha
for x in pdf_list:
    pdf_dict[x] = getSha1(x)

# 去重
pdf_dict_new = {v: k for k, v in pdf_dict.items()}
pdf_dict_new1 = {v: k for k, v in pdf_dict_new.items()}

# 查看差集
print(pdf_dict.keys() - pdf_dict_new1.keys())

L = [x for x in pdf_dict.keys() and not in pdf_dict_new1.keys()]
print(L)
# 将重复文件删除
print(type(duplicates),duplicates)