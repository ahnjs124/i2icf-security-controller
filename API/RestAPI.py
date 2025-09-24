import pymongo
import netifaces as ni
import sys, getopt
import netifaces as ni
import re
from regex import R
from pprint import pprint
import json
from flask import Flask,request
from bson.json_util import dumps
from flask_cors import CORS
from dict2xml import dict2xml
import generatorv2
import configparser
from flask import Response

from ncclient import manager # NETCONF 클라이언트 라이브러리 (Python용)


# Read configuration file
# Python 표준 라이브러리 configparser 모듈을 사용해서 설정 파일 파서(parser) 객체를 생성
# 보통 .ini 형식의 설정 파일을 읽고 쓰는 데 사용
config = configparser.ConfigParser()
# config 객체에 현재 읽혀 있는 섹션 목록 출력 (처음에는 비어 있음)
config.sections()

# '../controller.ini' 파일을 읽어서 config 객체에 설정 정보 로드
# 이 파일에는 섹션과 키-값 쌍으로 구성된 설정 정보가 들어 있음
config.read('../controller.ini')
# 만약 ini파일에 [DEFAULT] 섹션이 있으면, config.sections()시 출력이 되지 않음
config.sections()


# Flask instance 생성 (allows to run REST API)
# Flask는 Python으로 작성된 마이크로 웹 프레임워크로, 웹 애플리케이션과 RESTful API를 쉽게 만들 수 있게 해줌
# Flask 인스턴스는 "웹 서버 역할"을 하며, 클라이언트의 요청을 처리하고 응답을 반환
# Flask 인스턴스 이름이 api이므로 @api.route로 데코레이터 설정
api = Flask(__name__)


# CORS(Cross-Origin Resource Sharing)는 웹 애플리케이션이 다른 도메인(오리진)의 리소스에 접근할 수 있도록 허용하는 메커니즘
# 기본적으로 웹 브라우저는 보안상의 이유로 다른 도메인 간의 요청을 제한하는 동일 출처 정책(Same-Origin Policy)을 따름
# CORS는 서버가 특정 도메인에서 오는 요청을 허용하도록 설정할 수 있게 해줌
# Flask-CORS는 Flask 애플리케이션에서 CORS를 쉽게 설정할 수 있도록 도와주는 확장 라이브러리

# 현재 react와 flask가 다른 포트를 사용하고 있으므로 CORS 설정이 필요
# React(3000) ↔ Flask(5000)는 오리진이 달라 CORS 허용 필요 
CORS(api)


# @api.route 데코레이터는 Flask에서 특정 URL 경로와 HTTP 메서드에 대한 요청을 처리하는 함수를 정의할 때 사용
# 예를 들어, @api.route('/url/get', methods = ['GET'])는 '/url/get' 경로에 대한 GET 요청이 들어오면 이를 특정 함수로 라우팅하도록 설정
# 클라이언트가 '/url/get' 경로로 GET 요청을 보내면, Flask는 자동으로 이 데코레이터가 붙은 함수를 호출하여 요청을 처리


# @api.route('~~', methods = ['GET'])는 현재 상태 확인
# @api.route('~~', methods = ['PUT'])는 상태 변경


# 데코레이터에 설정된 요청이 react에서 들어오면 아래 함수가 실행됨 (Flask 인스턴스의 이름이 api이므로 @api.route로 데코레이터 설정)






#### URL group
@api.route('/url/get', methods = ['GET'])
def restGetURLGroup():
    # request는 클라이언트가 보낸 HTTP 요청을 하는 Flask 전역 객체 (request.json는 해당 객체에서 JSON 데이터를 파싱 및 딕셔너리로 변환)
    query = request.json
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")  # 로컬 MongoDB 접속 객체 생성, MongoDB가 실행되고 있는지 확인 필요 (systemctl status mongod)
    db = client["endpoint"] # MongoDB의 "endpoint"라는 데이터베이스에 접근
    col = db["url"]
     
    query = {query} #{"name":key}
    res = col.find_one(query)
    
    return json.loads(dumps(res)) # HTTP에서 GET은 현재 상태 확인이므로 res를 반환

@api.route('/url/put', methods = ['PUT'])
def restInsertURLGroup():
    try:
        data = request.json
        print(data)
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["url"]
        
        res = col.insert_one(data)
        return "Success" # HTTP에서 PUT은 상태 변경이므로 Success 반환
    except pymongo.errors.DuplicateKeyError:
        print("Duplicate Key for ",data["name"])



