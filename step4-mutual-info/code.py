# 前面我们已经获得了 疫苗和疾病相关的实体
# 1075 疫苗 1072 疾病
# 这里看一下有多少篇有特定的病毒

# 确定工作目录
import os
os.getcwd()
os.chdir("/home/wtian/bioNLP/step4-mutual-info")

# 载入上一步得到的数据
import pickle
with open("../step1-papers_target/data.pkl",'rb') as f:
    data = pickle.load(f)
# data.keys()
# len(data['paper_target'])
paper_target = data['paper_target']  # 1075篇目标文章
tokens_target = data['tokens_target']

# tokens_target为所有疫苗相关的pmid
# 1.分类提取各疫苗对应的pmid
coronavac = []
pfizer = []
astrazeneca = []
moderna = []
covaxin = []
vaccines_list = ["coronavac","pfizer","astrazeneca","moderna","covaxin"]
for i in range(len(tokens_target)):
    tokens = tokens_target[i]
    if "coronavac" in tokens:
        coronavac.append(paper_target[i])
    if "pfizer" in tokens:
        pfizer.append(paper_target[i])
    if "astrazeneca" in tokens:
        astrazeneca.append(paper_target[i])
    if "moderna" in tokens:
        moderna.append(paper_target[i])
    if "covaxin" in tokens:
        covaxin.append(paper_target[i])

len(coronavac)  # 效果不好 不知道为什么 看数据库大号的lebels应该是最多的？
len(pfizer)
len(astrazeneca)
len(moderna)
len(covaxin)
# >>> len(coronavac)
# 3
# >>> len(pfizer)
# 231
# >>> len(astrazeneca)
# 89
# >>> len(moderna)
# 22
# >>> len(covaxin)
# 2


# 2.分类提取各病毒亚型对应的pmid
omicron = []
delta = []
alpha = []
beta = []
gamma = []
variants_list = ["omicron","delta","alpha","beta","gamma"]
for i in range(len(tokens_target)):
    tokens = tokens_target[i]
    if "omicron" in tokens:
        omicron.append(paper_target[i])
    if "delta" in tokens:
        delta.append(paper_target[i])
    if "alpha" in tokens:
        alpha.append(paper_target[i])
    if "beta" in tokens:
        beta.append(paper_target[i])
    if "gamma" in tokens:
        gamma.append(paper_target[i])

len(omicron) 
len(delta)
len(alpha)
len(beta)
len(gamma)
# >>> len(omicron) 
# 56
# >>> len(delta)
# 35
# >>> len(alpha)
# 16
# >>> len(beta)
# 7
# >>> len(gamma)
# 2

# 发现直接提取关键词
# 疫苗相关往往找到比官网打好的lebels多
# 病毒相关往往找到比官网打好的lebels少

# 3.尝试提取同时出现5 X 5组合的pmid
vaccines_list = ["coronavac","pfizer","astrazeneca","moderna","covaxin"]
variants_list = ["omicron","delta","alpha","beta","gamma"]
import numpy as np
import pandas as pd
# 创建初始的全零矩阵
matrix = [[0, 0, 0, 0, 0] for _ in range(5)]
# 创建数据框 指定行和列的名称
df = pd.DataFrame(matrix, columns=vaccines_list, index=variants_list)
print(df)

def get_both_occur_pmid(vaccine, variant):
    global df
    for i in range(len(tokens_target)):
        tokens = tokens_target[i]
        if vaccine in tokens and variant in tokens:
            df[vaccine][variant] += 1
    return

for i in vaccines_list:
    for j in variants_list:
        get_both_occur_pmid(i,j)
print(df)
#          coronavac  pfizer  astrazeneca  moderna  covaxin
# omicron          1      11            3        2        0
# delta            0       4            3        1        0
# alpha            0       3            1        0        0
# beta             0       0            0        0        0
# gamma            0       0            0        0        0     

len(omicron)+len(delta)+len(alpha)+len(beta)+len(gamma)
# 116

