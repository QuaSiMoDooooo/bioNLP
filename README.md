This is a repository used to host the code and data related to the biological text mining and knowledge discovery(HZAU) course Thesis.

---

根据老师要求丰富README文档，README文档将以课程论文为主线，带着介绍仓库中每部分代码用途

# intro

虽然目前新型冠状病毒的传播已经不再构成国际关注的突发公共卫生事件，并且我们前后研发了各类疫苗，但是接种这些不同疫苗后感染不同亚型病毒的感染是否会导致后遗症，目前还鲜为人知，我们迫切需要从海量的医学文献中挖掘出有价值的知识

基于此，我们小组（吴天、闵聪聪、郑柳）将研究兴趣和课上讲授的文本挖掘和知识发现的技法进行结合，最后决定探究的方向为不同疫苗，不同毒株及后遗症三者的关系。

# 材料与方法

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120103911.png)

# 结果与讨论

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120103942.png)

在仓库中 `pubmed/abstract`文件夹下保存了我们根据pmid获取摘要内容的脚本

在 `step1-papers_target` 文件夹下我们展示了如何初步筛选和清洗目标文献

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104505.png)

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104525.png)

在 `step2-get-entities` 和 `step2-get-pubtator-annos` 我们展示了如何通过自定义的词列表以及Pubtator获取相关的实体注释信息

在 `step5-labels-valid` 中我们通过LitCovid已经打好的标签进行了比较

---

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104413.png)

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104436.png)

在 `step3-HPO-enrichment` 中保存了进行HPO富集分析的脚本

---

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104633.png)

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104641.png)

![](https://photo-bed-wt.oss-cn-hangzhou.aliyuncs.com/images/20231120104700.png)

在 `step4-mutual-info` 中我们进行了互信息的计算

---

筚路蓝缕以启山林
