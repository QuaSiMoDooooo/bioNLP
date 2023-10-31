import os
# 设置工作路径
os.getcwd()
os.chdir("/home/wtian/bioNLP/step5-labels-valid")

import pandas as pd
# 读取各打好的labels对应的pmid
# 5种疫苗
coronavac_papers = pd.read_csv("labels_pmid/coronavac_flt.tsv",sep="\t")
coronavac_pmid = coronavac_papers["pmid"]
pfizer_papers = pd.read_csv("labels_pmid/pfizer_flt.tsv",sep="\t")
pfizer_pmid = pfizer_papers["pmid"]
astrazeneca_papers = pd.read_csv("labels_pmid/astrazeneca_flt.tsv",sep="\t")
astrazeneca_pmid = astrazeneca_papers["pmid"]
moderna_papers = pd.read_csv("labels_pmid/moderna_flt.tsv",sep="\t")
moderna_pmid = moderna_papers["pmid"]
covaxin_papers = pd.read_csv("labels_pmid/covaxin_flt.tsv",sep="\t")
covaxin_pmid = covaxin_papers["pmid"]
# 5种病毒亚型
omicron_papers = pd.read_csv("labels_pmid/omicron_flt.tsv",sep="\t")
omicron_pmid = omicron_papers["pmid"]
delta_papers = pd.read_csv("labels_pmid/delta_flt.tsv",sep="\t")
delta_pmid = delta_papers["pmid"]
alpha_papers = pd.read_csv("labels_pmid/alpha_flt.tsv",sep="\t")
alpha_pmid = alpha_papers["pmid"]
beta_papers = pd.read_csv("labels_pmid/beta_flt.tsv",sep="\t")
beta_pmid = beta_papers["pmid"]
gamma_papers = pd.read_csv("labels_pmid/gamma_flt.tsv",sep="\t")
gamma_pmid = gamma_papers["pmid"]

def find_overlap_pmid(set1,set2):
    overlap_pmid = list(set(set1) & set(set2))
    return overlap_pmid

# targets：
# 1.和前面1075篇文章pmid overlap
# 2.看一下pfizer+omicron下各种疾病 和我们自己提的互信息排名在前的比较

# 1.和前面1075篇疫苗相关文章pmid overlap
# 载入上一步得到的数据
import pickle
with open("../step1-papers_target/data.pkl",'rb') as f:
    data = pickle.load(f)
paper_target = data['paper_target']
paper_target_id = [int(paper.replace(".txt","")) for paper in paper_target]
len(paper_target_id)  # 1075
# '32492212.txt'.replace(".txt","")
# 整合打好lebels的疫苗相关文章的pmid
vaccines_abot_id = list(coronavac_pmid)+list(pfizer_pmid)+list(astrazeneca_pmid)+list(moderna_pmid)+list(covaxin_pmid)
len(vaccines_abot_id)  # 82
print(len(find_overlap_pmid(paper_target_id, vaccines_abot_id)))  # 39

print(find_overlap_pmid(pfizer_pmid,omicron_pmid))
# [37480344, 37334978, 37242988, 37073325]
# 虽然只有四篇但还是作为金标准
# 查看对应疾病

# 载入上一步得到的数据 annos
import pickle
with open("../step2-get-pubtator-annos/data.pkl",'rb') as f:
    data = pickle.load(f)
paper_target_uniq_MESH = data['paper_target_uniq_MESH']
paper_target_uniq_MESH
# 整合
ref_disease = []
for id in [37480344, 37334978, 37242988, 37073325]:
    paper = str(id)+".txt"
    # 对应的MESH
    ref_disease += paper_target_uniq_MESH[paper]
ref_disease
len(ref_disease)  # 14
ref_disease_uniq = list(set(ref_disease))
len(ref_disease_uniq)  # 8
# ['MESH:D005221', 'MESH:D003967', 'MESH:D002637', 'MESH:C000657245', 'MESH:D009765', 'MESH:D012818', 'MESH:D007239', 'MESH:D006261']

# 提取MESH对应的disease
# 读取参考
ref = pd.read_csv("../pubtator/ref_mesh_disease.tsv",header=None,sep="\t")
ref.head()
#                                    0                1
# 0                 pulmonary fibrosis     MESH:D011658
# 1           coronavirus disease 2019  MESH:C000657245
# 2           Coronavirus disease 2019  MESH:C000657245
# 3                           COVID-19  MESH:C000657245
# 4  severe acute respiratory syndrome     MESH:D045169



disease_list = [list(ref.loc[ref.iloc[:,1] == mesh, ref.columns[0]])[0] for mesh in ref_disease_uniq]
disease_list
# ['fatigue', 'diarrhea', 'chest tightness', 'coronavirus disease 2019', 'obesity', 'respiratory symptoms', 'infection', 'headache']

# 自己算的：
# # ['hematological malignancies', 'dysgeusia', 'inability', 'cancer', 'pulmonary symptoms', 'olfactory loss', 'respiratory failure', 'myalgia', 'cough', 'depression']


