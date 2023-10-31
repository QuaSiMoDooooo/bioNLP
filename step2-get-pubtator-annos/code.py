# 确定工作目录
import os
os.getcwd()
os.chdir("/home/wtian/bioNLP/step2-get-pubtator-annos")

# 载入上一步得到的数据
import pickle
with open("../step1-papers_target/data.pkl",'rb') as f:
    data = pickle.load(f)
# data.keys()
# len(data['paper_target'])
paper_target = data['paper_target']  # 1075篇目标文章
tokens_target = data['tokens_target']

paper_target

# 提取这1075篇目标文章对应的Disease注释信息
import pandas as pd
paper_id = paper_target[0]
paper_annos = pd.read_csv(os.path.join("../pubtator/annos",paper_id),header=None,sep="\t")
paper_annos
type(paper_annos)
# 并根据MESH去重
# 提取第一列对应第二列为"Disease"的元素
filtered_paper_annos = paper_annos[paper_annos[4] == 'Disease']
filtered_paper_annos
# 对应第三列进行去重
MESH_uniq_tokens = list(set(filtered_paper_annos[5]))
MESH_uniq_tokens
# 先根据MESH作为实体进行互信息的计算，后面搞一张参照表进行MESH和疾病的转换
# ![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231021152436.png)

# 空字典储存
paper_target_uniq_MESH = {}
# 后续提取MESH实体 赋值
def get_unique_annos(paper_id):
    global paper_target_uniq_MESH
    try:
        paper_annos = pd.read_csv(os.path.join("../pubtator/annos",paper_id),header=None,sep="\t")
        filtered_paper_annos = paper_annos[paper_annos[4] == 'Disease']
        MESH_uniq_tokens = list(set(filtered_paper_annos[5]))
        paper_target_uniq_MESH[paper_id] = MESH_uniq_tokens
    except Exception:  # 跳过第一行再试试（第一行可能是没处理掉的title信息 如问号结尾）
        try:
            paper_annos = pd.read_csv(os.path.join("../pubtator/annos",paper_id),header=None,sep="\t",skiprows=[0])
            filtered_paper_annos = paper_annos[paper_annos[4] == 'Disease']
            MESH_uniq_tokens = list(set(filtered_paper_annos[5]))
            paper_target_uniq_MESH[paper_id] = MESH_uniq_tokens
        except Exception:  # 任意报错
            print(paper_id,":无法读取")


for id in paper_target:
    get_unique_annos(id)

len(paper_target_uniq_MESH.keys()) # 1072
# 37287866.txt :无法读取
# 36958743.txt :无法读取
# 32492212.txt :无法读取
# 只有3篇有问题 还好

paper_target_uniq_MESH

# 保存结果
os.getcwd()
import pickle
data = {"paper_target_uniq_MESH":paper_target_uniq_MESH}
# data.keys()
with open("data.pkl",'wb') as f:
    pickle.dump(data, f)

