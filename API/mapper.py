# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:57:46 2022

@author: Patrick
"""

import re
import operator
import math
from collections import Counter
from zss import simple_distance, Node #Zhang-Shasha Algorithm for Tree Edit Distance Calculation

#Python Class for an attribute in a YANG Data Model. Each node of YANG Data Model is assigned in yangdm python class.
class yangdm:
    def __init__ (self, tag, id, isLeaf, level, skip):
        self.tag = tag         # The TAG of the node in the YANG Data Model
        self.id = id           # The ID of the node in the YANG Data Model --> The ID should be assigned sequentially from top to bottom of the YANG DM
        self.isLeaf = isLeaf   # True if the node is a Leaf, False if it is not a Leaf
        self.level = level     # Level of the node YANG DM (Level 0 = Root, Level 1 = child of root)
        self.skip = skip       # True if it is skippable, e.g., Match-Case in YANG Data Model
        self.parent = None     # Parent of the node
        self.child = []        # Child of the node. If the node is a leaf, it is empty, i.e., []
        
    def setParent(self,parent): # For setting the parent of the node
        self.parent = parent
    
    def printParent(self):   # Printing the parent
        if self.parent is not None:
            print("Parent : {}".format(self.parent.tag))
        
    def printDM(self):       # Printing the node details
        print("Tag    : {}".format(self.tag))
        print("ID     : {}".format(self.id))
        print("isLeaf : {}".format(self.isLeaf))
        print("Level  : {}".format(self.level))
        print("Skip   : {}".format(self.skip))
        yangdm.printParent(self)
        print("Child  : {}".format(self.child))
    
    def setChild(self,child): # Setting the child of the node
        self.child.append(child)
    
    def setLeafID(self,leafID):
        self.leafID = leafID
        
    def path(self): #Get the path of the attribute
        if self.parent is None:
            return "/{}".format(self.tag)
        else:
            return "{}/{}".format(self.parent.path(),self.tag)




#Parsing from YANG Tree Data Model into Python Class yangdm. Reading each line of the YANG Tree Data Model
# YANG DataModel 파일의 각 line별 parsing
def parsing(line,id):
    linelen = len(line)
    skip = False
    
    # YANG 데이터모델 parsing
    # 현재칸이 빈칸'' 혹은 |로 되어있을 때, +가 나올때까지 오른쪽으로 이동
    # 예시:
    #start(index): 2, level: 0
    #  +--rw i2nsf-cfi-policy* [name]
    #start(index): 5, level: 1
    #  |  +--rw name                   string
    #start(index): 17, level: 5
    #  |     |  |     +--rw flow-rate-threshold?     uint64
    start = 0
    while line[start] == ' ' or line[start] == '|':
        start += 1

    # YANG데이터모델은 level(depth)이 1단계 증가할 때마다 3칸씩 안쪽으로 들여쓰기 된다.
    level = int((start-2)/3)
    
    # start(index)위치에서 3칸 옆이 r이 나옴. (+--rw)
    if line[start+3] == 'r':
        start += 6 # +로부터 데이터 시작부분은 6칸 옆에 나옴 (+--rw 데이터)
    else:
        start += 4 # 그 외의 데이터는 4칸 옆에 나옴 (+--:데이터)
    end = start
    

    if line[start] == '(':
        for i in range(start, linelen):
            if line[i] == ')':
                end = i
                break
        tag = line[start:end+1]
        start = end
        skip = True
    else:
        for i in range(start, linelen):
            if line[i] =='*' or line[i] =='?' or line[i] ==' 'or line[i] == '\n':
                end = i
                break
        tag = line[start:end]
        if line[end] == '*' or line[end] == '?':
            start = end + 1
        else:
            start = end
            
    isLeaf=True
    end = start


    while line[end] ==' ':
        end += 1
    
    if line[end] == '[' or line[end]=='\n':
        isLeaf = False

    
    data = yangdm(tag=tag,id=id,level=level,isLeaf=isLeaf, skip=skip)
    #print(data)
    #print(data.printDM())

    return data





def text_to_vector(text):
    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(vector1, vector2):
    vec1 = text_to_vector(vector1)
    vec2 = text_to_vector(vector2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 1 * int(max(len(vector1),len(vector2)))
    else:
        return int(len(vector1) * (1- float(numerator) / denominator))
    
def weird_dist(A, B):
    """
       Available to use for calculating Distance:
       1. strdist(A,B)
       2. seqMatch(A,B)
       3. get_cosine(A,B)
    """
    return get_cosine(A, B) 

class WeirdNode(object):

    def __init__(self, label):
        self.my_label = label
        self.my_children = list()

    @staticmethod
    def get_children(node):
        return node.my_children

    @staticmethod
    def get_label(node):
        return node.my_label

    def addkid(self, node, before=False):
        if before:  self.my_children.insert(0, node)
        else:   self.my_children.append(node)
        return self
    
    
def mapAttributes(cfiTree,nfiTree):

    # READ CFI / High-Level YANG Data Model tree and parse it into python yang dm class
    with open(cfiTree,'r') as f:
        next(f) # 다음줄로 넘어감 (1번째 줄 버림)
        id = 0
        cfiFull = [] #Full data model

        # parsing(line,id)하면 이렇게 나타난다 = <mapper.yangdm object at 0x7f8d50323310>
        # 그리고 parsing(line,id).printDM()을 하면, 내부 내용이 나온다.
        # <mapper.yangdm object at 0x7f8d50323310>
        # Tag    : group-name
        # ID     : 189
        # isLeaf : True
        # Level  : 3
        # Skip   : False
        # Child  : []

        # txt파일에서 한줄씩 가져오기
        for line in f:
            cfiFull.append(parsing(line,id)) # cfiFull = [<mapper.yangdm object at 0x7f8d50323310>, <mapper.yangdm object at 0x7f8d50323370>, ...]
            id += 1            

    
    
    ##### cfiFull에 들어있는 모든 yang data model 데이터들의 부모값을 입력
    # range(len(cfiFull)-1, -1, -1)
    # 마지막 인덱스부터 0 인덱스까지 1씩 감소함
    # cfiFull: [<mapper.yangdm object at 0x7f44fbfbb850>, <mapper.yangdm object at 0x7f44fbfbbfd0>, <mapper.yangdm object at 0x7f44fbfbb880>,....]
    
    # 예시:
    '''
    |     |  +--rw context
    |     |  |  +--rw time
    |     |  |  |  +--rw start-date-time?   yang:date-and-time
    '''
    # start-date-time의 부모는 time이고, time의 부모는 context이다.   

    for i in range(len(cfiFull)-1,-1,-1): # i = 10, 9, 8, .... , 0

        # cfi_minus.txt파일을 가장 아래줄부터 위로 훝는다.
        # 기준행인 i행을 잡고, 그보다 위쪽에 있는 행등을 살피면서, 한칸 안쪽으로 들어간 행이 바로 부모로 설정한다.
        # 즉, 기준 i행과 level을 비교해서 낮은 레벨의 행이 나오면 바로 부모로 설정한다.
        print("YangDataModel line:")
        print(cfiFull[i].printDM())

        for j in range(i-1,-1,-1):
            # 부모를 찾기 위해 선택된 i행부터 위로 올라가면서, 자신과 같은 레벨은 지나치고,
            # 한 칸 안쪽으로 들어간 행이 나오면 바로 그걸 부모 행으로 삼는다.
            if cfiFull[i].level > cfiFull[j].level:
                cfiFull[i].setParent(cfiFull[j])
                break
        
        print("line parent:")
        if i != 0:
            print(cfiFull[i].parent.tag) # 부모행 tag
        else: 
            print(cfiFull[i].parent)
        print("--------------")



    ##### 건너뛸 부분(skip) 판단하기
    # 위에서 각 행별로 parsing(line,id)를 해서, skip = false로 되어있음
    # +--:(괄호내용) 이렇게 되어 있는 부분은 건너뛴다. (skip 부분)
    # cfi_minus.txt에는 skip부분이 없고, nfi.txt에는 skip 부분이 존재함

    # 즉, 부모 판단시, level이 낮아도 (괄호)처럼 된 부분이 있으면
    # 그 부분은 건너뛰고 그보다 더 낮은 레벨을 부모로 삼는다.

    # 예시:
    '''
     |  |  |  |  +--rw ipv4
     |  |  |  |     +--rw dscp?                             inet:dscp
     |  |  |  |     +--rw identification?                   uint16
     |  |  |  |     +--rw (destination-network)?
     |  |  |  |     |  +--:(destination-ipv4-network)
     |  |  |  |     |  |  +--rw destination-ipv4-network?   inet:ipv4-prefix
     |  |  |  |     +--rw (source-network)?
     |  |  |  |        +--:(source-ipv4-network)
     |  |  |  |        |  +--rw source-ipv4-network?        inet:ipv4-prefix
    '''
    # 여기서 source-ipv4-network의 바로 위쪽은 (괄호)로 되어있으므로,
    # 그 부분은 skip을 해서, 부모는 ipv4 가 된다.
    for i in range(len(cfiFull)-1,-1,-1):
        try:
            while cfiFull[i].parent.skip:
                cfiFull[i].setParent(cfiFull[i].parent.parent)
        except:
            pass
    

    ##### 부모 아래의 직속 자식들을 확인한다.
    # 예시: 
    '''
    parent: context (id=36, path=/i2nsf-cfi-policy/rules/condition/context)
      children: [('time', 37, '/i2nsf-cfi-policy/rules/condition/context/time'), ('application', 47, '/i2nsf-cfi-policy/rules/condition/context/application'), ('device-type', 49, '/i2nsf-cfi-policy/rules/condition/context/device-type'), ('users', 51, '/i2nsf-cfi-policy/rules/condition/context/users'), ('geographic-location', 58, '/i2nsf-cfi-policy/rules/condition/context/geographic-location')]
    '''

    for i in range(len(cfiFull)):
        for j in range(len(cfiFull)):
            try:
                if cfiFull[i].id == cfiFull[j].parent.id and not cfiFull[j].skip:
                    cfiFull[i].setChild(cfiFull[j])
            except:
                pass
                    

        # i행 부모의 직속 자식만 즉시 확인
        if cfiFull[i].child:
            print(f"parent: {cfiFull[i].tag} (id={cfiFull[i].id}, path={cfiFull[i].path()})")
            kids = [(ch.tag, ch.id, ch.path()) for ch in cfiFull[i].child]
            print("  children:", kids)
            print()

    
    # YANG에서 leaf는 자식이 없고 값을 한 개만 가지는 노드    
    # ?가 있으면 해당 값이 있을수도 있고, 없을수도 있다.
    # leaf 예시: +--rw identification? uint16
    # leaf 예시: +--rw name string

    # CFI 트리에서 리프(leaf) 노드와 비-리프(non-leaf) 노드를 분리해서 따로 보관하고,
    # 리프(leaf)들엔 연속 번호(leafID) 를 붙이는 단계
    cfiLeaf = [] #For only the leaf data model
    leafID=0
    for x in cfiFull:
        if x.isLeaf and not x.skip:
            x.setLeafID(leafID)
            cfiLeaf.append(x)
            leafID+=1
            
    cfiNonLeaf = []
    for x in cfiFull:
        if not x.isLeaf and not x.skip:
            cfiNonLeaf.append(x)
            
    #########################################################################



    # READ NFI / High-Level YANG Data Model tree and parse it into python yang dm class
    with open(nfiTree,'r') as f:
        next(f)
        id = 0
        nfiFull = [] #Full data model
        for line in f:
            nfiFull.append(parsing(line,id))
            id += 1
            
    for i in range(len(nfiFull)-1,-1,-1):
        for j in range(i-1,-1,-1):
            if nfiFull[i].level > nfiFull[j].level:
                nfiFull[i].setParent(nfiFull[j])
                break
    
    for i in range(len(nfiFull)-1,-1,-1):
        try:
            while nfiFull[i].parent.skip:
                nfiFull[i].setParent(nfiFull[i].parent.parent)
        except:
            pass
    
    for i in range(len(nfiFull)):
        for j in range(len(nfiFull)):
            try:
                if nfiFull[i].id == nfiFull[j].parent.id and not nfiFull[j].skip:
                    nfiFull[i].setChild(nfiFull[j])
            except:
                pass
                    



    nfiLeaf = [] #For only the leaf data model
    nfiLeafID = 0
    for x in nfiFull:
        if x.isLeaf and not x.skip:
            x.setLeafID(nfiLeafID)
            nfiLeaf.append(x)
            nfiLeafID+=1
            
    nfiNonLeaf = []
    for x in nfiFull:
        if not x.isLeaf and not x.skip:
            nfiNonLeaf.append(x)



    #Separating the YANG Tree into 1 branch
    #Edge Contraction also used here --> If the parent and the leaf has similar label, the edge is deleted, then the parent and the child is unified
    def ctree (leafNode): #leafNode is a yangdm Python Class
        Nodes = list()
        Nodes.append(leafNode)
        parentNode = leafNode.parent
        while parentNode is not None:
            try:
                Nodes.append(parentNode)
            except AttributeError:
                pass
            leafNode = leafNode.parent
            parentNode = parentNode.parent
        return Nodes
    
    cfiM = list()
    nfiM = list()
    cfiNL = list()
    nfiNL = list()
    for i in range(len(cfiLeaf)):
        cfiM.append(ctree(cfiLeaf[i]))
        
    for j in range(len(nfiLeaf)):
        nfiM.append(ctree(nfiLeaf[j]))
        
    for i in range(len(cfiNonLeaf)):
        cfiNL.append(ctree(cfiNonLeaf[i]))
        
    for j in range(len(nfiNonLeaf)):
        nfiNL.append(ctree(nfiNonLeaf[j]))
    
    def getChild(parent):
        allChild = []
        for child in parent.child:
            allChild.append(child)
            if child.child:
                leaf = getChild(child)
                for l in leaf:
                    allChild.append(l)
        return allChild
    


    #MAPPING THE NON LEAF
    parentMap = {}
    for w in range(len(cfiNonLeaf)):
        distance = list()
        for x in reversed(cfiNL[w]):
            if x.parent is None:
                A = WeirdNode(x.tag)
            else:
                A.addkid(WeirdNode(x.tag))
        if cfiNonLeaf[w].parent is not None:
            minDistances = {}
            #print(cfiNonLeaf[w].tag)
            for x in parentMap[cfiNonLeaf[w].parent]:
                #print(cfiNonLeaf[i].tag, cfiNonLeaf[i].parent.tag, x.tag)
                nfiPair = getChild(x)
                nfiPair.insert(0,nfiPair[0].parent)
                distance=[]
    
                for j in range(len(nfiPair)):
                    F=''
                    for y in reversed(ctree(nfiPair[j])):
                        F+=y.tag+'/'
                        if y.parent is None:
                            B = WeirdNode(y.tag)
                        else:
                            B.addkid(WeirdNode(y.tag))
                    if nfiPair[j].isLeaf:
                        distance.append(10000)
                    else:
                        distance.append(int(simple_distance(A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)))
                index = [i for i, x in enumerate(distance) if x == min(distance)]
                for i in index:
                    minDistances[nfiPair[i]] = min(distance)
            min_val = min(minDistances.values())
            index = [k for k, x in minDistances.items() if x == min_val]
            parentMap[cfiNonLeaf[w]] = [k for k in index]
        else:
            for j in range(len(nfiNonLeaf)):
                for y in reversed(nfiNL[j]):
                    if y.parent is None:
                        B = WeirdNode(y.tag)
                    else:
                        B.addkid(WeirdNode(y.tag))
                distance.append(int(simple_distance(A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)))
    
            index, value = min(enumerate(distance), key=operator.itemgetter(1))
            index = [i for i, x in enumerate(distance) if x == min(distance)]
            parentMap[cfiNonLeaf[w]]= [nfiNonLeaf[k] for k in index]
    
    finalMap = {}
    res = {}
    for w in range(len(cfiLeaf)):
        minDistances = {}
        current = cfiLeaf[w]
    
        cfiM = ctree(current)
        nfiparents = parentMap[current.parent]
        for x in reversed(cfiM):
            if x.parent is None:
                A = WeirdNode(x.tag)
            else:
                A.addkid(WeirdNode(x.tag))
        for nfiparent in (nfiparents):
            distance=[]
            nfiPair = getChild(nfiparent)
    
    
            for j in range(len(nfiPair)):
                nfiM = ctree(nfiPair[j])
                for x in reversed(nfiM):
                    if x.parent is None:
                        B = WeirdNode(x.tag)
                    else:
                        B.addkid(WeirdNode(x.tag))
    
                distance.append(int(simple_distance(A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)))
    
            index = [i for i, x in enumerate(distance) if x == min(distance)]
            for i in index:
                minDistances[nfiPair[i]] = min(distance)
    
        min_val = min(minDistances.values())
        index = [k for k, x in minDistances.items() if x == min_val]
        finalMap[current] = [i for i in index]
        for i in index:
            if current in res:
                res[current].append(i)
            else:
                res[current] = [i]
    return res