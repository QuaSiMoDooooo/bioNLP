# 确定工作目录
import os
os.getcwd()
os.chdir("/home/wtian/bioNLP/step2-get-entities")

# 载入上一步得到的数据
import pickle
with open("../step1-papers_target/data.pkl",'rb') as f:
    data = pickle.load(f)
# data.keys()
# len(data['paper_target'])
paper_target = data['paper_target']
tokens_target = data['tokens_target']

# 获取实体
# 以 37716352.txt 为例
import nltk
paper_target.index('37716352.txt')
tokens_test = tokens_target[paper_target.index('37716352.txt')]
tagged_test = nltk.pos_tag(tokens_test)
tagged_test

# # 某列表由多个元组组成，找出所有元组分第一个中包含”vacc“的元素
for tup in tagged_test:
    if "vacc" in tup[0]:
        print(tup[0])
        print(tup[1])

# 需要3个部分实体内容
# 疫苗 病毒 后遗症
# 疫苗和病毒可以直接用相关语料列表提取，主要是这个后遗症
# 1 先试试看能不能直接用HPO的本体获取到
# 2 若不行 看看HPO是如何富集的 能从基因富集到疾病吗
# https://www.genenames.org/download/archive/
# Current tab separated hgnc_complete_set file ：
# https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt

# HPO。。。

# genes

import pandas as pd
gene_df = pd.read_csv("hgnc_complete_set.txt",sep='\t',low_memory=False)
gene_df.head()
gene_list = gene_df["symbol"]
gene_list  # 全大写
gene_list = [gene.lower() for gene in gene_list]

# 在paper_taget上进一步提取提到基因的文章
paper_target2 = []
tokens_target2 = []
genes_target2 = []
len(paper_target)  # 1075
for i in range(len(paper_target)):
    genes_target = []
    for gene in gene_list:
        if gene in tokens_target[i]:
            genes_target.append(gene)
    if len(genes_target) != 0:
        paper_target2.append(paper_target[i])
        genes_target2.append([gene.upper() for gene in genes_target])  # 保存大写 因为可能拿去富集
        tokens_target2.append(tokens_target[i])

print(len(paper_target2))  # 671
# 需要注意手动检查 去除一些伪基因token 如 IMPACT SET JUN 等

# 但这些疾病不一定与后遗症相关，而可能与病毒感染相关
# 虽然是通过vaccine相关词汇提取出来的paper_target
# 。。。

# 临时保存 提取出来有基因的
# 保存结果
os.getcwd()
import pickle
data = {"paper_target2":paper_target2,"tokens_target2":tokens_target2,"genes_target2":genes_target2}
# data.keys()
with open("paper_target_with_gene.pkl",'wb') as f:
    pickle.dump(data, f)

# python讲多个列表组成的列表中的所有元素整理到一个列表中，并进行去重操作，并写到文件再作为一列
flat_gene_list = list(set([item for sublist in genes_target2 for item in sublist]))
flat_gene_list
# 将列表写入文件
with open('flat_gene_list.txt', 'w') as file:
    for item in flat_gene_list:
        file.write(str(item) + '\n')