#### Device group
@api.route('/device/get', methods = ['GET'])
def restGetDeviceGroup():
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["device"]
    query = request.json
    res = col.find_one(query)
    return res

@api.route('/device/put', methods = ['PUT'])
def restInsertDeviceGroup():
    try:
        data = request.json
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["device"]
        
        res = col.insert_one(data)
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate Key for ",data["name"]
        


#### User group
@api.route('/user/get', methods = ['GET'])
def restGetUserGroup():
    
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["user"]
    query = request.json
    res = col.find_one(query) # find_one은 query 기반으로 일치하는 document 1개 찾기
    return res


@api.route('/user/put', methods = ['PUT'])
def restInsertUserGroup():
    try:
        data = request.json
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["user"]
        res = col.insert_one(data) # insert_one은 해당 data를 mongo의 endpoint 데이터베이스의 user 컬렉션에 입력
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate Key for ",data["name"]
        


#### location group
@api.route('/location/get', methods = ['GET'])
def restGetLocationGroup():
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["location"]
    query = request.json
    res = col.find_one(query)
    return res

@api.route('/location/put', methods = ['PUT'])
def restInsertLocationGroup():
    try:
        data = request.json
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["location"]
        
        res = col.insert_one(data)
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        print("Duplicate Key for ",data["name"])




## registration interface
# Insert Capabilities of an NSF. The DMS delivers the capabilities via Registration Interface
@api.route('/register/nsf', methods = ['PUT'])
def restInsertCapability():
    try:
        data = request.json
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["nsfDB"]
        col = db["capabilities"]
        print(data)
        res = col.insert_one(data)
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        print("Duplicate Key for ",data["nsf-name"])
        return Response(f"Duplicate Key for {data['nsf-name']}", status=400)


# nsfDB database의 capabilities 컬렉션에서 query에 해당하는 모든 NSF의 Capability를 반환
# Get all Capabilities of NSFs in the nsfDB database
@api.route('/nsfDB/get', methods = ['GET'])
def restGetAllCapability(query={}):
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["nsfDB"]
    col = db["capabilities"]
    result = {}
    result["nsf"] = []
    for res in col.find(query):
        result["nsf"].append(res)
    return json.loads(dumps(result)) 




# API for security policy tranlator
# Input: JSON format High-level policy (CFI) 
# (Configuration 탭에서 Submit 버튼 누를 시 Flask 서버로 전송된 데이터) (configuration.js 에서 fetch()로 보낸 JSON 데이터)

