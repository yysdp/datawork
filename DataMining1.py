import  pandas as pd
import  numpy as np
#读取.csv文件获取数据，转换数据格式
data_path = "data.csv"
datas = pd.read_csv(data_path).values.tolist()

#节点类
class Node(object):
    def __init__(self):
        self.elem = []  #初始设置为空
        self.next = []  # 初始设置下一节点为空
        self.support_count = 0  #初始化支持度为0
        self.type = 1   #节点类型， 0位存储候选项的节点，1位连接节点，默认为0
#分类方法a
a = [[1,4,7],[2,5,8],[3,6,9]]

#建立哈希树,q为叶子节点最大项数
q = 3
def hashTree(datas,root,index):
    #比较完成，建立叶子节点
    if(index>2 or len(datas)<=q):
        root.elem.append(datas[0])
        root.type = 0
        for ds in datas[1:]:
            nd = Node()
            nd.elem.append(ds)
            nd.type = 0
            root.next.append(nd)
            root = nd
        return
    #遍历分类方法a
    for ai in a:
        ds = []
        #新建节点并链接父节点
        node = Node()
        #遍历数据
        for data in datas:
            #当data的第index项在ai时分类
            if (data[index] in ai):
                ds.append(data)
        #root.elem.append(ai)
        root.next.append(node)
        hashTree(ds,node,index+1)
#从线索0开始
index = 0
#建立根节点
root = Node()
hashTree(datas,root,index)

#深度优先输出哈希树
jishu = []
def outTree(root,i=0):
    print(i+1,"层",root.type,root.elem,root.support_count)
    if(root.elem!=[]):
        jishu.append(root.elem)
    for nx in root.next:
        if(nx!=None):
            outTree(nx,i+1)

outTree(root)
print()


t = [1,2,3,5,6]
all = []

#target每组要输出的元素个数，step游标
def combine(data, step, select_data, target_num):
    # 如果已经凑齐一组完成的组合，输出当前组
    if(len(select_data) == target_num):
        all.append(tuple(select_data))
        return select_data
    # 如果游标超过数组长，说明后续元素都被遍历完成，跳转到上一个元素的循环
    if(step >= len(data)):
        return
    # 把选中的元素加入临时输出列表中，n个一组作为输出
    select_data.append(data[step])
    # 递归调整最后一位
    combine(data, step + 1, select_data, target_num )
    # 构建一个新组合，首先要删掉上次输出组中药排除的元素
    select_data.pop()
    # 递归向上调整一位元素
    combine(data, step + 1, select_data, target_num )

combine(t, 0, [], q)
ls = []
for al in all:
    ls.append(list(al))
print(ls,len(ls),"\n")

def panduan(ts,root,index):
    if(root==None):
        return
    if(root.type==0):
        while(root.elem!=[]):
            if (ts == root.elem[0]):
                root.support_count += 1
                break
            elif(root.next!=[]):
                root=root.next[0]
            else:
                return
    else:
        for i in range(len(root.next)):
            if (ts[index] in a[i]):
                print(ts[index],a[i],index,)
                panduan(ts, root.next[i], index + 1)
                break
for ts in ls:
    index = 0
    panduan(ts,root,index)
print()
outTree(root)