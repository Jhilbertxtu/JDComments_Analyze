import pandas as pd
from sklearn.decomposition import PCA
from sklearn import svm
'''
10条数据,但模型是100维的,所以复制够100,只取前10
第1次 c=2 完全正确4,完全错误2,模糊4
[1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1.
 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0. 0. 0.
 1. 1. 1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0.
 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0. 0. 0. 1. 1. 1. 0. 0. 1. 1. 0.
 0. 0. 1. 1.]
 第2次 c=1 完全正确5,完全错误1,模糊4
 [0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1.
 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0.
 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0.
 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0. 0. 0. 1. 1. 0.
 0. 0. 1. 1.]
 '''
# 读取测试数据
test=pd.read_csv('datas/test.csv')
tx = test.iloc[:,:]
# 建立测试PCA,维度需要根据模型优化情况及测试数据量调整
pcax=PCA(n_components=100)
pcax.fit(tx)
low_x=pcax.transform(tx)


# 获取模型数据
df = pd.read_csv('datas/phone_pos_neg.csv')
# y为结果,x为向量值
y = df.iloc[:,1]
x = df.iloc[:,2:]

#原始数据400维,降维到100
pca = PCA(n_components = 100).fit_transform(x)
#调整c值,以期最优
clf = svm.SVC(C = 1, probability = True)
#训练
clf.fit(pca,y)
#预测结果
result = clf.predict(low_x)
print(result)