# Output: XML format Low-level policy (NFI)
# http://ipv4:5000/high_level
@api.route('/high_level', methods=['PUT'])
def restInsertConfiguration():
    # request는 클라이언트가 보낸 HTTP 요청을 하는 Flask 전역 객체 (request.json는 해당 객체에서 JSON 데이터를 파싱 및 딕셔너리로 변환)
    req = request.json
    print("\n● Received high-level policy (JSON):")
    pprint(req, indent=2)
    print("--------------------------------")
    
    # null 값은 제거 후 남은 것들만 확인
    data = cleanNullTerms(req)
    print("\n● High-level policy (without NULL)(JSON):")
    pprint(data, indent=2)
    print("--------------------------------")

    # JSON to XML
    # dict2xml 모듈을 사용해서 JSON을 XML 문자열로 변환
    xml = dict2xml(data)
    print("\n● High-level policy (JSON to XML):")
    pprint(xml, indent=2)
    print("--------------------------------")
    
    # High-level policy XML to Low-level policy XML for each NSF
    # generatorv2 모듈을 사용해서 High-leve policy XML 문자열을 각 NSF에 맞는 Low-level XML 형식으로 변환
    # result 변수는 변환된 XML 데이터를 담고 있는 딕셔너리 형태
    # {nsf-name: xml-configuration, nsf-name2: xml-configuration2, ...} 형태
    result = generatorv2.gen(xml)
    print("\n● High-level policy XML to Low-level policy XML for each NSF:")   
    pprint(result, indent=2)
    print("--------------------------------")
   
   
    # GET IP ADDRESS OF NSF
    # {key:value} = {firewall:"firewall 내용"} {web-filtering:"web-filtering 내용"} 으로 2가지
    for key,value in result.items():
      try:
        # MongoDB 클라이언트 객체를 만듬
        # 이 객체를 통해 MongoDB 서버와 연결하고, 데이터베이스/컬렉션에 접근하거나 데이터를 주고 받을 수 있음
        # mongodb:// → MongoDB에 접속한다는 프로토콜
        # 127.0.0.1 → 로컬호스트 IP (즉, 현재 내 컴퓨터에서 실행 중인 MongoDB 서버)
        # 27017 → MongoDB 서버의 기본 포트 번호
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/") # 내 PC에 띄워진 MongoDB 인스턴스에 연결


        # 웹페이지에서 submit을 누르기 전에는 mongoDB의 데이터베이스를 검색해보면 print(client.list_database_names()) nsfDB 데이터베이스가 존재하지 않음
        # 하지만 submit을 누르면 DMS쪽에서 Security Controller쪽으로 nsfDB를 전달하여 Security Controller의 mongoDB 데이터베이스에 nsfDB가 생성됨
        db = client["nsfDB"] # "nsfDB" 데이터베이스
        col = db["capabilities"] # "nsfDB"안의 "capabilities" 컬렉션(테이블과 유사) 선택
        
        query = {"nsf-name":key} # {"nsf-name":"firewall"}
        res = col.find_one(query)
        print("NSF IP:", res["nsf-access-info"]["ip"])


        ### confd 입력 데이터
        #### 아래는 최종 번역된 Low-Level Policy를 ConfD(=NSF 관리 서버)에 실제로 “적용”하는 코드
        confd = {'address': res["nsf-access-info"]["ip"],
            'netconf_port': 2022,
            'username': 'admin',
            'password': 'admin'}


        # from ncclient import manager
        # ncclient = Python용 NETCONF 클라이언트 라이브러리
        # IETF NETCONF 프로토콜(SSH 기반 장비 설정 프로토콜)을 파이썬에서 쉽게 다룰 수 있도록 해줌
       
        # manager = ncclient에서 NETCONF 서버 연결 및 조작을 쉽게 해주는 모듈
        # manager.connect() = 가장 자주 쓰이는 함수, NETCONF 세션 열 때 사용
        
        # connect → NETCONF 서버(예: ConfD, 라우터, 스위치)에 연결
        # get-config, edit-config → 설정 조회/변경
        # rpc → 사용자 정의 RPC 호출
        # close-session → 세션 종료
        confd_manager = manager.connect(
            host = confd["address"],
            port = confd["netconf_port"],
            username = confd["username"],
            password = confd["password"],
            hostkey_verify = False)
        

        # NETCONF에서 설정을 변경할 때는 <edit-config> RPC 안에 <config> 요소를 포함해야 함.
        # 여기서 {value} 부분에는 실제 적용하려는 Low-Level Policy XML이 들어가야 함.
        configuration = f"""
    <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        {value}
    </nc:config>
    """

        # 설정 반영하기
        # edit_config() : NETCONF 표준 RPC 호출
        # target="running" : ConfD의 “running datastore”에 설정 적용
        # config=configuration : 위에서 만든 XML을 넘겨줌
        confd_configuration = confd_manager.edit_config(target="running",config = configuration)
        
        # NETCONF 세션 종료
        confd_manager.close_session()
      except:
        print("Cannot connect to NSF's confd")
    
    return result



def cleanNullTerms(d):
   clean = {}
   for k, v in d.items():
      if isinstance(v, dict):
         nested = cleanNullTerms(v)
         if len(nested.keys()) > 0:
            clean[k] = nested
      elif v is not None:
         clean[k] = v
   return clean 

def main(argv):
#  print(sys.argv[1])
  ip = ''
  opts, args = getopt.getopt(argv,"h",["ip=","if="])
  for opt, arg in opts:
    if opt == '-h':
      print("RestAPI.py [--ip <ip-address>|--if <interface-name>]")
      sys.exit()
    elif opt in ("--ip"):
      if re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",arg):
        ip = arg
      else:
        print(f"{arg} is not a valid IP address")
        sys.exit()
    elif opt in ("--if"):
      try:
        ip = ni.ifaddresses(arg)[ni.AF_INET][0]['addr']
      except ValueError:
        print(f"Invalid interface value. The value must be: {ni.interfaces()}")
        sys.exit()
  if ip == '':
    print(f"""Put the IP address or interface.\nUsage:\nRestAPI.py [--ip <ip-address>|--if <interface-name>]""")
  else:
    api.run(host=ip)

if __name__== '__main__':
  main(sys.argv[1:])
