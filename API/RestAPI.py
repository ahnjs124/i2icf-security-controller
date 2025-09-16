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

from ncclient import manager

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

# 즉, 데코레이터에 설정된 요청이 들어오면 아래 함수가 실행됨
@api.route('/url/get', methods = ['GET'])
def restGetURLGroup():
    query = request.json
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["url"]
    
    query = {query} #{"name":key}
    res = col.find_one(query)
    
    return json.loads(dumps(res))

@api.route('/url/put', methods = ['PUT'])
def restInsertURLGroup():
    try:
        data = request.json
        print(data)
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["url"]
        
        res = col.insert_one(data)
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        print("Duplicate Key for ",data["name"])

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

@api.route('/user/put', methods = ['PUT'])
def restInsertUserGroup():
    try:
        data = request.json
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
        db = client["endpoint"]
        col = db["user"]
        
        res = col.insert_one(data)
        return "Success"
    except pymongo.errors.DuplicateKeyError:
        return "Duplicate Key for ",data["name"]
        

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
        

@api.route('/user/get', methods = ['GET'])
def restGetUserGroup():
    
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["user"]
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

@api.route('/location/get', methods = ['GET'])
def restGetLocationGroup():
    client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/")
    db = client["endpoint"]
    col = db["location"]
    query = request.json
    res = col.find_one(query)
    return res


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


#API for security policy tranlator - Input High-level policy (CFI), Output Low-level policy (NFI)
#http://ipv4:5000/high_level
@api.route('/high_level', methods=['PUT'])
def restInsertConfiguration():
    req = request.json
    #start = datetime.datetime.now()
    data = cleanNullTerms(req)
    print(data)
    xml = dict2xml(data)
    result = generatorv2.gen(xml)
    #end = datetime.datetime.now()
    # time = end-start
    # result["time"] = time.total_seconds()
    # result["optimal"] = optimal.total_seconds()
    # for x,y in result.items():
    #     print(x)
    #     print(y)

    #GET IP ADDRESS OF NSF
    for key,value in result.items():
      try:
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        db = client["nsfDB"]
        col = db["capabilities"]

        query = {"nsf-name":key}
        res = col.find_one(query)
        confd = {'address': res["nsf-access-info"]["ip"],
            'netconf_port': 2022,
            'username': 'admin',
            'password': 'admin'}

        confd_manager = manager.connect(
            host = confd["address"],
            port = confd["netconf_port"],
            username = confd["username"],
            password = confd["password"],
            hostkey_verify = False)
        
        configuration = f"""
    <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        {value}
    </nc:config>
    """
        confd_configuration = confd_manager.edit_config(target="running",config = configuration)
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