# 可以发现数据质量并不是很好
# 转化方向
# 展示：
# 计算pfizer+omicron和各种疾病的互信息 绘制词云和排名
# 其它的vaccine和variant分开计算互信息进行排名然后整合
# 5 X 5表格 各自最高的疾病
# 基因HPO结果

# 4.计算互信息
# 输入多个实体信息 统计频率 以计算互信息
# 若输入两个实体则是 eg：其它的vaccine和variant分开计算互信息进行排名然后整合
# 若输入三个实体则是 eg：计算pfizer+omicron和各种疾病的互信息 绘制词云和排名

# 读取每篇文章注释的mesh
with open("../step2-get-pubtator-annos/data.pkl",'rb') as f:
    data = pickle.load(f)
data.keys()
paper_target_uniq_MESH = data["paper_target_uniq_MESH"]
paper_target_uniq_MESH.values()
# 提取出所有mesh 合并 并保留唯一id 作为潜在关联后遗症 以进行后面的互信息计算
merge_list = []
for sublist in paper_target_uniq_MESH.values():
    merge_list.extend(sublist)
len(merge_list)  # 5487
merge_list_uniq = list(set(merge_list))
len(merge_list_uniq)  # 680
merge_list_uniq
# 去除列表中的nan
merge_list_uniq = pd.Series(merge_list_uniq).dropna().to_list()
len(merge_list_uniq) # 609
merge_list_uniq  # 唯一顺序 后面有用

# >>> paper_target.index("37287866.txt")
# 131
# >>> paper_target.index("36958743.txt")
# 254
# >>> paper_target.index("32492212.txt")
# 1066
def get_all_occur_pmid_num(token1,token2,token3=" "):
    # 因为要提取mesh 频率 所以不用1075 而是1072 直接在1075基础上过滤算了 免得顺序变了
    occur_num = 0
    if token3 == " ":
        for i in range(len(tokens_target)):
            if i not in [131,254,1066]:
                tokens = tokens_target[i]
                paper = paper_target[i]
                mesh_id = paper_target_uniq_MESH[paper]
                if token1 in tokens and token2 in mesh_id:
                    occur_num += 1
    else:
        for i in range(len(tokens_target)):
            if i not in [131,254,1066]:
                tokens = tokens_target[i]
                paper = paper_target[i]
                mesh_id = paper_target_uniq_MESH[paper]
                if token1 in tokens and token2 in tokens and token3 in mesh_id:
                    # 前两个实体在该文章摘要分词中 第三个实体（mesh）在该文章mesh id中
                    occur_num += 1
    return occur_num

import math
def cal_mutual_info(token1,mesh,N):  # 两个实体的互信息批量计算 包装函数
    p_token1 = len(token1) / N
    p_mesh = merge_list.count(mesh) / N
    p_2 = get_all_occur_pmid_num(token1,mesh) / N
    mutual_info = math.log2((p_2 / p_token1 / p_mesh)+1)  # 为避免log2 所以+1
    return mutual_info

# 获取mesh对应的疾病 函数
ref = pd.read_csv("../pubtator/ref_mesh_disease.tsv",header=None,sep="\t")
ref.head()
def get_mesh_disease(meshs):
    disease_list = [list(ref.loc[ref.iloc[:,1] == mesh, ref.columns[0]])[0] for mesh in meshs]
    return(disease_list)


##############正式计算################
# 1. 计算pfizer+omicron和各种疾病的互信息 绘制词云和排名
mesh_occur_num_list = []
for mesh in merge_list_uniq:
    mesh_occur_num_list.append(get_all_occur_pmid_num("pfizer","omicron",mesh))

