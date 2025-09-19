# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:09:31 2022

@author: Patrick
"""

import i2nsfMongoDB
from collections import OrderedDict


# 고수준 정책(CFI/그룹명·URL·프로토콜 등)을 **NFI(YANG 경로·값)**로 변환하는 핵심 번역기
def convertMongo(highData):
    lowData = OrderedDict()


    # highData 예시
    # {1: 'newPolicy', 2: 'newRule', 13: 'webserver', 14: 'tcp', 16: 80, 17: 80, 71: 'drop'}
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
            print(highData[17])
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

    print(lowData)
    return(lowData)

# mydict = {"ipv4-capability": "source-address"}
# findCapability(mydict)
# highData = {1: 'security_policy_for_blocking_sns', 5: 'block_access_to_sns_during_office_hours', 12: 'employees', 30: 'sns-websites', 64: 'drop'}

# print(convertMongo(highData))
