import nltk
from nltk.corpus import wordnet,stopwords
from nltk.stem import PorterStemmer
from string import punctuation
import os

# 确定工作目录
os.getcwd()
os.chdir("/home/wtian/bioNLP/step1-papers_target")

# 从疫苗入手先直接对摘要分词
vaccine_about = ["vaccin","vaccine","vaccination","coronavac","pfizer","covaxin","moderna"]
# 相似词
# brown  # 不好
# wordnet
for each in vaccine_about:
    print("\nThe similar words for \"{}\" in WordNet include: ".format(each))
    synonyms = []
    for syn in wordnet.synsets(each):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    # print(synonyms)
vaccine_about = ["vaccin","vaccine","vaccination","vaccinum","coronavac","pfizer","covaxin","moderna"]

# 这个其实还根据后面的结果如stem和第二部获取实体的效果进行了调整
# [stemmer.stem(token) for token in vaccine_about]
#  # ['vaccin', 'vaccin', 'vaccin', 'vaccinum', 'coronavac', 'pfizer', 'covaxin', 'moderna']
vaccine_about = ["vaccin","vaccinum","coronavac","pfizer","covaxin","moderna"]

# 提取出分词中存在vaccine_about中元素的paper_taget和对应的tokens
paper_target = []
tokens_target = []
abstract_path = "../pubmed/abstract/abstract_doc"
for file_name in os.listdir(abstract_path):
    # print(file_name)
    # break

    file_path = os.path.join(abstract_path,file_name)
    abstract = open(file_path,'r',encoding='utf-8').read()
    abstract = abstract.replace('\n',' ')

    # 初步分词
    tokens = nltk.word_tokenize(abstract)
    tokens = [token.lower() for token in tokens]
    # tokens

    # 清洗

    # 去掉停用词
    # stopwords.readme().replace('\n', ' ')
    # stopwords.fileids()
    # stopwords.raw('english').replace('\n',' ')
    # print(len(tokens))
    tokens2 = [token for token in tokens if token not in stopwords.words('english')]
    # print(len(tokens2))

    # 去掉符号
    # print(len(tokens2))
    tokens3 = [token for token in tokens2 if token not in punctuation]
    # print(len(tokens3))
    # tokens3

    # stem
    stemmer = PorterStemmer()
    tokens4 = [stemmer.stem(token) for token in tokens3]
    # tokens4

    # 判断token4中是否存在vaccine_about中元素
    # 提取出对应的paper_target和tokens_target
    for token in vaccine_about:
        if token in tokens4:
            paper_target.append(file_name)
            tokens_target.append(tokens4)
            # print(paper_target)
            # print(tokens_target)
            break  # 只要有一个元素存在就直接提出来

    # break  # 单个测试文件
print(len(paper_target))  # 1075

# 保存结果
os.getcwd()
import pickle
data = {"paper_target":paper_target,"tokens_target":tokens_target}
# data.keys()
with open("data.pkl",'wb') as f:
    pickle.dump(data, f)

