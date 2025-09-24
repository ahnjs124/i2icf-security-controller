import i2nsfMongoDB
import os
import json
from pprint import pprint

# INSERT URL GROUP
# i2nsfMongoDB.insertURLGroup({'name':"sns-websites",'urls':["facebook","instagram"]})
# i2nsfMongoDB.insertURLGroup({'name':"search-engine",'urls':["google","duckduckgo","bing"]})

# INSERT USER GROUP
# i2nsfMongoDB.insertUserGroup({'name':"employees","mac-address":None,"range-ipv4-address":{"start":"192.0.2.0","end":"192.0.2.255"},"range-ipv6-address":{"start":None,"end":None}})
# i2nsfMongoDB.insertUserGroup({'name':"employeesv6","mac-address":None,"range-ipv4-address":{"start":None,"end":None},"range-ipv6-address":{"start":"2001:db8:1::","end":"2001:db8:1:f:ffff:ffff:ffff:ffff"}})

# Capability Mapping 삽입
# mongo의 데이터베이스에 mapping을 생성시키고, capabilityMapping 내용을 넣음
# INSERT CAPABILITY MAPPING FROM AUTOMATIC DATA MODEL MAPPER
with open("capabilityMapping.json") as f:
    capDict = json.load(f)
    #print(capDict["capabilityMapping"])
    i2nsfMongoDB.insertCapabilityMapping(capDict["capabilityMapping"])

# INSERT CAPABILITY PATH
# mongo의 mapping 데이터베이스에 capabilityPath 내용을 넣음
with open("capabilityPath.json") as f:
    capDict = json.load(f)
    #print(capDict["capabilityPath"])
    i2nsfMongoDB.insertCapabilityPath(capDict["capabilityPath"])

# print(i2nsfMongoDB.getCapabilityPath("ipv4-capability"))


# Attribute Mapping
# 이 부분을 실행시키면 mongo의 데이터베이스에 endpoint가 생성됨
# ★ MongoDB에서 consumer facing interface(CFI) ID와 NSF-facing-interface(NFI) ID를 서로 Mapping시킴
i2nsfMongoDB.insertAttributesMap('DataModel/cfi_minus.txt','DataModel/nfi.txt')


#INSERT CAPABILITY
# i = 0
# for filename in os.listdir("capability"):
#     file = os.path.join("capability",filename)
#     if os.path.isfile(file):
#         with open(file) as f:
#             data = json.load(f)
#             #data["nsf-name"] += str(i)
#             # i+=1
#             i2nsfMongoDB.insertCapability(data)

# with open("capability/time-based-firewall.json") as f:
#     data =json.load(f)
#     i2nsfMongoDB.insertCapability(data)

# INSERT ICMP MESSAGE MAPPING
# mongo의 mapping 데이터베이스에 icmp-code-type 내용을 넣음
with open("icmp-code-type.json") as f:
    icmpDict = json.load(f)
    i2nsfMongoDB.insertICMPMessage(icmpDict["icmp-code-type"])

# INSERT NEXT HEADER (PROTOCOL) MAPPING
# mongo의 mapping 데이터베이스에 next-header 내용을 넣음
with open("next-header.json") as f:
    nhDict = json.load(f)
    i2nsfMongoDB.insertNextHeader(nhDict["next-header"])



# GET URL GROUP
# urls = i2nsfMongoDB.getURLGroup("sns-websites")
# pprint(urls)

# GET USER GROUP
# user = i2nsfMongoDB.getUserGroup("employees")
# pprint(user)

# GET Capability Mapping
#capMap=i2nsfMongoDB.getCapabilityMapping()
#print(c["/i2nsf-security-policy/rules/condition/icmp/version"])

#print(i2nsfMongoDB.findCapability(test))

# GET NEXT HEADER AND ICMP MESSAGE MAP
# print(int(i2nsfMongoDB.getNextHeader("tcp")["protocol-number"]))
# print(int(i2nsfMongoDB.getICMPMessage("echo")["code"]))