mesh_occur_num_list
len(mesh_occur_num_list)  # 609 和前面merge_list_uniq对应
# 3个实体的互信息手算
N = 1075
p_pfizer = len(pfizer) / N
p_omicron = len(omicron) / N
# 某mesh 在merge_list中出现的次数其实就是该出现该mesh的文章数 因为我们前面每篇文章保留的mesh id 是唯一的
# 计算每个mesh的互信息：
mutual_info_p3 = []  # 保存609个unique mesh的互信息结果
for i in range(609):
    mesh = merge_list_uniq[i]
    p_mesh = merge_list.count(mesh) / N
    p_3 = mesh_occur_num_list[i] / N
    mutual_info = math.log2((p_3 / p_pfizer / p_omicron / p_mesh)+1)  # 为避免log2 所以+1
    mutual_info_p3.append(mutual_info)
mutual_info_p3

# 获得列表中从大到小元素的索引
sorted_indexes = [i for i, _ in sorted(enumerate(mutual_info_p3), key=lambda x: x[1], reverse=True)]
print(sorted_indexes)
# [487, 500, 456, 365, 34, 348, 286, 406, 584, 411, 590, 334, 300, 318, 575, 139, 237, 0, 1, 2, 3, 4, 5, 6 ...
len(sorted_indexes)
# 看看前10mesh对应的疾病
get_mesh_disease([merge_list_uniq[id] for id in sorted_indexes[:10]])
# 按互信息大小顺序
# ['hematological malignancies', 'dysgeusia', 'inability', 'cancer', 'pulmonary symptoms', 'olfactory loss', 'respiratory failure', 'myalgia', 'cough', 'depression']
# pfizer+omicron

# # 绘制词云
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# # 定义单词列表和权重列表
# words = get_mesh_disease([merge_list_uniq[id] for id in sorted_indexes])
# weights = [i for i in range(609,0,-1)]
# # 创建一个词云对象，设置词云的参数
# wordcloud = WordCloud(width=800, height=400, background_color="white")
# # 将单词列表和权重列表转换成字典
# word_weights = dict(zip(words, weights))
# # 生成词云
# wordcloud.generate_from_frequencies(frequencies=word_weights)
# # 保存
# wordcloud.to_file("wordcloud.png")
# # 显示词云图
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# 2. 其它的vaccine和variant分开计算互信息进行排名然后整合
vaccines_list = ["coronavac","pfizer","astrazeneca","moderna","covaxin"]
variants_list = ["omicron","delta","alpha","beta","gamma"]
len(merge_list_uniq)
merge_list_uniq

# 获取5组分别和各mesh的互信息前10的疾病
for i in range(5):
    for j in range(5):
        vaccine = vaccines_list[i]
        variant = variants_list[j]
        vaccine_mesh_mutual_info_list = []
        variant_mesh_mutual_info_list = []
        for mesh in merge_list_uniq:
            vaccine_mesh_mutual_info = cal_mutual_info(vaccine,mesh,1075)
            variant_mesh_mutual_info = cal_mutual_info(variant,mesh,1075)
            vaccine_mesh_mutual_info_list.append(vaccine_mesh_mutual_info)
            variant_mesh_mutual_info_list.append(variant_mesh_mutual_info)
        # 取前10mesh对应的疾病
        vaccine_mesh_sorted_indexes = [i for i, _ in sorted(enumerate(vaccine_mesh_mutual_info_list), key=lambda x: x[1], reverse=True)]
        variant_mesh_sorted_indexes = [i for i, _ in sorted(enumerate(variant_mesh_mutual_info_list), key=lambda x: x[1], reverse=True)]
        vaccine_disease_10 = get_mesh_disease([merge_list_uniq[id] for id in vaccine_mesh_sorted_indexes[:10]])
        variant_disease_10 = get_mesh_disease([merge_list_uniq[id] for id in variant_mesh_sorted_indexes[:10]])
        print(vaccine," ",variant)
        print(vaccine_disease_10)
        print(variant_disease_10)

