# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:09:31 2022

@author: Patrick
"""

import i2nsfMongoDB
from collections import OrderedDict

# 고수준 정책(CFI/그룹명·URL·프로토콜 등)을 **NFI(YANG 경로·값)**로 변환하는 핵심 번역기
# I2NSF의 CFI/NFI는 IETF RFC 8329 (I2NSF 프레임워크) 에서 역할과 위치가 정의
# CFI: I2NSF Consumer-Facing Interface YANG Data Model
# NFI: I2NSF NSF-Facing Interface YANG Data Model

# highData 예시
# {1: 'policy111', 2: 'rule111', 13: 'webserver', 14: 'tcp', 16: 80, 17: 80, 71: 'drop'}
'''
● highData:
{ 1: 'policy111',
  5: 'rule111',
  13: 'webserver',
  14: 'tcp',
  16: 80,
  17: 80,
  71: 'drop'}

keys,values: 1 policy111
i2nsfMongoDB.getAttributesMap(1)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb0f'), 'cfiPath': '/i2nsf-cfi-policy/name', 'cfiID': 1, 'map': [{'nfiId': 1, 'nfiPath': '/i2nsf-security-policy/name'}]}

keys,values: 5 rule111
i2nsfMongoDB.getAttributesMap(5)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb12'), 'cfiPath': '/i2nsf-cfi-policy/rules/name', 'cfiID': 5, 'map': [{'nfiId': 7, 'nfiPath': '/i2nsf-security-policy/rules/name'}]}

keys,values: 13 webserver
i2nsfMongoDB.getAttributesMap(13)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb17'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/destination', 'cfiID': 13, 'map': [{'nfiId': 20, 'nfiPath': '/i2nsf-security-policy/rules/condition/layer-2/destination-mac-address'}, {'nfiId': 39, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-network'}, {'nfiId': 41, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-range'}, {'nfiId': 60, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-network'}, {'nfiId': 62, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-range'}, {'nfiId': 80, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/destination-port-number'}, {'nfiId': 98, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/destination-port-number'}, {'nfiId': 109, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/destination-port-number'}, {'nfiId': 121, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/destination-port-number'}, {'nfiId': 139, 'nfiPath': '/i2nsf-security-policy/rules/condition/voice/destination-voice-id'}]}

keys,values: 14 tcp
i2nsfMongoDB.getAttributesMap(14)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb18'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/transport-layer-protocol', 'cfiID': 14, 'map': [{'nfiId': 32, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv4/protocol'}, {'nfiId': 57, 'nfiPath': '/i2nsf-security-policy/rules/condition/ipv6/protocol'}]}

keys,values: 16 80
i2nsfMongoDB.getAttributesMap(16)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb19'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/start', 'cfiID': 16, 'map': [{'nfiId': 77, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/source-port-number/port-numbers'}, {'nfiId': 81, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/destination-port-number/port-numbers'}, {'nfiId': 95, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/source-port-number/port-numbers'}, {'nfiId': 99, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/destination-port-number/port-numbers'}, {'nfiId': 106, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/source-port-number/port-numbers'}, {'nfiId': 110, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/destination-port-number/port-numbers'}, {'nfiId': 118, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/source-port-number/port-numbers'}, {'nfiId': 122, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/destination-port-number/port-numbers'}]}

keys,values: 17 80
i2nsfMongoDB.getAttributesMap(17)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb1a'), 'cfiPath': '/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/end', 'cfiID': 17, 'map': [{'nfiId': 77, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/source-port-number/port-numbers'}, {'nfiId': 81, 'nfiPath': '/i2nsf-security-policy/rules/condition/tcp/destination-port-number/port-numbers'}, {'nfiId': 95, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/source-port-number/port-numbers'}, {'nfiId': 99, 'nfiPath': '/i2nsf-security-policy/rules/condition/udp/destination-port-number/port-numbers'}, {'nfiId': 106, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/source-port-number/port-numbers'}, {'nfiId': 110, 'nfiPath': '/i2nsf-security-policy/rules/condition/sctp/destination-port-number/port-numbers'}, {'nfiId': 118, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/source-port-number/port-numbers'}, {'nfiId': 122, 'nfiPath': '/i2nsf-security-policy/rules/condition/dccp/destination-port-number/port-numbers'}]}

keys,values: 71 drop
i2nsfMongoDB.getAttributesMap(71)
=> lowAttr: {'_id': ObjectId('68cfb411f645946c6a56eb3b'), 'cfiPath': '/i2nsf-cfi-policy/rules/action/primary-action/action', 'cfiID': 71, 'map': [{'nfiId': 177, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/ingress-action'}, {'nfiId': 178, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/egress-action'}, {'nfiId': 179, 'nfiPath': '/i2nsf-security-policy/rules/action/packet-action/log-action'}, {'nfiId': 181, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/ingress-action'}, {'nfiId': 182, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/egress-action'}, {'nfiId': 183, 'nfiPath': '/i2nsf-security-policy/rules/action/flow-action/log-action'}]}
'''


# highData는 사용자로부터 전달된 null값이 제외된 데이터 (CFI)
# 해당 CFI 데이터를 기반으로 방화벽 정책을 생성하는 NFI를 적용시켜야 한다
# 그걸 위해서는 mapping을 해야하는데, convertMongo에서 해당 mapping을 진행한다
def convertMongo(highData):
    lowData = OrderedDict()

    for keys,value in highData.items():
        lowAttr = i2nsfMongoDB.getAttributesMap(keys)
        ip=None

        #### highData의 현재 키를 NFI 경로로 매핑하기 위한 메타(맵핑 표) 조회

        # 사용자 그룹 이름이 들어온 경우: MAC/IPv4/IPv6 범위를 NFI 경로에 채움
        if (i2nsfMongoDB.getUserGroup(value)):
            userGroup = i2nsfMongoDB.getUserGroup(value)

            # MAC 주소가 있으면 MAC용 NFI 경로에 기록
            if userGroup['mac-address']:
                #print(lowAttr['map'][0]['nfiPath'])
                lowData[lowAttr['map'][0]['nfiPath']] = userGroup['mac-address']
            
            # IPv4 범위(start/end)가 있으면 IPv4용 NFI 경로에 "start end" 형식으로 기록
            if userGroup['range-ipv4-address']['start'] and userGroup['range-ipv4-address']['end']:
                ip = "ipv4"
                lowData[lowAttr['map'][2]['nfiPath']] = userGroup['range-ipv4-address']['start'] + " " + userGroup['range-ipv4-address']['end']
            
            # IPv6 범위(start/end)가 있으면 IPv6용 NFI 경로에 "start end" 형식으로 기록
            if userGroup['range-ipv6-address']['start'] and userGroup['range-ipv6-address']['end']:
                ip = "ipv6"
                lowData[lowAttr['map'][4]['nfiPath']] = userGroup['range-ipv6-address']['start'] + " " + userGroup['range-ipv6-address']['end']
        
        # 디바이스 그룹 이름이 들어온 경우: 사용자 그룹과 동일한 방식으로 MAC/IPv4/IPv6 채움
        elif (i2nsfMongoDB.getDeviceGroup(value)):
            deviceGroup = i2nsfMongoDB.getDeviceGroup(value)

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
        
        
        elif (keys == 60 or keys == 61 or keys == 62):
            locationGroup = i2nsfMongoDB.getLocationGroup(highData[60],highData[61],highData[62])
            if locationGroup["geo-ipv4-address"]["start"] and locationGroup["geo-ipv4-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv4/source-ipv4-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
            if locationGroup["geo-ipv6-address"]["start"] and locationGroup["geo-ipv6-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv6/source-ipv6-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
        
        
        elif (keys == 64 or keys == 65 or keys == 66):
            locationGroup = i2nsfMongoDB.getLocationGroup(highData[64],highData[65],highData[66])
            if locationGroup["geo-ipv4-address"]["start"] and locationGroup["geo-ipv4-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv4/destination-ipv4-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
            if locationGroup["geo-ipv6-address"]["start"] and locationGroup["geo-ipv6-address"]["end"]:
                lowData["/i2nsf-security-policy/rules/condition/ipv6/destination-ipv6-range"] = locationGroup["geo-ipv4-address"]["start"] + " " +locationGroup["geo-ipv4-address"]["end"]
        
        
        # URL 그룹: URL 목록을 해당 NFI 경로에 매핑
        elif (i2nsfMongoDB.getURLGroup(value)):
            urlData = i2nsfMongoDB.getURLGroup(value)
            lowData[lowAttr['map'][1]['nfiPath']] = urlData['urls']


        elif (lowAttr['cfiPath'] == "/i2nsf-cfi-policy/rules/condition/firewall/transport-layer-protocol"):
            val = i2nsfMongoDB.getNextHeader(value)["protocol-number"]
            if not ip:
                pass
            elif ip == "ipv6":
                lowData[lowAttr['map'][1]['nfiPath']] = int(val)
            else:
                lowData[lowAttr['map'][0]['nfiPath']] = int(val)
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
        elif (lowAttr['cfiPath']=="/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/start"):
            start = value
            end = highData[17]
            #print(highData[17])
            if (14 not in highData or highData[14] =="tcp"):
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
        elif (lowAttr['cfiPath']=="/i2nsf-cfi-policy/rules/condition/firewall/range-port-number/end"):
            pass
        else:
            lowData[lowAttr['map'][0]['nfiPath']] = value

    print("\n● convertMongo lowData:")
    print(lowData)
    print("--------------------------------")

    return(lowData)

# mydict = {"ipv4-capability": "source-address"}
# findCapability(mydict)
# highData = {1: 'security_policy_for_blocking_sns', 5: 'block_access_to_sns_during_office_hours', 12: 'employees', 30: 'sns-websites', 64: 'drop'}

# print(convertMongo(highData))
