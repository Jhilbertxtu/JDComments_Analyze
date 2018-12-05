'''
处理语料数据
数据来源:京东手机分类>按评论排序后的第一页所有产品(60个)->产品评论5星和1星的评论内容(见single_spiders/JDcomments)
去标点及英文后逐行读取文件数据进行jieba分词
去除空行,重复,停用词
然后导到mysql再去重一次,得到dis_neg_cut.txt,dis_pos_cut.txt

坑:
差评一般是真的差,好评不一定是好!!!
'''
import jieba
import jieba.analyse
import codecs,re
def pdata(inFile,outFile,st,good):
    '''
    处理评论数据,good是特别为隐藏在好评中的差评准备的
    :param inFile:
    :param outFile:
    :param st:
    :param good:
    :return:
    '''
    f=codecs.open(inFile,'r',encoding='utf8')
    target=codecs.open(outFile,'w',encoding='utf8')
    i=1
    line=f.readline()
    while line:
        line=fix(line,good)
        if line:
            line=cut(line,st)
            if line:
                target.writelines (line + '\n')
        i=i + 1
        line=f.readline()
def cut(line,st):
    '''
    去除空行,重复,停用词
    :param line:
    :param st:
    :return:
    '''
    segList=jieba.cut (line, cut_all=False)
    segSentence=[]
    for word in segList:
        if word != '\t' and word !='\n' and word not in st and word not in segSentence:
            segSentence.append(word)
    if len(segSentence)>0:
        return ' '.join(segSentence)

def fix(l,good):
    '''
    去英文,数字,符号及好评中的差评
    :param l:
    :param good:
    :return:
    '''
    line=l.strip ()
    if good==1:
    # 去掉好评数据的差评!!!
        del_line=['不好看','坑','骗','垃圾','死机','太差','磨损','不舒服','卡的要死','反应慢','后悔','闪屏','黑屏','信号差','缺点','差评',
                  '不好用','不爽','噪音','卡死','失望','可怜','二手','生气','不满意','烦人','山寨','退货','差劲','无法','不太方便','不适合','上当','妈的','赔偿']
        for s in del_line:
            if s in line:
                return None
    # 去除文本中的英文和数字
    line=re.sub ("[a-zA-Z0-9]", "", line)
    # 去除文本中的中文符号和英文符号
    line=re.sub ("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）～ ;℃:￣▽)]+", "", line)
    return line
def main():
    jieba.load_userdict('datas/phone_dict.txt')
    stopkey=[w.strip () for w in codecs.open ('datas/stopwords1598.txt', 'r', encoding='utf-8').readlines ()]
    # n_in为负面语料,p_in为正面语料
    # n_in='datas/phone_comments_neg.txt'
    # p_in='datas/phone_comments_pos.txt'
    # n_out='datas/phone_comments_neg_cut.txt'
    # p_out='datas/phone_comments_pos_cut.txt'
    # pdata (n_in, n_out,stopkey,0)
    # pdata (p_in, p_out,stopkey,1)
    test='datas/test.txt'
    test_out='datas/test_cut.txt'
    pdata(test,test_out,stopkey,0)
if __name__=='__main__':
    main()