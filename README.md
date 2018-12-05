# JDComments_Analyze
    基于京东手机产品评论所做的用户评论极性分析,含36000条评论(部分评论是一条,但折行了,懒得处理了)
    SVM预测正确率86%左右,主要受语料质量影响.       
坑:负面评论一般是真负面,正面评论不一定(评分5星,评论骂娘)

程序   
cut.py:为处理语料数据    
word2vec.py:根据wiki语料生成评论训练集   
svm.py:svm训练并测试新评论    
JDcomments_Spider.py:爬虫

数据datas:   
phone_comments_neg.txt:原始负面评论   
phone_comments_neg_cut.txt:负面评论分词   
phone_comments_pos.txt:原始正面评论   
phone_comments_pos_cut.txt:正面评论分词   
dis_neg_cut.txt:去重后的负面分词    
dis_pos_cut.txt:去重后的正面分词    
phone_dict.txt:JIEBA分词自定义字典   
phone_pos_neg.csv:训练集   
stopwords1598.txt:停用词   
test.csv:测试数据向量   
test.txt:原始测试数据   
test_cut.txt:测试数据分词   