# coronavac   omicron
# ['chemosensory disturbances', 'rheumatic diseases', 'impaired memory', 'diarrhea', 'heart failure', 'coronary heart disease', 'stroke', 'obesity', 'autoimmune disorder', 'chest tightness']
# ['lower lobe cystic', 'nasal obstruction', 'brachial plexopathy', 'epileptic seizures', 'atopic diseases', 'parasitic diseases', 'psychotic', 'traumatic intracranial hemorrhage', 'anosmia without rhinitis', 'MIS-C']
# coronavac   delta
# ['chemosensory disturbances', 'rheumatic diseases', 'impaired memory', 'diarrhea', 'heart failure', 'coronary heart disease', 'stroke', 'obesity', 'autoimmune disorder', 'chest tightness']
# ['lower lobe cystic', 'ALAD', 'Pulmonary Tuberculosis', 'brachial plexopathy', 'epileptic seizures', 'ALD', 'hemoptysis', 'traumatic intracranial hemorrhage', 'opportunistic infections', 'mitral insufficiency']
# coronavac   alpha
# ['chemosensory disturbances', 'rheumatic diseases', 'impaired memory', 'diarrhea', 'heart failure', 'coronary heart disease', 'stroke', 'obesity', 'autoimmune disorder', 'chest tightness']
# ['brachial plexopathy', 'epileptic seizures', 'Acute Stress', 'traumatic intracranial hemorrhage', 'mitral insufficiency', 'acute necrotizing encephalitis', 'zoonotic disease', 'psychotic', 'pericardial effusion', 'necrosis']
# coronavac   beta
# ['chemosensory disturbances', 'rheumatic diseases', 'impaired memory', 'diarrhea', 'heart failure', 'coronary heart disease', 'stroke', 'obesity', 'autoimmune disorder', 'chest tightness']
# ['insulin-dependent diabetes mellitus', 'DM', 'chronic bronchitis', 'mitral insufficiency', 'pericardial effusion', 'Pancreatitis', 'immunodeficiency virus-1 (HIV-1)', 'hypotension', 'skin rash', 'Gut Dysbiosis, Neuroinflammation']
# coronavac   gamma
# ['chemosensory disturbances', 'rheumatic diseases', 'impaired memory', 'diarrhea', 'heart failure', 'coronary heart disease', 'stroke', 'obesity', 'autoimmune disorder', 'chest tightness']
# ['immunodeficiency', 'infection', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# pfizer   omicron
# ['psoriasis', 'invasive fungal infection', 'colorectal cancer', 'cholestasis', 'liver disease', 'FND', 'deafness', 'leukocytosis', 'Appendicitis in Multisystem Inflammatory Syndrome', 'ECG abnormalities']
# ['lower lobe cystic', 'nasal obstruction', 'brachial plexopathy', 'epileptic seizures', 'atopic diseases', 'parasitic diseases', 'psychotic', 'traumatic intracranial hemorrhage', 'anosmia without rhinitis', 'MIS-C']
# pfizer   delta
# ['psoriasis', 'invasive fungal infection', 'colorectal cancer', 'cholestasis', 'liver disease', 'FND', 'deafness', 'leukocytosis', 'Appendicitis in Multisystem Inflammatory Syndrome', 'ECG abnormalities']
# ['lower lobe cystic', 'ALAD', 'Pulmonary Tuberculosis', 'brachial plexopathy', 'epileptic seizures', 'ALD', 'hemoptysis', 'traumatic intracranial hemorrhage', 'opportunistic infections', 'mitral insufficiency']
# pfizer   alpha
# ['psoriasis', 'invasive fungal infection', 'colorectal cancer', 'cholestasis', 'liver disease', 'FND', 'deafness', 'leukocytosis', 'Appendicitis in Multisystem Inflammatory Syndrome', 'ECG abnormalities']
# ['brachial plexopathy', 'epileptic seizures', 'Acute Stress', 'traumatic intracranial hemorrhage', 'mitral insufficiency', 'acute necrotizing encephalitis', 'zoonotic disease', 'psychotic', 'pericardial effusion', 'necrosis']
# pfizer   beta
# ['psoriasis', 'invasive fungal infection', 'colorectal cancer', 'cholestasis', 'liver disease', 'FND', 'deafness', 'leukocytosis', 'Appendicitis in Multisystem Inflammatory Syndrome', 'ECG abnormalities']
# ['insulin-dependent diabetes mellitus', 'DM', 'chronic bronchitis', 'mitral insufficiency', 'pericardial effusion', 'Pancreatitis', 'immunodeficiency virus-1 (HIV-1)', 'hypotension', 'skin rash', 'Gut Dysbiosis, Neuroinflammation']
# pfizer   gamma
# ['psoriasis', 'invasive fungal infection', 'colorectal cancer', 'cholestasis', 'liver disease', 'FND', 'deafness', 'leukocytosis', 'Appendicitis in Multisystem Inflammatory Syndrome', 'ECG abnormalities']
# ['immunodeficiency', 'infection', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# astrazeneca   omicron
# ['colorectal cancer', 'heart block', 'FND', 'partial lipodystrophy', 'change disease', 'developmental abnormalities', 'psychological dysfunction', 'ankle swelling', 'ADHD', 'focal segmental glomerulosclerosis']
# ['lower lobe cystic', 'nasal obstruction', 'brachial plexopathy', 'epileptic seizures', 'atopic diseases', 'parasitic diseases', 'psychotic', 'traumatic intracranial hemorrhage', 'anosmia without rhinitis', 'MIS-C']
# astrazeneca   delta
# ['colorectal cancer', 'heart block', 'FND', 'partial lipodystrophy', 'change disease', 'developmental abnormalities', 'psychological dysfunction', 'ankle swelling', 'ADHD', 'focal segmental glomerulosclerosis']
# ['lower lobe cystic', 'ALAD', 'Pulmonary Tuberculosis', 'brachial plexopathy', 'epileptic seizures', 'ALD', 'hemoptysis', 'traumatic intracranial hemorrhage', 'opportunistic infections', 'mitral insufficiency']
# astrazeneca   alpha
# ['colorectal cancer', 'heart block', 'FND', 'partial lipodystrophy', 'change disease', 'developmental abnormalities', 'psychological dysfunction', 'ankle swelling', 'ADHD', 'focal segmental glomerulosclerosis']
# ['brachial plexopathy', 'epileptic seizures', 'Acute Stress', 'traumatic intracranial hemorrhage', 'mitral insufficiency', 'acute necrotizing encephalitis', 'zoonotic disease', 'psychotic', 'pericardial effusion', 'necrosis']
# astrazeneca   beta
# ['colorectal cancer', 'heart block', 'FND', 'partial lipodystrophy', 'change disease', 'developmental abnormalities', 'psychological dysfunction', 'ankle swelling', 'ADHD', 'focal segmental glomerulosclerosis']
# ['insulin-dependent diabetes mellitus', 'DM', 'chronic bronchitis', 'mitral insufficiency', 'pericardial effusion', 'Pancreatitis', 'immunodeficiency virus-1 (HIV-1)', 'hypotension', 'skin rash', 'Gut Dysbiosis, Neuroinflammation']
# astrazeneca   gamma
# ['colorectal cancer', 'heart block', 'FND', 'partial lipodystrophy', 'change disease', 'developmental abnormalities', 'psychological dysfunction', 'ankle swelling', 'ADHD', 'focal segmental glomerulosclerosis']
# ['immunodeficiency', 'infection', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# moderna   omicron
# ['anhedonia', 'demyelination and gliosis', 'flushing', 'osteoarthritis', 'marginal zone lymphoma', 'chronic bronchitis', 'posthypoxic necrotizing leukoencephalopathy', 'gastroesophageal reflux disease', 'dyspepsia', 'chronic lymphocytic leukemia']
# ['lower lobe cystic', 'nasal obstruction', 'brachial plexopathy', 'epileptic seizures', 'atopic diseases', 'parasitic diseases', 'psychotic', 'traumatic intracranial hemorrhage', 'anosmia without rhinitis', 'MIS-C']
# moderna   delta
# ['anhedonia', 'demyelination and gliosis', 'flushing', 'osteoarthritis', 'marginal zone lymphoma', 'chronic bronchitis', 'posthypoxic necrotizing leukoencephalopathy', 'gastroesophageal reflux disease', 'dyspepsia', 'chronic lymphocytic leukemia']
# ['lower lobe cystic', 'ALAD', 'Pulmonary Tuberculosis', 'brachial plexopathy', 'epileptic seizures', 'ALD', 'hemoptysis', 'traumatic intracranial hemorrhage', 'opportunistic infections', 'mitral insufficiency']
# moderna   alpha
# ['anhedonia', 'demyelination and gliosis', 'flushing', 'osteoarthritis', 'marginal zone lymphoma', 'chronic bronchitis', 'posthypoxic necrotizing leukoencephalopathy', 'gastroesophageal reflux disease', 'dyspepsia', 'chronic lymphocytic leukemia']
# ['brachial plexopathy', 'epileptic seizures', 'Acute Stress', 'traumatic intracranial hemorrhage', 'mitral insufficiency', 'acute necrotizing encephalitis', 'zoonotic disease', 'psychotic', 'pericardial effusion', 'necrosis']
# moderna   beta
# ['anhedonia', 'demyelination and gliosis', 'flushing', 'osteoarthritis', 'marginal zone lymphoma', 'chronic bronchitis', 'posthypoxic necrotizing leukoencephalopathy', 'gastroesophageal reflux disease', 'dyspepsia', 'chronic lymphocytic leukemia']
# ['insulin-dependent diabetes mellitus', 'DM', 'chronic bronchitis', 'mitral insufficiency', 'pericardial effusion', 'Pancreatitis', 'immunodeficiency virus-1 (HIV-1)', 'hypotension', 'skin rash', 'Gut Dysbiosis, Neuroinflammation']
# moderna   gamma
# ['anhedonia', 'demyelination and gliosis', 'flushing', 'osteoarthritis', 'marginal zone lymphoma', 'chronic bronchitis', 'posthypoxic necrotizing leukoencephalopathy', 'gastroesophageal reflux disease', 'dyspepsia', 'chronic lymphocytic leukemia']
# ['immunodeficiency', 'infection', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# covaxin   omicron
# ['ankle swelling', 'neurological damage', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# ['lower lobe cystic', 'nasal obstruction', 'brachial plexopathy', 'epileptic seizures', 'atopic diseases', 'parasitic diseases', 'psychotic', 'traumatic intracranial hemorrhage', 'anosmia without rhinitis', 'MIS-C']
# covaxin   delta
# ['ankle swelling', 'neurological damage', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# ['lower lobe cystic', 'ALAD', 'Pulmonary Tuberculosis', 'brachial plexopathy', 'epileptic seizures', 'ALD', 'hemoptysis', 'traumatic intracranial hemorrhage', 'opportunistic infections', 'mitral insufficiency']
# covaxin   alpha
# ['ankle swelling', 'neurological damage', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# ['brachial plexopathy', 'epileptic seizures', 'Acute Stress', 'traumatic intracranial hemorrhage', 'mitral insufficiency', 'acute necrotizing encephalitis', 'zoonotic disease', 'psychotic', 'pericardial effusion', 'necrosis']
# covaxin   beta
# ['ankle swelling', 'neurological damage', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# ['insulin-dependent diabetes mellitus', 'DM', 'chronic bronchitis', 'mitral insufficiency', 'pericardial effusion', 'Pancreatitis', 'immunodeficiency virus-1 (HIV-1)', 'hypotension', 'skin rash', 'Gut Dysbiosis, Neuroinflammation']
# covaxin   gamma
# ['ankle swelling', 'neurological damage', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']
# ['immunodeficiency', 'infection', 'coronavirus disease 2019', 'Serosal Hematoma Acting', 'pain', 'hypotension', 'Bilateral Carpal Tunnel Syndrome', 'chronic obstructive pulmonary disease', 'neurocognitive impairment', 'pneumonia']

