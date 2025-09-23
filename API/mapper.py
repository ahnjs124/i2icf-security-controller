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
    # 예시:
    # text: i2nsf-security-policy
    # words: ['i2nsf', 'security', 'policy']
    # text: i2nsf-cfi-policy
    # words: ['i2nsf', 'cfi', 'policy']

    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    return Counter(words) # 리스트 내용을 counting해서 dictionary화 시킴


def get_cosine(vector1, vector2):
    vec1 = text_to_vector(vector1) # Counter(['i2nsf', 'security', 'policy']) = vec1 = {'i2nsf': 1, 'security': 1, 'policy': 1}
    vec2 = text_to_vector(vector2) # Counter(['i2nsf', 'cfi', 'policy']) = vec2 = {'i2nsf': 1, 'cfi': 1, 'policy': 1}
    intersection = set(vec1.keys()) & set(vec2.keys()) # 공통 부분만 추출 => intersection = {'i2nsf','policy'}
    # 분자
    numerator = sum([vec1[x] * vec2[x] for x in intersection]) # 각 key의 value값 곱하기 (출연횟수의 곱)

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())]) # 각 벡터의 제곱합 vec1 = {'i2nsf':1, 'security':1, 'policy':1} => 1² + 1² + 1² = 3
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())]) # 각 벡터의 제곱합 vec2 = {'i2nsf':1, 'cfi':1, 'policy':1} => 1² + 1² + 1² = 3
    # 분모
    denominator = math.sqrt(sum1) * math.sqrt(sum2)


    # 기존 코사인 유사도: cos(θ) = numerator / denominator => 두 벡터가 얼마나 유사한지 0~1 사이의 값으로 나옴
    # 여기서는 유사도가 아니라 "거리"처럼 변환해서 쓰기 위해서, 1 - (numerator/denominator)를 사용
    # 값이 작을수록 비슷하고, 클수록 다름
    if not denominator:
        # denominator가 0일 때
        return 1 * int(max(len(vector1),len(vector2))) # len(vector1)를 곱해서, 문자열 길이만큼 스케일링된 거리값을 나타냄, 두 문자열이 길수록 차이가 커짐
    else:
        # denominator가 0이 아닌 수(양수, 음수, float 전부)
        return int(len(vector1) * (1- float(numerator) / denominator)) # len(vector1)를 곱해서, 문자열 길이만큼 스케일링된 거리값을 나타냄, 두 문자열이 길수록 차이가 커짐
    

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
        if before:  
            self.my_children.insert(0, node)
        else:
            self.my_children.append(node)
        
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
        print("cfi YangDataModel line:")
        print(cfiFull[i].printDM())

        for j in range(i-1,-1,-1):
            # 부모를 찾기 위해 선택된 i행부터 위로 올라가면서, 자신과 같은 레벨은 지나치고,
            # 한 칸 안쪽으로 들어간 행이 나오면 바로 그걸 부모 행으로 삼는다.
            if cfiFull[i].level > cfiFull[j].level:
                cfiFull[i].setParent(cfiFull[j])
                break
        
        print("cfi line parent:")
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
    # ?가 있으면 해당 값이 있을수도 있고, 없을수도 있다. (설정만 해놓음)
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
    
    print("single cfiLeaf:\n", cfiLeaf)
    print("single cfiNonLeaf:\n", cfiNonLeaf)

    #########################################################################


    # READ NFI / High-Level YANG Data Model tree and parse it into python yang dm class
    ##### CFI와 같이 각 행별로 Yang Data Model 형태 parsing
    with open(nfiTree,'r') as f:
        next(f)
        id = 0
        nfiFull = [] #Full data model
        for line in f:
            nfiFull.append(parsing(line,id))
            id += 1
            

    ##### CFI와 같이 nfiFull에 들어있는 모든 yang data model 데이터들의 부모값을 입력
    for i in range(len(nfiFull)-1,-1,-1):
        print("nfi YangDataModel line:")
        print(nfiFull[i].printDM())

        for j in range(i-1,-1,-1):
            if nfiFull[i].level > nfiFull[j].level:
                nfiFull[i].setParent(nfiFull[j])
                break
        
        print("nfi line parent:")
        if i != 0:
            print(nfiFull[i].parent.tag) # 부모행 tag
        else: 
            print(nfiFull[i].parent)
        print("--------------")


    ##### CFI와 같이 건너뛸 부분(skip) 판단하기
    for i in range(len(nfiFull)-1,-1,-1):
        try:
            while nfiFull[i].parent.skip:
                nfiFull[i].setParent(nfiFull[i].parent.parent)
        except:
            pass


    ##### CFI와 같이 부모 아래의 직속 자식들을 확인
    for i in range(len(nfiFull)):
        for j in range(len(nfiFull)):
            try:
                if nfiFull[i].id == nfiFull[j].parent.id and not nfiFull[j].skip:
                    nfiFull[i].setChild(nfiFull[j])
            except:
                pass
                    
        # i행 부모의 직속 자식만 즉시 확인
        if nfiFull[i].child:
            print(f"parent: {nfiFull[i].tag} (id={nfiFull[i].id}, path={nfiFull[i].path()})")
            kids = [(ch.tag, ch.id, ch.path()) for ch in nfiFull[i].child]
            print("  children:", kids)
            print()


    # NFI 트리에서 리프(leaf) 노드와 비-리프(non-leaf) 노드를 분리해서 따로 보관하고,
    # 리프(leaf)들엔 연속 번호(nfiLeafID) 를 붙이는 단계
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

    print("single nfiLeaf:\n", nfiLeaf)
    print("single nfiNonLeaf:\n", nfiNonLeaf)


