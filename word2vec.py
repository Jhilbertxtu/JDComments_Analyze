import warnings
# 忽略警告
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import codecs
import numpy as np
import pandas as pd
import gensim

def getWordVecs(wordList,model):
    '''
    根据wiki语料的向量模型获取单个词的向量
    :param wordList:
    :param model:
    :return:
    '''
    vecs = []
    for word in wordList:
        word = word.replace('\n','')
        try:
            # 每个词的向量值有400个维度
            # vecs=[[词1的400维的向量值],[词2的400维的向量值]...]
            vecs.append(model[word])
        except KeyError as e:
            print(e)
            continue
    return np.array(vecs, dtype='float')
def createVecs(f,model):
    fileVecs=[]
    # 根据数据量决定对正向及负向语料各取18000条数据
    vmax=18000
    with codecs.open (f, 'rb', encoding='utf-8') as contents:
        for line in contents:
            wordList=line.split (' ')
            vecs=getWordVecs (wordList, model)
            if len (vecs) > 0:
                # 求一个句子中所有词的向量值的均值
                vecsArray=sum (np.array (vecs)) / len (vecs)
                fileVecs.append (vecsArray)
                if len(fileVecs)==vmax:
                    return fileVecs
    return fileVecs

if __name__=='__main__':
    # 加载wiki语料向量
    inm='/your_path/wiki_zh_text.vector'
    model=gensim.models.KeyedVectors.load_word2vec_format (inm, binary=False)
    # #模型建立
    # in_neg='datas/dis_neg_cut.txt'
    # in_pos='datas/dis_pos_cut.txt'
    # out_csv='datas/phone_pos_neg.csv'
    # negInput=createVecs (in_neg, model)
    # posInput=createVecs (in_pos, model)
    # #根据正向和负向模型的长度,建立结果Y,正向全是1,负向全是0
    # Y=np.concatenate ((np.ones (len (posInput)), np.zeros (len (negInput))))
    # X=posInput[:]
    # 将正负向数据组合
    # for neg in negInput:
    #     X.append (neg)
    # X=np.array (X)
    # # 保存数据
    # df_x=pd.DataFrame (X)
    # df_y=pd.DataFrame (Y)
    # data=pd.concat ([df_y, df_x], axis=1)
    #建立测试数据
    test='datas/test_cut.txt'
    out_csv='datas/test.csv'
    testInput=createVecs(test,model)
    data=pd.DataFrame(testInput)
    data.to_csv (out_csv)