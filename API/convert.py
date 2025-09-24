# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:09:31 2022

@author: Patrick
"""

import i2nsfMongoDB
from collections import OrderedDict

# mongo 데이터베이스
'''
iotlab@ubuntu:~/i2nsf-security-controller/API$ mongo
> show dbs
admin     0.000GB
config    0.000GB
endpoint  0.000GB           # endpoint에 값을 입력해서 추가하면 생성됨
local     0.000GB
mapping   0.000GB
nsfDB     0.000GB
> use endpoint
switched to db endpoint
> show collections
device                      # Endpoint의 Device Group에 값을 입력해서 추가하면 생성됨
mapping                     # insertMongoDB.py를 실행시키면 mapping이 생성됨
url                         # Endpoint의 Url Group에 값을 입력해서 추가하면 생성됨
user                        # Endpoint의 User Group에 값을 입력해서 추가하면 생성됨
>
>
>
> db.device.find().pretty()                             # Endpoint의 Device 컬렉션에 내용 확인
{
	"_id" : ObjectId("68cfb514a63020d2b413c9ce"),
	"name" : "webserver",
	"mac-address" : null,
	"range-ipv4-address" : {
		"start" : "192.168.18.137",
		"end" : "192.168.18.137"
	},
	"range-ipv6-address" : {
		"start" : null,
		"end" : null
	}
}
> db.user.find().pretty()                               # Endpoint의 user 컬렉션에 내용 확인
{
	"_id" : ObjectId("68d376f010b1df1528d49ed3"),
	"name" : "student",
	"mac-address" : null,
	"range-ipv4-address" : {
		"start" : "10.0.0.10",
		"end" : "10.0.0.20"
	},
	"range-ipv6-address" : {
		"start" : null,
		"end" : null
	}
}
> db.url.find().pretty()                                # Endpoint의 url 컬렉션에 내용 확인
{
	"_id" : ObjectId("68d38c77251aba3042ebe3fe"),
	"name" : "sns",
	"urls" : [
		"www.instagram.com"
	]
}
'''



# 고수준 정책(CFI/그룹명·URL·프로토콜 등)을 **NFI(YANG 경로·값)**로 변환하는 핵심 번역기
# I2NSF의 CFI/NFI는 IETF RFC 8329 (I2NSF 프레임워크) 에서 역할과 위치가 정의
# CFI: I2NSF Consumer-Facing Interface YANG Data Model
# NFI: I2NSF NSF-Facing Interface YANG Data Model

# highData 예시
# {1: 'policy', 2: 'rule', 13: 'webserver', 14: 'tcp', 16: 80, 17: 80, 71: 'drop'}
'''
● highData:
{ 1: 'policy',
  5: 'rule',
  12: 'student',
  13: 'webserver',
  14: 'tcp',
  16: 80,
  17: 80,
  71: 'drop'}


keys,values: 1 policy
i2nsfMongoDB.getAttributesMap(1)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb0f'), 'cfiPath': '/i2nsf-cfi-policy/name', 'cfiID': 1, 'map': [{'nfiId': 1, 'nfiPath': '/i2nsf-security-policy/name'}]}

keys,values: 5 rule
i2nsfMongoDB.getAttributesMap(5)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb12'), 'cfiPath': '/i2nsf-cfi-policy/rules/name', 'cfiID': 5, 'map': [{'nfiId': 7, 'nfiPath': '/i2nsf-security-policy/rules/name'}]}


keys,values: 71 drop
i2nsfMongoDB.getAttributesMap(71)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb3b'), 'cfiPath': '/i2nsf-cfi-policy/rules/action/primary-action/action', 'cfiID': 71, 'map': [{'nfiId': 177, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/ingress-action'}, {'nfiId': 178, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/egress-action'}, {'nfiId': 179, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/log-action'}, {'nfiId': 181, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/ingress-action'}, {'nfiId': 182, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/egress-action'}, {'nfiId': 183, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/log-action'}]}
'''


# highData는 사용자로부터 전달된 null값이 제외된 데이터 (CFI)
# 해당 CFI 데이터를 기반으로 방화벽 정책을 생성하는 NFI를 적용시켜야 한다
# 그걸 위해서는 mapping을 해야하는데, convertMongo에서 해당 mapping을 진행한다 

# highData 예시: {1: 'policy', 5: 'rule', 13: 'webserver', 14: 'tcp', 16: 80, 17: 80, 71: 'drop'}
def convertMongo(highData):
    lowData = OrderedDict()

    for keys,value in highData.items():
        # i2nsfMongoDB.getAttributesMap시,
        # mongo > endpoint 데이터베이스 > mapping 컬렉션 > {"cfiID":key}를 가지는 document를 lowAttr에 출력
        # 출력 예시: 
        '''
        {
        "_id" : ObjectId("68cfb411f645946c6a56eb10"),
        "cfiPath" : "/i2nsf-cfi-policy/language",
        "cfiID" : 2,
        "map" : [
                {
                "nfiId" : 2,
                "nfiPath" : "/i2nsf-security-policy/language"
                }
            ]
        }
        '''

        # highData에서 하나씩 뽑아내면서 해당 key값을 기반으로 
        # cfi와 nfi의 mapping 데이터를 가져와서 lowAttr에 입력
        lowAttr = i2nsfMongoDB.getAttributesMap(keys)
        ip=None

        # highData의 현재 키를 NFI 경로로 매핑하기 위한 메타(맵핑 표) 조회
        # 사용자 그룹 이름이 들어온 경우: MAC/IPv4/IPv6 범위를 NFI 경로에 채움


        ##### User Group (cfiID:12)
        # I2NSF 웹사이트에서 Endpoint의 User Group에 데이터가 입력 되었을 시,
        # mongo > endpoint 데이터베이스 > user 컬렉션 > {"name":value}를 가지는 document를 출력
        # keys,values: 12 student
        '''
        lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb16'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/source', 
        'cfiID': 12, 
        'map': [{'nfiId': 22, 'nfiPath': '/i2nsf-security-policy/rules/condition/layer-2/source-mac-address'}, {'nfiId': 46, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/source-ipv4-network'}, {'nfiId': 48, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/source-ipv4-range'}, {'nfiId': 67, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/source-ipv6-network'}, {'nfiId': 69, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/source-ipv6-range'}, {'nfiId': 76, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/source-port-number'}, {'nfiId': 94, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/source-port-number'}, {'nfiId': 105, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/source-port-number'}, {'nfiId': 117, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/source-port-number'}, {'nfiId': 138, 'nfiPath': '/i2nsf-security-policy/rules/condition/voice/source-voice-id'}]}
        '''
        # cfiID:12
        if (i2nsfMongoDB.getUserGroup(value)):
            userGroup = i2nsfMongoDB.getUserGroup(value)

            # 딕셔너리 기반 key:value 확인
            # MAC 주소가 있으면 MAC용 NFI 경로에 기록
            if userGroup['mac-address']:
                lowData[lowAttr['map'][0]['nfiPath']] = userGroup['mac-address']
               
            # IPv4 범위(start/end)가 있으면 IPv4용 NFI 경로에 "start end" 형식으로 기록
            if userGroup['range-ipv4-address']['start'] and userGroup['range-ipv4-address']['end']:
                ip = "ipv4"
                lowData[lowAttr['map'][2]['nfiPath']] = userGroup['range-ipv4-address']['start'] + " " + userGroup['range-ipv4-address']['end']
            
            # IPv6 범위(start/end)가 있으면 IPv6용 NFI 경로에 "start end" 형식으로 기록
            if userGroup['range-ipv6-address']['start'] and userGroup['range-ipv6-address']['end']:
                ip = "ipv6"
                lowData[lowAttr['map'][4]['nfiPath']] = userGroup['range-ipv6-address']['start'] + " " + userGroup['range-ipv6-address']['end']
        


        ##### Device Group (cifID:13)
        # 디바이스 그룹 이름이 들어온 경우: 사용자 그룹과 동일한 방식으로 MAC/IPv4/IPv6 채움
        # I2NSF 웹사이트에서 Endpoint의 Device Group에 데이터가 입력 되었을 시,
        # mongo > endpoint 데이터베이스 > device 컬렉션 > {"name":value}를 가지는 document를 출력
        # keys,values: 13 webserver
        '''
        lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb17'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/destination', 
        'cfiID': 13,
        'map': [{'nfiId': 20, 'nfiPath': '/i2nsf-security-policy/rules/condition/layer-2/destination-mac-address'}, {'nfiId': 39, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-network'}, {'nfiId': 41, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-range'}, {'nfiId': 60, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-network'}, {'nfiId': 62, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-range'}, {'nfiId': 80, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/destination-port-number'}, {'nfiId': 98, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/destination-port-number'}, {'nfiId': 109, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/destination-port-number'}, {'nfiId': 121, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/destination-port-number'}, {'nfiId': 139, 'nfiPath': '/i2nsf-security-policy/rules/condition/voice/destination-voice-id'}]}
        '''
        # cfiID:13
        elif (i2nsfMongoDB.getDeviceGroup(value)):
            deviceGroup = i2nsfMongoDB.getDeviceGroup(value)
            # 딕셔너리 기반 key:value 확인
            # MAC 주소 기록
            if deviceGroup['mac-address']:
                #print(lowAttr['map'][0]['nfiPath'])
                lowData[lowAttr['map'][0]['nfiPath']] = deviceGroup['mac-address']

            # IPv4 범위 기록    
            if deviceGroup['range-ipv4-address']['start'] and deviceGroup['range-ipv4-address']['end']:
                ip = "ipv4"
                lowData[lowAttr['map'][2]['nfiPath']] = deviceGroup['range-ipv4-address']['start'] + " " + deviceGroup['range-ipv4-address']['end']
            
            # IPv6 범위 기록
            if deviceGroup['range-ipv6-address']['start'] and deviceGroup['range-ipv6-address']['end']:
                ip = "ipv6"
                lowData[lowAttr['map'][4]['nfiPath']] = deviceGroup['range-ipv6-address']['start'] + " " + deviceGroup['range-ipv6-address']['end']
        
        

        ##### Location Group (cfiID:60,61,62,64,65,66)
        # highData는 resInfo에서 추출한 key값을 기반으로 만들어짐
        '''
        ● resInfo:
        [[False, 1, 'name', True, 1],
         ...
         [False, 6, 'country', True, 60],
         [False, 6, 'region', True, 61],
         [False, 6, 'city', True, 62],
         [False, 6, 'country', True, 64],
         [False, 6, 'region', True, 65],
         [False, 6, 'city', True, 66],
         ...]
         '''

        # highData의 key값이 country, region, city에 해당되는 60, 61, 62일 때 아래 부분 실행
        # 해당 key값들일 때, 그에 해당되는 value를 넣음
        # cfiID:60,61,62
        elif (keys == 60 or keys == 61 or keys == 62):
            locationGroup = i2nsfMongoDB.getLocationGroup(highData[60],highData[61],highData[62])
            if locationGroup["geo-ipv4-address"]["start"] and locationGroup["geo-ipv4-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv4/source-ipv4-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
            if locationGroup["geo-ipv6-address"]["start"] and locationGroup["geo-ipv6-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv6/source-ipv6-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
        
        
        # highData의 key값이 country, region, city에 해당되는 64, 65, 66일 때 아래 부분 실행
        # 해당 key값들일 때, 그에 해당되는 value를 넣음
        # cfiID:64,65,66
        elif (keys == 64 or keys == 65 or keys == 66):
            locationGroup = i2nsfMongoDB.getLocationGroup(highData[64],highData[65],highData[66])
            if locationGroup["geo-ipv4-address"]["start"] and locationGroup["geo-ipv4-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
            if locationGroup["geo-ipv6-address"]["start"] and locationGroup["geo-ipv6-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
        
        
        ##### URL Group (cfiID:31)
        # I2NSF 웹사이트에서 Endpoint의 URL Group에 데이터가 입력 되었을 시,
        # mongo > endpoint 데이터베이스 > url 컬렉션 > {"name":value}를 가지는 document를 출력
        # keys,values: 31 sns
        '''
        lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb22'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/url-category/url-name',
        'cfiID': 31, 
        'map': [{'nfiId': 135, 'nfiPath': '/i2nsf-security-policy/rules/condition/url-category/pre-defined'}, {'nfiId': 136, 'nfiPath': '/i2nsf-security-policy/rules/condition/url-category/user-defined'}]}
        '''
        # cfiID:31
        elif (i2nsfMongoDB.getURLGroup(value)):
            urlData = i2nsfMongoDB.getURLGroup(value)
            lowData[lowAttr['map'][1]['nfiPath']] = urlData['urls']



        ##### transport-layer-protocol, ICMP message (cfiID: 14,19)
        # highData의 transport-layer-protocol(14), ICMP message(19)
        '''
        lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb18'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/transport-layer-protocol',
        'cfiID': 14, 
        'map': [{'nfiId': 32, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/protocol'}, {'nfiId': 57, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/protocol'}]}
        '''
        # cfiID:14
        elif (lowAttr['cfiPath'] == "/i2nsf-cfi-policy/rules/condition/firewall/transport-layer-protocol"):
            val = i2nsfMongoDB.getNextHeader(value)["protocol-number"]
            if not ip:
                pass
            elif ip == "ipv6":
                lowData[lowAttr['map'][1]['nfiPath']] = int(val)
            else:
                lowData[lowAttr['map'][0]['nfiPath']] = int(val)

        # cfiID:19
        elif (lowAttr['cfiPath'] == "/i2nsf-cfi-policy/rules/condition/firewall/icmp/message"):
            if isinstance(value,str):
                value=[value]
            if '/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-range' in lowData or '/i2nsf-security-policy/rules/condition/ipv6/source-ipv6-range' in lowData:
                lowData[lowAttr['map'][0]['nfiPath']] = "icmpv6"
                for val in value:
                    lowData[lowAttr['map'][1]['nfiPath']] = int(i2nsfMongoDB.getICMPMessage(val)["icmpv6"]["type"])
                    lowData[lowAttr['map'][2]['nfiPath']] = int(i2nsfMongoDB.getICMPMessage(val)["icmpv6"]["code"])
            else: #Default is ICMPv4
                lowData[lowAttr['map'][0]['nfiPath']] = "icmpv4"
                for val in value:
                    lowData[lowAttr['map'][1]['nfiPath']] = int(i2nsfMongoDB.getICMPMessage(val)["icmpv4"]["type"])
                    lowData[lowAttr['map'][2]['nfiPath']] = int(i2nsfMongoDB.getICMPMessage(val)["icmpv4"]["code"])



        ##### Firewall (cfiID:14,16,17)
        # highData의 Transport Protocol(14), start port number(16), end port nubmer(17)
        '''
        lowAttr: {"_id" : ObjectId("68cfb411f645946c6a56eb19"), "cfiPath" : "/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/start", 
        "cfiID" : 16,
        "map" :[
                {
                    "nfiId" : 77,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/tcp/source-port-number/port-numbers"
                },
                {
                    "nfiId" : 81,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/tcp/destination-port-number/port-numbers"
                },


                {
                    "nfiId" : 95,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/udp/source-port-number/port-numbers"
                },
                {
                    "nfiId" : 99,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/udp/destination-port-number/port-numbers"
                },


                {
                    "nfiId" : 106,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/sctp/source-port-number/port-numbers"
                },
                {
                    "nfiId" : 110,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/sctp/destination-port-number/port-numbers"
                },


                {
                    "nfiId" : 118,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/dccp/source-port-number/port-numbers"
                },
                {
                    "nfiId" : 122,
                    "nfiPath" : "/i2nsf-security-policy/rules/condition/dccp/destination-port-number/port-numbers"
                }
              ]
            }
        '''
        # cfiID:16
        elif (lowAttr['cfiPath']=="/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/start"):
            start = value       # start port 번호 ("cfiID" : 16이면 start port 번호)
            end = highData[17]  # end port 번호 (highData[17])

            # highData[14]는 Transport Protocol를 선택함
            if (14 not in highData or highData[14] == "tcp"):
                if 12 in highData:
                    lowData[lowAttr['map'][0]['nfiPath']] = str(start) + " " + str(end)
                if 13 in highData:
                    lowData[lowAttr['map'][1]['nfiPath']] = str(start) + " " + str(end)
                if (12 not in highData and 13 not in highData):
                    lowData[lowAttr['map'][0]['nfiPath']] = str(start) + " " + str(end)
                    lowData[lowAttr['map'][1]['nfiPath']] = str(start) + " " + str(end)
            else:
                if highData[14] == "udp":
                    if 12 in highData:
                        lowData[lowAttr['map'][2]['nfiPath']] = str(start) + " " + str(end)
                    if 13 in highData:
                        lowData[lowAttr['map'][3]['nfiPath']] = str(start) + " " + str(end)
                    if (12 not in highData and 13 not in highData):
                        lowData[lowAttr['map'][2]['nfiPath']] = str(start) + " " + str(end)
                        lowData[lowAttr['map'][3]['nfiPath']] = str(start) + " " + str(end)
                elif highData[14] == "sctp":
                    if 12 in highData:
                        lowData[lowAttr['map'][4]['nfiPath']] = str(start) + " " + str(end)
                    if 13 in highData:
                        lowData[lowAttr['map'][5]['nfiPath']] = str(start) + " " + str(end)
                    if (12 not in highData and 13 not in highData):
                        lowData[lowAttr['map'][4]['nfiPath']] = str(start) + " " + str(end)
                        lowData[lowAttr['map'][5]['nfiPath']] = str(start) + " " + str(end)
                elif highData[14] == "dccp":
                    if 12 in highData:
                        lowData[lowAttr['map'][6]['nfiPath']] = str(start) + " " + str(end)
                    if 13 in highData:
                        lowData[lowAttr['map'][7]['nfiPath']] = str(start) + " " + str(end)
                    if (12 not in highData and 13 not in highData):
                        lowData[lowAttr['map'][6]['nfiPath']] = str(start) + " " + str(end)
                        lowData[lowAttr['map'][7]['nfiPath']] = str(start) + " " + str(end)
        

        ##### end port number (cfiID:17)
        # 위에서 관련 내용을 정의해둬서, 이 부분은 패스
        # cfiID:17
        elif (lowAttr['cfiPath']=="/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/end"):
            pass       
        
        '''
        위에 정의된 cfiID들
        User Group: 12
        Device Group: 13
        Location Group: 60,61,62,64,65,66
        Url Group: 31

        transport-layer-protocol: 14
        ICMP message: 19

        start port: 16
        end port: 17
        '''

        ##### 그 이외의 cfiID들은 아래의 코드로 동작함 (cfiID: 1 ~ 80까지)
        else:
            # 위에서 정의된 cfiID들을 제외한 나머지 highData 입력 cfiID들은,
            # 아래의 코드로 바로 나타낸다.
            # 예시: {1: 'policy', 5: 'rule'}
            lowData[lowAttr['map'][0]['nfiPath']] = value

    print("\n● convertMongo lowData:")
    print(lowData)
    print("--------------------------------")

    return(lowData)

# mydict = {"ipv4-capability": "source-address"}
# findCapability(mydict)
# highData = {1: 'security_policy_for_blocking_sns', 5: 'block_access_to_sns_during_office_hours', 12: 'employees', 30: 'sns-websites', 64: 'drop'}

# print(convertMongo(highData))