##########################################################################

    #Separating the YANG Tree into 1 branch
    #Edge Contraction also used here --> If the parent and the leaf has similar label, the edge is deleted, then the parent and the child is unified
    
    
    # 입력: leafNode (부모·자식 포인터를 가진 yangdm 클래스 인스턴스)
    # 동작: leafNode에서 시작해 parent를 따라 루트까지 위로 올라가며 노드들을 Nodes 리스트에 순서대로 넣음
    # 반환: [현재노드, 부모, 조부모,.., 루트]
    # ctree 함수는 한 개의 노드(특정행)가 최상단 행(루트)까지 가지는 모든 부모의 경로를 반환한다
    def ctree (leafNode): #leafNode is a yangdm Python Class
        Nodes = list()
        Nodes.append(leafNode) # 현재 노드
        parentNode = leafNode.parent # 부모 노드 확인
        while parentNode is not None:
            try:
                Nodes.append(parentNode) # 부모 노드가 존재시 list에 넣기
            except AttributeError:
                pass
            leafNode = leafNode.parent # 기존 부모를 leafNode로 변경
            parentNode = parentNode.parent # 기존 부모의 부모를 parentNode로 변경
        
        # 특정 노드의 부모가 더 이상 없을 때까지 실행
        return Nodes
   

    # 각 노드별로 최상단 행까지의 모든 부모들을 나타내는 리스트를 개별적으로 작성
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

    # 각 노드별로 최상단 행까지의 모든 부모를 나타내므로, 모든 리스트의 마지막 값은 동일하다
    # 예시: cfi LeafNode의 모든 리스트들은 <mapper.yangdm object at 0x7f2f93524f40>로 끝난다.
    # 예시: nfi LeafNode의 모든 리스트들은 <mapper.yangdm object at 0x7f2f93524ac0>로 끝난다.
    # cfiM = cfi LeafNode: [[<mapper.yangdm object at 0x7f2f93524f70>, <mapper.yangdm object at 0x7f2f93524f40>], [<mapper.yangdm object at 0x7f2f93524ee0>, <mapper.yangdm object at 0x7f2f93524f40>],...]
    # nfiM = nfi LeafNode: [[<mapper.yangdm object at 0x7f2f93524fd0>, <mapper.yangdm object at 0x7f2f93524ac0>], [<mapper.yangdm object at 0x7f2f93524760>, <mapper.yangdm object at 0x7f2f93524ac0>],...]
    # cfiNL = cfi NonLeafNode: [[<mapper.yangdm object at 0x7f2f93524f40>], [<mapper.yangdm object at 0x7f2f93524880>, <mapper.yangdm object at 0x7f2f93524f40>], [<mapper.yangdm object at 0x7f2f93524eb0>, <mapper.yangdm object at 0x7f2f93524880>, <mapper.yangdm object at 0x7f2f93524f40>],...]
    # nfiNL = nfi NonLeafNode: [[<mapper.yangdm object at 0x7f2f93524ac0>], [<mapper.yangdm object at 0x7f2f93550100>, <mapper.yangdm object at 0x7f2f93524ac0>], [<mapper.yangdm object at 0x7f2f935501c0>, <mapper.yangdm object at 0x7f2f93550100>, <mapper.yangdm object at 0x7f2f93524ac0>],...]

    print("cfi LeafNode (List):\n", cfiM)
    print("nfi LeafNode (List):\n", nfiM)
    print("cfi NonLeafNode (List):\n", cfiNL)
    print("nfi NonLeafNode (List):\n", nfiNL)


    def getChild(parent):
        allChild = []
        for child in parent.child:
            allChild.append(child)
            if child.child:
                leaf = getChild(child)
                for l in leaf:
                    allChild.append(l)
        return allChild
    

    # 각 노드 집합의 개수는 동일함
    # len(cfiLeaf) == len(cfiM)
    # len(nfiLeaf) == len(nfiM)
    # len(cfiNonLeaf) == len(cfiNL)
    # len(nfiNonLeaf) == len(nfiNL)


    #MAPPING THE NON LEAF
    parentMap = {}
    for w in range(len(cfiNonLeaf)):
        print(w, cfiNonLeaf(w))
        distance = list()

        for x in reversed(cfiNL[w]): # 경로 리스트를 뒤집어서 루트부터 순회
            # 리스트의 맨 처음은 x.parent = None
            # 그 다음부터 x.parent 존재 
            if x.parent is None:
                # 맨 처음에 부모 없는 루트 노드에서 WeirdNode의 인스턴스 생성
                # A = <mapper.WeirdNode object at 0x7fe432870100>
                A = WeirdNode(x.tag)
            else:
                # addkid()로 처음에 만들어진 WeirdNode 인스턴스 안의 my_children 리스트에
                # 추가 생성되는 객체들 저장
                A.addkid(WeirdNode(x.tag)) # 자식을 붙임
            print(A.my_children)


        # cfiNonLeaf: 단일 행의 yangdm 객체
        # cfiNL: 부모 객체까지 포함한 리스트 형태

        # for문의 맨 처음 노드는 부모가 없어서 else로 넘어간다. 그 뒤는 부모가 다 존재한다.
        # 선택된 cfiNonLeaf 노드에 부모가 있는 경우
        if cfiNonLeaf[w].parent is not None:
            minDistances = {}
            print("name:", cfiNonLeaf[w].tag)

            for x in parentMap[cfiNonLeaf[w].parent]:
                print(cfiNonLeaf[i].tag, cfiNonLeaf[i].parent.tag, x.tag)
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

                    # Leaf일 때는 거리값에 10000을 넣어서 최솟값 경쟁에서 제외
                    if nfiPair[j].isLeaf:
                        # 특정 후보가 리프(Leaf)인 경우
                        distance.append(10000)
                    else:
                        # 리프(Leaf)가 아닌 경우
                        # Zhang–Shasha Tree Edit Distance (장샤샤 알고리즘 거리 계산)
                        '''
                        zss.simple_distance(A, B, get_children=zss.Node.get_distance, get_label=zss.Node.get_label, label_dist=strdist)
                        Computes the exact tree edit distance between trees A and B. Provides a simplified interface for use when insert/remove cost is equivalent to updating a node from/to an empty label.

                        Parameters:	
                        A: The root of a tree.
                        B: The root of a tree.
                        get_children: A function get_children(node) == [node children]. Defaults to zss.Node.get_children().
                        get_label: A function get_label(node) == 'node label'.All labels are assumed to be strings at this time. Defaults to zss.Node.get_label().
                        label_distance: A function label_distance((get_label(node1), get_label(node2)) >= 0. This function should take the output of get_label(node) and return an integer greater or equal to 0 representing how many edits to transform the label of node1 into the label of node2. By default, this is string edit distance (if available). 0 indicates that the labels are the same. A number N represent it takes N changes to transform one label into the other.
                        Returns: An integer distance [0, inf+)
                        '''
                        distance.append(int(simple_distance(A, B, WeirdNode.get_children, WeirdNode.get_label, weird_dist)))
                index = [i for i, x in enumerate(distance) if x == min(distance)]


                for i in index:
                    minDistances[nfiPair[i]] = min(distance)

            min_val = min(minDistances.values())
            index = [k for k, x in minDistances.items() if x == min_val]
            parentMap[cfiNonLeaf[w]] = [k for k in index]

        else:
            # 선택된 cfiNonLeaf 노드에 부모가 없을 때 (for문 맨 처음부분)
            for j in range(len(nfiNonLeaf)):
                # reversed(nfiNL[j])는 nfiNL[j]번째의 리스트를 가져와서, 맨 뒤에부터 값을 하나씩 꺼낸다. 
                # 예시: y = <mapper.yangdm object at 0x7f276e2af370>
                for y in reversed(nfiNL[j]):
                    
                    # nfi의 노드에 부모가 있는지 확인
                    if y.parent is None:
                        B = WeirdNode(y.tag)
                    else:
                        B.addkid(WeirdNode(y.tag))

                # Zhang–Shasha Tree Edit Distance (장샤샤 알고리즘 거리 계산)
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