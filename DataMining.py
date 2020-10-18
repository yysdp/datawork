import pandas as pd

#候选项地址
#data_path = "data2.csv"
data_path = "data.csv"

#读取.csv文件获取数据，转换数据格式
datas = pd.read_csv(data_path).values.tolist()

#叶子结点最长长度 候选项长度
leafL, length = 3, len(datas[0])
#给定交易t
t = [1,2,3,5,6]
#t = [1,2,3,5,6,7]
t.sort()

#节点类
class Node(object):
    def __init__(self):
        self.elem = []  # 储存叶子结点或哈希函数参数y
        self.next = []  # 指向下一结点，初始为空list
        self.support_count = []  #支持度list
        self.type = 1   #节点类型， 0为存储候选项的节点，1位连接节点，默认为0

#哈希函数，x为输入数据，y为整除参数,初始y为3
y = 3
def hash(x,y):
    return (x-1)%y

#建立哈希树,data为候选项集，root为当前结点，index为当前对比的候选项集的位数
def hashTree(datas,root,index,y):
    if(datas==[]):
        return
    #比较完成，建立叶子节点
    if(len(datas)<=leafL):
        root.elem, root.type=datas, 0
        for i in range(len(datas)):
            root.support_count.append(0)
        return
    elif(index>=length): #现有的哈希函数无法继续区分时，调整哈希函数参数
        hashTree(datas, root, index-1, y+1)
        return
    for i in range(y):
        ds = []
        node = Node()
        root.elem = y
        for data in datas:
            if (hash(data[index],y)==i):
                ds.append(data)
        if (ds!= []):
            root.next.append(node)
            hashTree(ds, node, index + 1, y)
        else:
            root.next.append(None)
#从线索0开始 建立根节点
index, root = 0, Node()

#创建候选项集的哈希树,
hashTree(datas,root,index,y)

#深度优先输出哈希树
def outTree(root,i=0):
    #根据type判断结点类型输出不同结果
    if(root.type==0):
        print(i + 1, "层", root.elem, "对应支持度为", root.support_count)
    else:
        print(i + 1, "层，参数y为",root.elem)
    for nx in root.next:
        if(nx!=None):
            outTree(nx,i+1)

outTree(root)
print()

#result用来储存交易t的所有子集
result = []
#组合，给定交易t, 得到所以大小为target_num的子集
#target每组要输出的元素个数，step游标
def combine(data, step, select_data, target_num):
    # 如果已经凑齐一组完成的组合，输出当前组
    if(len(select_data) == target_num):
        result .append(tuple(select_data))
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
combine(t, 0, [], length)

#j将元组转化为list
ls = []
for re in result :
    ls.append(list(re))
for i in range(0,len(ls),7):#每七个一行输出
    print(ls[i:i+7])
print()

#匹配候选项集,ts为一个组合，root为哈希树根节点，index为索引
def pipei(ts,root,index):
    #结点为空时，结束
    if(root==None):
        return
    #当到达叶子结点时
    if(root.type==0):
        # 遍历叶子结点对应的候选项，匹配与其对应的候选项时，匹配成功时该候选项对应的支持度+1
        for i, el in enumerate(root.elem):
            if (el == ts):
                root.support_count[i]+=1
                print("匹配成功",ts)
        return
    #当到达内部结点时，根据哈希函数到达它的子结点,
    else:
        for i, nx in enumerate(root.next):
            if(hash(ts[index],root.elem)==i):
                pipei(ts, nx, index + 1)
                break

#将每一个组合匹配候选项
for ts in ls:
    index = 0
    pipei(ts,root,index)

#输出哈希树查看支持度变化
print()
outTree(root)