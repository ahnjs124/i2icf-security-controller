import React from 'react';
import './configuration.css'
import Resultmodal from '../modals_components/resultmodal';
import { useState } from 'react'

// Configuration 컴포넌트 정의 및 내보내기
// App.js에서 component = <Configuration mode={mode}/>; 가 실행될 때 이 컴포넌트가 렌더링됨
export default function Configuration({mode}) {
  
  // 기본적으로 event, condition, action 박스는 닫혀있고, 체크박스를 클릭하면 열림
  const [eventChecked, setEventChecked] = useState(false);
  const [conditionChecked, setConditionChecked] = useState(false);
  const [actionChecked, setActionChecked] = useState(false);
  
  // 모달(팝업창) 창 열림 상태 관리
  const [openModal, setOpenModal] = useState(false);

// Policy
const [PolicyName, setPolicyName]= useState(""); // Policy의 Name 변수
const [PolicyLanguage, setPolicyLanguage] = useState(""); // Policy의 Language 변수
const [ResolutionStrategy, setResolutionStrategy]= useState("") // Policy의 Resolution Strategy 변수

// Rule
const [RuleName, setRuleName] = useState(""); // Rule의 Name 변수
const [PriorityName, setPriorityName] = useState(""); // Rule의 Priority 변수

// Event
const [SystemEvent, setSystemEvent] = useState(""); // Event의 System Event 변수
const [Systemevent, setSystemAlarm] = useState(""); // Event의 System Alarm 변수

//Condition
const [FirewallSource, setFirewallSource] = useState(""); // Firewall의 Source 변수
const [FirewallDest, setFirewallDest] = useState(""); // Firewall의 Destination 변수
const [FirewallStartPortNum, setFirewallStartPortNum] = useState(""); // Firewall의 Start Port Number 변수
const [FirewallEndPortNum, setFirewallEndPortNum] = useState(""); // Firewall의 End Port Number 변수
const [FirewallIcmpMessage, setFirewallIcmpmessage] = useState(""); // Firewall의 ICMP Message 변수
const [FirewallSystemAlarm, setFirewallSystemAlarm] = useState(""); // Firewall의 System Alarm 변수

// Anti-DDOS
const [DdosPacketRateThreshod, setDdosPacketRateThreshod] = useState(""); // Anti-DDOS의 Packet Rate Threshold 변수
const [DdosByteRateThreshod, setDdosByteRateThreshod] = useState(""); // Anti-DDOS의 Byte Rate Threshold 변수
const [DdosFlowRateThreshod, setDdosFlowRateThreshod] = useState(""); // Anti-DDOS의 Flow Rate Threshold 변수

// Antivirus
const [ExceptionFiles, setExceptionFiles] =useState(""); // Anti-Virus의 Exception Files 변수

// Payload
const [PayloadContent,setPayloadContent] = useState("") // Payload의 Content 변수

// URL-Categroy
const [UrlName,setUrlName] = useState("") // URL의 Url-name 변수

// Voice
const [VoiceSourceId,setVoiceSourceId] = useState("") // Voice의 Source Id 변수
const [VoiceDestId,setVoiceDestId] = useState("") // Voice의 Destination Id 변수
const [VoiceUserAgent,setVoiceUserAgent] = useState("") // Voice의 User Agent 변수

// Context Time
const [ContextStartDateTime,setContextStartDateTime] = useState("") // Context의 Start Date Time 변수
const [ContextEndDateTime,setContextEndDateTime] = useState("") // Context의 End Date Time 변수


// variables for the frequency buttons
// only once
const [frequencyOnlyOnce, setFrequencyOnlyOnce] = useState(false); // only-once 선택 상태 변수
const [StartTime, setStartTime] = useState(""); // only-once 선택시 Frequency의 Start Time 변수
const [EndTime, setEndTime] = useState(""); // only-once 선택시 Frequency의 End Time 변수

// weekly
const [frequencyWeekly, setFrequencyWeekly] = useState(false); // weekly 선택 상태 변수
const [Day, setDay] = useState(""); // weekly 선택시 Frequency의 Day 변수

// monthly
const [frequencyMonthly, setFrequencyMonthly] = useState(false); // monthly 선택 상태 변수
const [MonthlyDay, setMonthlyDay] = useState(""); // monthly 선택시 Frequency의 Day 변수

// yearly
const [frequencyYearly, setFrequencysYearly] = useState(false); // yearly 선택 상태 변수
const [YearlyMonth, setYearlyMonth] = useState(""); // yearly 선택시 Frequency의 Month 변수


// Application
const [ApplicationProtocal,setApplicationProtocal] = useState("") // Application의 Protocal 변수

// Device Type
const [DeviceType,setDeviceType] = useState("") // Device Type의 Device 변수

//User
const [UserID, setUserID] = useState();     // User 클릭시 User ID 변수
const [UserName, setUserName] = useState(); // User 클릭시 User Name 변수

// Group
const [GroupID, setGroupID] = useState();   // Group 클릭시 Group ID 변수
const [GroupName, setGroupName] = useState(); // Group 클릭시 Group Name 변수


// variables for the users radio buttons 
const [oneUser, setOneUser] = useState(false); // Users에서 User 선택 상태 변수
const [groupUser, setGroupUser] = useState(false); // Users에서 Group 선택 상태 변수


// Geograpghic Location
const [GeoSource, setGeoSource] = useState(""); // Geographic Location의 Source 변수
const [GeoDest, setGeoDest] = useState(""); // Geographic Location의 Destination 변수

// Thread-Feed
const [ThreadName, setThreadName] = useState(""); // Thread-Feed의 Name 변수

// Action 체크박스 클릭 시 열리는 Action 박스 안의 변수들
const [PrimaryAction, setPrimaryAction ] = useState(""); // Action의 Primary Action 변수
const [SeciondaryAction, setSecondaryAction ] = useState(""); // Action의 Secondary Action 변수




// Event 체크박스 클릭 시 상태 변경 함수
const handleEventCheck = () => {
  setEventChecked(!eventChecked);
};

// Condition 체크박스 클릭 시 상태 변경 함수
const handleConditionCheck = () => {
  setConditionChecked(!conditionChecked);
};

// Action 체크박스 클릭 시 상태 변경 함수
const handleActionCheck = () => {
  setActionChecked(!actionChecked);
};


// Policy_infos_form 객체: 폼 데이터를 저장하는 상태 변수
const [Policy_infos_form, setPolicyInfosform] = useState({
  "i2nsf-cfi-policy": { 
      "name": null,
      "language": null,
      "resolution-strategy":null,
      "rules" : {
          "name":null,
          "priority":null,
          "event":{
              "system-event":null,
              "system-alarm":null
          },
          "condition": {
              "firewall": {
                  "source":null,
                  "destination":null,
                  "transport-layer-protocol": null,
                  "range-port-number": {
                      "start":null,
                      "end":null
                  },
                  "icmp": {
                      "message":null
                  }
              },
              "ddos" : {
                  "rate-limit" : {
                      "packet-rate-threshold":null,
                      "byte-rate-threshold":null,
                      "flow-rate-threshold":null
                  }
              },
              "anti-virus" : {
                  "exception-file":null
              },
              "payload" : {
                  "content" : null
              },
              "url-category": {
                  "url-name" :null
              },                
              "voice" : {
                  "source-id": null,
                  "destination-id":null,
                  "user-agent":null
              },
              "context": {
                  "time": {
                      
                      "start-date-time":null,
                      "end-date-time":null,
                      "period": {
                          "start-time":null,
                          "end-time" :null,
                          "day":null,
                          "date":null,
                          "month":null
                      },
                      "frequency" : null
                  },
                  "application": {
                      "protocol": null
                  },
                  "device-type": {
                      "device": null
                  },
                  "users": {
                      "user":{
                          "id":null,
                          "name":null
                      },
                      "group":{
                          "id":null,
                          "name":null
                      }
                  },
                  "geographic-location":{
                      "source": {
                        "country": null,
                        "region": null,
                        "city": null
                      },
                      "destination": {
                        "country": null,
                        "region": null,
                        "city": null
                      }
                  }
              },
              "thread-feed": {
                  "name":null
              }
          },

          "action":{
              "primary-action": {
                  "action": null
              },
              "secondary-action": {
                  "log-action": null
              }
          }
      }
  }
});


// Policy_infos_form 객체: 폼 데이터를 저장하는 상태 변수
var temp2 = Policy_infos_form

// XML 결과를 저장하는 상태 변수
const [xml, setxml ] = useState("");

// 폼 제출 시 실행되는 함수
const ClickSubmit =async (e) => {
  e.preventDefault()
  
  // Condition > Context > Time > Frequency에서 선택한 값에 따라 Policy_infos_form 객체의 frequency 속성 설정
  if(frequencyOnlyOnce === true){
    // temp2 변수에 입력된 Policy_infos_form에서 frequency 속성 설정
    temp2['i2nsf-cfi-policy'].rules.condition.context.time.frequency = "only-once"
    // 그리고 setPolicyInfosform으로 Policy_infos-form 상태 변수 업데이트
    setPolicyInfosform(temp2)
  } 
  else if(frequencyWeekly ===true){
    temp2['i2nsf-cfi-policy'].rules.condition.context.time.frequency = "weekly"
    setPolicyInfosform(temp2)

  } 
  else if(frequencyMonthly ==true){
    temp2['i2nsf-cfi-policy'].rules.condition.context.time.frequency = "monthly"
    setPolicyInfosform(temp2)

  }
  else if(frequencyYearly == true){
    temp2['i2nsf-cfi-policy'].rules.condition.context.time.frequency = "yearly"
    setPolicyInfosform(temp2)
  }


  /*
  클라이언트(React) (포트 3000)
  - npm start -> React 개발서버 실행 -> React 앱을 브라우저에서 띄워줌.
  - React는 클라이언트쪽으로 사용자 인터페이스(UI)를 제공하고, 사용자의 입력을 받아 Flask 서버에 요청을 보냄.

  서버(Flask) (포트 5000)
  - python3 RestAPI.py로 실행된 Flask 앱이 5000번 포트에서 요청을 기다립니다.
  - React가 보낸 요청을 받고 api.route 데코레이터로 정의된 엔드포인트에서 요청을 처리한 뒤 React로 응답을 돌려줌.
  */


  // 모달(팝업창) 열기
  // await fetch(): 서버가 응답할 때까지 기다렸다가 Response 객체 받음
  // await response.json(): 응답 본문(body)을 JSON으로 파싱할 때까지 기다렸다가 결과 받음

  
  // Flask 서버가 http://127.0.0.1:5000 주소에서 실행 중일 때, Flask 서버로 Policy_infos_form 데이터 보내기 
  // PUT 메서드로 /high_level 엔드포인트에 요청
  const response = await fetch('http://127.0.0.1:5000/high_level', { // fetch()는 브라우저가 제공하는 Web API로, React에 상관없이 네트워크 요청을 보냄(HTTP GET/POST/PUT/DELETE 등)
      method: 'PUT', // HTTP 메서드를 PUT으로 지정 (데이터 수정/업데이트 할 때 주로 사용)
      body: JSON.stringify(Policy_infos_form), // Policy_infos_form 객체를 JSON 문자열로 변환해 요청 본문(body)에 담음
      headers: {
          'Content-Type': 'application/json'  // 클라이언트에서 서버로 보낼 데이터 형식이 JSON임을 명시
      }
  })
  // => 위 코드는 Policy_infos_form 데이터를 JSON으로 변환 후,
  // http://172.24.4.120:5000/high_level 서버에 PUT 요청으로 보내고,
  // 응답이 왔을 때, response 변수에 응답 객체 저장
              
  // 응답이 JSON 형식이라고 가정하고, response 변수에서 JSON 데이터 추출
  const myJson = await response.json();
  
  // 추출한 JSON 데이터를 xml 상태 변수에 저장
  setxml(myJson)
}


// 디버깅용: 각 입력 필드의 값이 변경될 때마다 호출되는 함수
const print =(e) => {
  console.log(e.target.name)
  console.log(e.target.value)
}



const handleChange =(e) => {
  var temp = Policy_infos_form
  console.log(e.target.name)
  // Policy ok
  if(e.target.name==="name"){
    if (e.target.value === ""){
      temp['i2nsf-cfi-policy'].name = null
    }
    else {
      temp['i2nsf-cfi-policy'].name = e.target.value
    }
    setPolicyInfosform(temp)
    setPolicyName(e.target.value)
  }
  else if(e.target.name==="language"){
    setPolicyLanguage(e.target.value)
    if (e.target.value === ""){
      temp['i2nsf-cfi-policy'].language = null
    }
    else {
      temp['i2nsf-cfi-policy'].language = e.target.value
    }
    
    setPolicyInfosform(temp)
  }
  else if(e.target.name==="resolutionStrategy"){
    if (e.target.value === ""){
      temp['i2nsf-cfi-policy']['resolution-strategy'] = null
    }
    else {
      temp['i2nsf-cfi-policy']['resolution-strategy'] = e.target.value
    }
    setPolicyInfosform(temp)
    setResolutionStrategy(e.target.value)
  }

  // Rule ok
  else if(e.target.name==="rulename"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.name = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.name = e.target.value
    }
    
    setPolicyInfosform(temp)
    setRuleName(e.target.value)
  }
  else if(e.target.name==="priority"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.priority = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.priority = e.target.value
    }
    
    setPolicyInfosform(temp)
    setPriorityName(e.target.value)
  }
  else if(e.target.name==="configEvent"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.event['system-event']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.event['system-event']= e.target.value
    }
    setPolicyInfosform(temp)
    
    setSystemEvent(e.target.value)
  }
  else if(e.target.name==="configAlarm"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.event['system-alarm'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.event['system-alarm'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    
    setSystemAlarm(e.target.value)
  }
  // Condition ok
  else if(e.target.name==="firewallsource"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.source = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.source = e.target.value
    }
    setPolicyInfosform(temp)
    setFirewallSource(e.target.value)
  }
  else if(e.target.name==="firewalldestination"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.destination = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.destination = e.target.value
    }
    setPolicyInfosform(temp)
    setFirewallSource(e.target.value)
  }
  else if(e.target.name==="firewallconfigTransportProtocol"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['transport-layer-protocol']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['transport-layer-protocol']= e.target.value
    }
    setPolicyInfosform(temp)
    setFirewallSystemAlarm(e.target.value)
  }
  else if(e.target.name==="start"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['range-port-number']['start'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['range-port-number']['start'] = e.target.value
    }
    setPolicyInfosform(temp)
    setFirewallStartPortNum(e.target.value)
    
  }
  else if(e.target.name==="end"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['range-port-number']['end']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall['range-port-number']['end']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallEndPortNum(e.target.value)
    
  }
  else if(e.target.name==="icmpMessage"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.icmp['message'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.firewall.icmp['message'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallIcmpmessage(e.target.value)
    
  }

 // DDos  ok
  else if(e.target.name==="packet-rate-threshold"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['packet-rate-threshold']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['packet-rate-threshold']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallIcmpmessage(e.target.value)
    
  }
  else if(e.target.name==="byte-rate-threshold"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['byte-rate-threshold'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['byte-rate-threshold'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallIcmpmessage(e.target.value)
    
  }
  else if(e.target.name==="flow-rate-threshold"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['flow-rate-threshold'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.ddos['rate-limit']['flow-rate-threshold'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallIcmpmessage(e.target.value)
    
  }

  // Anti virus
  else if(e.target.name==="exception-files"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition['anti-virus'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition['anti-virus'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setFirewallIcmpmessage(e.target.value)
  }

  // Payload
  else if(e.target.name==="content"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.payload.content = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.payload.content = e.target.value
    }
    
    setPolicyInfosform(temp)
    setPayloadContent(e.target.value)
  }
  else if(e.target.name==="url-category"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition['url-category']['url-name']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition['url-category']['url-name']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setUrlName(e.target.value)
  }
  // Voice
  else if(e.target.name==="source-id"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.voice['source-id']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.voice['source-id']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setVoiceSourceId(e.target.value)
  }
  else if(e.target.name==="destination-id"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.voice['destination-id']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.voice['destination-id']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setVoiceDestId(e.target.value)
  }
  else if(e.target.name==="user-agent"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.voice['user-agent'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.voice['user-agent'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setVoiceUserAgent(e.target.value)
  }

  // context time
  else if(e.target.name==="start-date-time"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time['start-date-time']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time['start-date-time']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setContextStartDateTime(e.target.value)
  }
  else if(e.target.name==="end-date-time'"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time['end-date-time']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time['end-date-time']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setContextEndDateTime(e.target.value)
  }

  //Period
  else if(e.target.name==="start-time"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period['start-time']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period['start-time']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setContextEndDateTime(e.target.value)
  }
  else if(e.target.name==="end-time"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period['end-time']= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period['end-time']= e.target.value
    }
    
    setPolicyInfosform(temp)
    setContextEndDateTime(e.target.value)
  }
  // Weekly
  else if(e.target.name==="day"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.day = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.day = e.target.value
    }
    setPolicyInfosform(temp)
    setDay(e.target.value)
  }
  // Monthly
  else if(e.target.name==="Monthlydate"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.date = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.date = e.target.value
    }
    
    setPolicyInfosform(temp)
    setMonthlyDay(e.target.value)
  }
  // Yearly
  else if(e.target.name==="YearlyMonth"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.month= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.period.month= e.target.value
    }
    
    setPolicyInfosform(temp)
    setYearlyMonth(e.target.value)  
  }
  // Frequency
  else if(e.target.name==="frequency"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.frequency= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.time.frequency= e.target.value
    }
    setPolicyInfosform(temp)
    setYearlyMonth(e.target.value)  
  }
  
  // Application 
  else if(e.target.name==="applicationProtocol"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.application.protocol = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.application.protocol = e.target.value
    }
    
    setPolicyInfosform(temp)
    setApplicationProtocal(e.target.value)
  } 
  else if(e.target.name==="deviceType"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['device-type'].device = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['device-type'].device = e.target.value
    }
    
    setPolicyInfosform(temp)
    setDeviceType(e.target.value)
  } 
  // Users
  else if(e.target.name==="oneUserID"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.user.id= null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.user.id= e.target.value
    }
    
    setPolicyInfosform(temp)
    setUserID(e.target.value)
  } 
  else if(e.target.name==="oneUserName"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.user.name = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.user.name = e.target.value
    }
    
    setPolicyInfosform(temp)
    setUserName(e.target.value)
  } 
  // Group
  else if(e.target.name==="groupUserID"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.group.id = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.group.id = e.target.value
    }
    
    setPolicyInfosform(temp)
    setGroupID(e.target.value)
  } 
  else if(e.target.name==="groupUserName"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.group.name = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context.users.group.name = e.target.value
    }
    
    setPolicyInfosform(temp)
    setGroupName(e.target.value)
  } 

  // Geo
  else if(e.target.name==="GeoSourceCountry"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.country = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.country = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoSource(e.target.value)
  } 
  else if(e.target.name==="GeoSourceRegion"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.region = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.region = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoSource(e.target.value)
  } 
  else if(e.target.name==="GeoSourceCity"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.city = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].source.city = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoSource(e.target.value)
  } 
  else if(e.target.name==="GeoDestinationCountry"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.country = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.country = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoDest(e.target.value)
  } 
  else if(e.target.name==="GeoDestinationRegion"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.region = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.region = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoDest(e.target.value)
  } 
  else if(e.target.name==="GeoDestinationCity"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.city = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition.context['geographic-location'].destination.city = e.target.value
    }
    setPolicyInfosform(temp)
    setGeoDest(e.target.value)
  } 

  // Thread-feed
  else if(e.target.name==="threatfeed"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.condition['thread-feed'].name = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.condition['thread-feed'].name = e.target.value
    }
    
    setPolicyInfosform(temp)
    setThreadName(e.target.value)
  } 

  // ACtion
  else if(e.target.name==="primaryAction"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.action["primary-action"]['action'] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.action["primary-action"]['action'] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setPrimaryAction(e.target.value)
    
  } 
  else if(e.target.name==="secondaryAction"){
    if (e.target.value === "") {
      temp['i2nsf-cfi-policy'].rules.action['secondary-action']["log-action"] = null
    }
    else {
      temp['i2nsf-cfi-policy'].rules.action['secondary-action']["log-action"] = e.target.value
    }
    
    setPolicyInfosform(temp)
    setSecondaryAction(e.target.value)
    
  } 
  console.log(Policy_infos_form)
  
}
  const scrollToMiddle = () => {
    const body = document.querySelector('body');
    const viewportHeight = window.innerHeight;
    const middle =  body.scrollHeight / 2 - viewportHeight / 2;
    console.log(middle);

    window.scrollTo({
      top: middle,
      behavior: 'smooth'
    });
  };


  return (
    <div className='configuration'>
      <h1>Configuration</h1>
      <form>
        <fieldset>
        <legend>i2nsf-cfi-policy</legend>
            {/* name */}
            <div className='config'>
              <label htmlFor="name">Name: </label>
              <input required
                id='name'
                name='name'
                type="text"
                onChange={handleChange}
              />
            </div>

            <br></br>

            {/* language */}
            <div className='config'>
              <label htmlFor="language">Language: </label>
              <input id='language'
                name='language'
                type="text"
                onChange={handleChange}
              />
            </div>

            <br></br>

            {/* resolution strategy */}
            <div className='config'>
                <label htmlFor='resolutionStrategy'>Resolution Strategy: </label>
                <select name="resolutionStrategy" id="resolutionStrategy" onChange={handleChange}>
                <option value="">Select</option>
                <option value="fmr">fmr</option>
                <option value="lmr">lmr</option>
                <option value="pmre">pmre</option>
                <option value="pmrn">pmrn</option>
                </select>
            </div>
          

          <br></br>

          {/* rules */} 
          <fieldset>
            <legend>Rule:</legend>
            <div className='configRules'>
              <div className='config'>
                <label htmlFor="rulename">Name: </label>
                <input required id="rulename" name="rulename" type="text" onChange={handleChange}/>
              </div>

              <br></br>

              <div className='config'>
                {/* rule priority which later needs regex added */}
                <label htmlFor="rulepriority">Priority: </label>
                <input id="rulepriority" name="priority" type="text" onChange={handleChange}/>
              </div>

              <br></br>

              {/* Events Field */}
              <fieldset>
                <legend >
                  <label className="labelLegend">
                    Event <input className="inputCheckbox" id="eventCheckbox" name="eventCheckbox" type="checkbox" onChange={handleEventCheck} checked={eventChecked} />
                  </label>
                </legend>
                <div className={eventChecked ? "isShown" : "isHidden"}>
                  <div className='config'>
                    <label htmlFor='configEvent'>System Event: </label>
                    <select name="configEvent" id="configEvent" onChange={handleChange}>
                      <option value="">Select</option>
                      <option value="access-violation">access-violation</option>
                      <option value="configuration-change">configuration-change</option>
                    </select>
                  </div>

                  <br></br>

                  <div className='config'>
                    <label htmlFor='configAlarm'>System Alarm: </label>
                    <select name="configAlarm" id="configAlarm" onChange={handleChange}>
                      <option value="">Select</option>
                      <option value="memory-alarm">memory-alarm</option>
                      <option value="cpu-alarm">cpu-alarm</option>
                      <option value="disk-alarm">disk-alarm</option>
                      <option value="hardware-alarm">hardware-alarm</option>
                      <option value="interface-alarm">interface-alarm</option>
                    </select>
                  </div>
                </div>
              </fieldset>

              <br></br>
              
              <fieldset>
                <legend>
                  <label className="labelLegend">
                    Condition <input className="conditionCheckbox" id="conditionCheckbox" name="conditionCheckbox" type="checkbox" onChange={handleConditionCheck} checked={conditionChecked} />
                  </label>
                </legend>
                <div className={conditionChecked ? "isShown" : "isHidden"}>              
                  <fieldset>
                    <legend>Firewall:</legend>
                    <div className='configFirewall'>
                      <div className='config'>
                        <label htmlFor="source">Source: </label>
                        <input id='source' name='firewallsource' type='union' onChange={handleChange}/>
                      </div>

                      <br></br>

                      <div className='config'>
                        <label htmlFor="destination">Destination: </label>
                        <input id='destination' name='firewalldestination' type='union' onChange={handleChange}/>
                      </div>

                      <br></br>

                      <div className='config'>
                        <label htmlFor='configTransportProtocol'>Transport Protocol: </label>
                        <select name="firewallconfigTransportProtocol" onChange={handleChange}>
                          <option value="">Select</option>
                          <option value="tcp">tcp</option>
                          <option value="udp">udp</option>
                          <option value="sctp">sctp</option>
                          <option value="dccp">dccp</option>
                        </select>
                      </div>
                    </div>

                    <br></br>

                    <div className='portNumber'>               
                      <div className='config'>
                        <label htmlFor="start">Start-port-number: </label>
                        <input id="start" name='start' type='text' onChange={handleChange}/>
                      </div>
                        <br></br>
                      <div className='config'>
                        <label htmlFor="end">End-port-number: </label>
                        <input id="end" name='end' type='text' onChange={handleChange}/>
                      </div>
                    </div>

                  <br></br>

                  {/* icmp message */}

                    <div className='config'>
                      <label htmlFor='icmpMessage'>Icmp Message: </label>

                      <select name="icmpMessage" id="icmpMessage" onChange={handleChange}>
                        <option value="">Select</option>
                        <option value="echo-reply">echo-reply</option>
                        <option value="destination-unreachable">destination-unreachable</option>
                        <option value="redirect">redirect</option>
                        <option value="echo">echo</option>
                        <option value="router-advertisement">router-advertisement</option>
                        <option value="router-solicitation">router-solicitation</option>
                        <option value="time-exceeded">time-exceeded</option>
                        <option value="parameter-problem">parameter-problem</option>
                        <option value="experimental-mobility-protocols">experimental-mobility-protocols</option>
                        <option value="extended-echo-request">extended-echo-request</option>
                        <option value="extended-echo-reply">extended-echo-reply</option>
                      </select>

                    </div>
                  </fieldset>
              
                  <br></br>

                  {/* ddos section */}
                  <fieldset>
                    <legend>Anti-DDoS:</legend>
                    <div className='ddos'>
                      <div className='config'>
                        <label htmlFor="packet-rate-threshold">Packet-rate-threshold: </label>
                        <input id='packet-rate-threshold' name='packet-rate-threshold' type='text' onChange={handleChange}/>
                      </div>
                      
                      <br></br>

                      <div className='config'>
                        <label htmlFor="byte-rate-threshold">Byte-rate-threshold: </label>
                        <input id='byte-rate-threshold' name='byte-rate-threshold' type='text' onChange={handleChange}/>
                      </div>
                      

                      <br></br>
                      <div className='config'>
                        <label htmlFor="flow-rate-threshold">Flow-rate-threshold: </label>
                        <input id='flow-rate-threshold' name='flow-rate-threshold' type='text' onChange={handleChange}/>   
                      </div>
                    </div>
                  </fieldset>

                  <br></br>

                  {/* This is the antivirus section  */}
                  <fieldset>
                    <legend>Anti-Virus:</legend>
                    <div className='antivirus'>
                      <div className='config'>
                        <label htmlFor="exception-files">Exception-files: </label>
                        <input id='exception-files' name='exception-files' type='text' onChange={handleChange}/>
                      </div>
                    </div>
                  </fieldset>
                

                  <br></br>

                  {/* This is the payload section */}
                  <fieldset>
                    <legend>Payload:</legend>
                    <div className='payload'>
                      <div className='config'>
                        <label htmlFor="content">Content: </label>
                        <input id='content' name='content' type='text' onChange={handleChange} />
                      </div>
                    </div>
                  </fieldset>


                  <br></br>

                  <fieldset>
                    <legend>URL:</legend>
                    {/* This is the URl category section */}
                    <div className='url-category'>
                      <div className='config'>
                        <label htmlhtmlFor="url-category">Url-name: </label>
                        <input id='url-category' name='url-category' type='text' onChange={handleChange}/>
                      </div>
                    </div>
                  </fieldset>
                

                  <br></br>

                  {/* Voice section */}
                  <fieldset>
                    <legend>Voice:</legend>
                    <div className='voice'>
                      <div className='config'>
                        <label htmlFor="source-id">Source-id: </label>
                        <input id='source-id' name='source-id' type='text' onChange={handleChange}/>
                      </div>

                      <br></br>
                      <div className='config'>
                        <label htmlFor="destination-id">Destination-id: </label>
                        <input id='destination-id' name='destination-id' type='text' onChange={handleChange} />
                      </div>

                      <br></br>
                      <div className='config'>
                        <label htmlFor="user-agent">User-agent: </label>
                        <input id='user-agent' name='user-agent' type='text' onChange={handleChange}/>
                      </div>
                    </div>
                  </fieldset>

                        
                  <br></br>

                  {/* Context */}
                  <fieldset>
                    <legend>Context:</legend>
                    <fieldset>
                      <legend>Time:</legend>
                      <div className='context'>
                        <div className='config'>
                          <label htmlFor="start-date-time">Start-date-time: </label>
                          <input id='start-date-time' name='start-date-time' type='text' onChange={handleChange} />
                        </div>
                      </div>

                      <br></br>
            
                      <div className='config'>
                        <label htmlFor="end-date-time">End-date-time: </label>
                        <input id='end-date-time' name='end-date-time' type='text' onChange={handleChange} />
                      </div>

                      <br></br>

                      <label>Frequency: </label>
                      <br></br>
                      <div className='configRadio'>
                        <label htmlFor="once">Only Once</label>
                        <input name='frequency' id="once" type="radio" value="only-once" className='frequencyRadio' defaultChecked  onChange={handleChange} onClick={() => {setFrequencyOnlyOnce(true); setFrequencyWeekly(false) ;setFrequencyMonthly(false); setFrequencysYearly(false);}}/>
                      </div>
                      <div className='configRadio'>
                        <label htmlFor="weekly">Weekly</label>                   
                        <input name='frequency' id="weekly" type="radio" value="weekly" className='frequencyRadio' onChange={handleChange} onClick={() => {setFrequencyOnlyOnce(false); setFrequencyWeekly(true) ;setFrequencyMonthly(false); setFrequencysYearly(false);}}/>
                      </div>
                      <div className='configRadio'>  
                        <label htmlFor="monthly">Monthly</label>                 
                        <input name='frequency' id="monthly" type="radio" value="monthly" className='frequencyRadio' onChange={handleChange} onClick={() => {setFrequencyOnlyOnce(false); setFrequencyWeekly(false) ;setFrequencyMonthly(true); setFrequencysYearly(false);}}/> 
                      </div>
                      <div className='configRadio'>                    
                        <label htmlFor="yearly">Yearly</label>                   
                        <input name='frequency' id="yearly" type="radio" value="yearly" className='frequencyRadio' onChange={handleChange} onClick={() => {setFrequencyOnlyOnce(false); setFrequencyWeekly(false) ;setFrequencyMonthly(false); setFrequencysYearly(true);}}  />
                      </div>

                      <br></br>

                      <fieldset>
                        <legend>Period:</legend>
                        <div className='config'>                  
                          <div className={frequencyOnlyOnce ? "isShown" : "isHidden"}>
                            <div className='config'>  
                            <label htmlFor='start-time'>Start-time: </label>
                            <input id='start-time' name='start-time' type='time' onChange={handleChange}/>
                            </div>
                            <br></br>
                            <div className='config'>  
                            <label htmlFor='end-time'>End-time: </label>
                            <input id='end-time' name='end-time' type='time' onChange={handleChange}/>
                            </div>
                          </div>

                          <div className={frequencyWeekly ? "isShown" : "isHidden"}>
                            <label htmlFor='day'>Day: </label>
                            <input id='day' name='day' type='day' onChange={handleChange}/>
                          </div>

                          <div className={frequencyMonthly ? "isShown" : "isHidden"}>
                            <label htmlFor='date'>Date: </label>
                            <input id='date' name='Monthlydate' type='date' onChange={handleChange}/>
                          </div>

                          <div className={frequencyYearly ? "isShown" : "isHidden"}>
                            <label htmlFor='month'>Month: </label>
                            <input id='month' name='YearlyMonth' type='month' onChange={handleChange}/>
                          </div>
                        </div>
                      </fieldset>
                    </fieldset>

                    <br></br>

                    <fieldset>
                      <legend>Application:</legend>
                      <div className='config'>
                        <label htmlFor='applicationProtocol'>Application Protocol: </label>
                        <select id="applicationProtocol" name='applicationProtocol' onChange={handleChange} >
                            <option value="">Select</option>
                            <option value="http">http</option>
                            <option value="https">https</option>
                            <option value="http2">http2</option>
                            <option value="https2">https2</option>
                            <option value="ftp">ftp</option>
                            <option value="ssh">ssh</option>
                            <option value="telnet">telnet</option>
                            <option value="smtp">smtp</option>
                            <option value="pop3">pop3</option>
                            <option value="pop3s">pop3s</option>
                            <option value="imap">imap</option>
                            <option value="imaps">imaps</option>
                        </select>
                      </div>
                    </fieldset>
                    
                    <br></br>

                    <fieldset>
                      <legend>Device-type:</legend>
                      <div className='config'>
                        <label htmlFor='deviceType'>Device Type: </label>
                        <select id='deviceType' name='deviceType' onChange={handleChange}>
                            <option value=''>Select</option>
                            <option value='computer'>computer</option>
                            <option value='mobile-phone'>mobile-phone</option>
                            <option value='voip-vocn-phone'>voip-vocn-phone</option>
                            <option value='tablet'>tablet</option>
                            <option value='network-infrastructure-device'>network-infrastructure-device</option>
                            <option value='iot-device'>iot-device</option>
                            <option value='ot'>ot</option>
                            <option value='vehicle'>vehicle</option>
                        </select>
                      </div>
                    </fieldset>

                    <br></br>
                    <fieldset>
                      <legend>Users:</legend>
                      <div className='config'>
                        <label htmlFor="oneUser" className='userLabel'>User</label> 
                        <input name='users' id="oneUser" type="radio" value="user" className='userRadio'  onClick={() => {setOneUser(true); setGroupUser(false)}}/>
                      </div>
                      
                      <div className='config'>
                        <label htmlFor="groupUser" className='userLabel'>Group</label> 
                        <input name='users' id="groupUser" type="radio" value="group" className='userRadio' onClick={() =>{setOneUser(false); setGroupUser(true)}} />
                      </div>
                    
                      <br></br>

                      {/* hidden section that appear after one of the radio buttons has been clicked */}

                      {/* One user only */}
                      <div className={oneUser ? "isShown" : "isHidden"}>
                        
                        <label htmlFor='oneUser'>ID: </label>
                        <input id='oneUser' name='oneUserID' onChange={handleChange} />

                        <br></br>
                        <br></br>

                        <label>Name: </label>
                        <input id='oneUser' name='oneUserName' onChange={handleChange}/>

                      </div>

                      {/* Group user */}
                      <div className={groupUser ? "isShown" : "isHidden"}>
                        
                        <label htmlFor='groupUser'>ID: </label>
                        <input id='groupUser' name='groupUserID' onChange={handleChange}/>

                        <br></br>
                        <br></br>

                        <label>Name: </label>
                        <input id='groupUser' name='groupUserName' onChange={handleChange}/>

                      </div>   
                    </fieldset>
                    <br></br>

                    <fieldset>
                      {/* geographic location */}
                      <legend>Geographic-location:</legend>
                      <fieldset>
                        <legend>Source:</legend>
                        <div className='config'>
                          <label htmlFor='country'>Country: </label>
                          <input id='country' name='GeoSourceCountry' onChange={handleChange} />

                          <br></br>
                          <br></br>

                          <label htmlFor='region'>Region: </label>
                          <input id='region' name='GeoSourceRegion' onChange={handleChange} />

                          <br></br>
                          <br></br>

                          <label htmlFor='city'>City: </label>
                          <input id='city' name='GeoSourceCity' onChange={handleChange} />
                        </div>
                      </fieldset>

                      
                      <br></br>
                      
                      <fieldset>
                        <legend>Destination:</legend>
                        <div className='config'>
                          <label htmlFor='country'>Country: </label>
                          <input id='country' name='GeoDestinationCountry' onChange={handleChange} />

                          <br></br>
                          <br></br>

                          <label htmlFor='region'>Region: </label>
                          <input id='region' name='GeoDestinationRegion' onChange={handleChange} />

                          <br></br>
                          <br></br>

                          <label htmlFor='city'>City: </label>
                          <input id='city' name='GeoDestinationCity' onChange={handleChange} />
                        </div>
                      </fieldset>

                    </fieldset>

                  </fieldset>
                

                  <br></br>

                  <fieldset>
                    <legend>Thread-feed:</legend>
                    <div className='config'>
                      <label htmlFor='threatfeed'>Name: </label>
                      <input id='threatfeed' name='threatfeed' onChange={handleChange}/>
                    </div>              
                  </fieldset>
                </div>
              </fieldset>
            </div>

            <br></br>
            <fieldset>
              <legend>                  
                <label className="labelLegend">
                  Action <input className="actionCheckbox" id="actionCheckbox" name="actionCheckbox" type="checkbox" onChange={handleActionCheck} checked={actionChecked} />
                </label>
              </legend>
              <div className={actionChecked ? "isShown" : "isHidden"}>   
                <div className='configAction'>
                  <div className='config'>
                    <label htmlFor='primaryAction'>Primary Action</label>
                    <select id='primaryAction' name='primaryAction'onChange={handleChange}>

                      <option value = ''>Select</option>
                      <option value='pass'>pass</option>
                      <option value='drop'>drop</option>
                      <option value='reject'>reject</option>
                      <option value='rate-limit'>rate-imit</option>
                      
                    </select>
                  </div>

                  <br></br>
                  <div className='config'>
                    <label htmlFor='secondaryAction'>Secondary Action</label>

                    <select id='secondaryAction' name='secondaryAction' onChange={handleChange}>

                      <option value = ''>Select</option>
                      <option value='rule log'>rule log</option>
                      <option value='session log'>session log</option>                

                    </select>
                  </div>
                </div>
              </div>
            </fieldset>
          </fieldset>
        </fieldset>

      </form>

        <button className='openModalBtn' onClick={(e) => {setOpenModal(true);ClickSubmit(e);scrollToMiddle()}}>Submit</button>
        {openModal && <Resultmodal closeModal={setOpenModal} data={xml} mode={mode}/>} 
    </div>  
  )
}
