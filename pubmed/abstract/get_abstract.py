# 读取14895篇（截至2023.10.10）文章的PMID
# https://www.ncbi.nlm.nih.gov/research/coronavirus/docsum?filters=e_condition.LongCovid

import pandas as pd
import numpy as np
import os
import glob
import time
# import multiprocessing
# from joblib import Parallel,delayed
# from argparse import ArgumentParser
from Bio import Entrez
Entrez.email = "fabien012390wt@163.com"

# 设置工作路径
os.chdir("/home/wtian/bioNLP/pubmed/abstract/")

# parser = ArgumentParser()
# parser.add_argument(
#     '--sid_path',
#     help='pmid sub doc path',
#     type=str,
#     dest='sid_path'
# )
# args=parser.parse_args()
# sid_path = args.sid_path

# 所有pmid测试
# os.chdir("/home/wtian/bioNLP/pubmed/abstract/")
pmid = pd.read_csv("./pmid.tsv",sep="\t")
# pmid.head()
id = pmid["pmid"]
# id.head()
# type(id)  # <class 'pandas.core.series.Series'>
# len(id)  # 14895
# len(id.unique())  # 14895
# # 无重复pmid

# 读取当前sub pmid
# pmid = pd.read_csv(sid_path,sep="\t",header=None)
# id = pmid.iloc[:,0]

# 获得了感兴趣的文献的ID列表，就可以使用Entrez库来下载这些文献的摘要或全文
# 摘要

doc_path = "./abstract_doc"
if not os.path.exists(doc_path):
    os.makedirs(doc_path)

def get_abstract(id):
    file_path = doc_path + "/" + str(id) + ".txt"
    handle = Entrez.efetch(db="pubmed", id=id, rettype="abstract", retmode="text")
    abstract = handle.read()
    handle.close()
    with open(file_path, "w") as f:
        f.write(abstract)

# 测试 37813579
# get_abstract(37813579)
# 成功

# 获取全部14895篇文献摘要
# 考虑并行，否则太慢

# 1 #
# multiprocessing可以用并且非常快 但没让我指定并行/线程数量 我有点慌
# https://mp.weixin.qq.com/s/y8ex70Hr279nsvjWd5cY8g
# pool = multiprocessing.Pool()
# results = pool.map(get_abstract,id)
# pool.close()
# pool.join()

# 2 #
# 指定线程
# https://mp.weixin.qq.com/s/c2ZbW5BnvsT0qbCa8GQ8tQ
# processes_count = 10
# processes_pool = multiprocessing.Pool(processes=processes_count)
# processes_pool.map(get_abstract, id)
# 但是运行一段时间大概1200-1400个后就报错：
# multiprocessing.pool.MaybeEncodingError: Error sending result: '<multiprocessing.pool.ExceptionWithTraceback object at 0x7fc51242f880>'. Reason: 'TypeError("cannot pickle '_io.BufferedReader' object")'

# 3 #
# 将14895分割成15个子文件 手动跑15个进程算了
# ![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231011114918.png)
# for i in id:
#     get_abstract(i)
# urllib.error.HTTPError: HTTP Error 429: Too Many Requests
# 太多请求。。

# 4 #
# 将14895分割成15个子文件 不一次跑15个进程（不放到后台 &）
# 修改mian.sh脚本 每次跑一个子文件 但每个子文件进程指定10个线程
# processes_count = 10
# processes_pool = multiprocessing.Pool(processes=processes_count)
# processes_pool.map(get_abstract, id)
# 还是会出现：
# multiprocessing.pool.MaybeEncodingError: Error sending result: '<multiprocessing.pool.ExceptionWithTraceback object at 0x7fc51242f880>'. Reason: 'TypeError("cannot pickle '_io.BufferedReader' object")'

# 5 #
# 算了我放弃了懒得想
# 还是一个个下载，哪里断了还可以续上

# 考虑可能中途中断：
file_pattern = os.path.join(doc_path,"*")
files = glob.glob(file_pattern)
files_num = len(files)
print(files_num)
print(len(id))  # 14895
for index in range(files_num,14895):
    i = id[index]
    print(i)
    get_abstract(int(i))
