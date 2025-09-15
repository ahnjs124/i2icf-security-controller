import React from 'react'
import { useState, useEffect } from 'react';
import './NSFs.css'

// nsfmodal 컴포넌트 불러오기
import Nsfmodal from '../modals_components/nsfmodal';

// numberWithCommas 함수: 숫자에 천 단위 구분 쉼표 추가
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

 // NSFs 컴포넌트 정의 및 내보내기
 // App.js에서 component = <NSFs mode={mode} />; 가 실행될 때 이 컴포넌트가 렌더링됨
export default function NSFs({mode}) {

  // 모달 창 열림 상태, NSF 데이터, NSF 목록 상태 관리
  // onenModal = false: 모달 창이 닫혀 있음
  // posts = []: NSF 목록 초기값은 빈 배열
  // value = []: 선택된 NSF 데이터 초기값은 빈 배열
  const [openModal, setOpenModal] = useState(false);
  const [posts, setPosts] = useState([]);
  const [value, setValue] = useState([]);

  // 컴포넌트가 마운트될 때(즉, <Nsfmodal />가 렌더링될 때) NSF 데이터 가져오기
  // 초기 렌더링 시 한 번만 실행
  useEffect(() => {
    // Flask 백엔드에서 NSF 데이터 가져오기
    fetch('http://172.24.4.120:5000/nsfDB/get')
       // 응답을 JSON으로 파싱
       .then((response) => response.json())
       // 가져온 데이터를 posts 상태에 저장
       .then((data) => {
          setPosts(data["nsf"]);
       })
       // 에러 처리
       .catch((err) => {
          console.log(err.message);
       });
  }, []);

  // posts 상태 확인
  console.log(posts)

  // NSF 목록 테이블 렌더링
  return (
    // NSF 목록을 담는 div, 높이는 화면 전체 높이로 설정
    <div className='NSFs' style={{height:"100vh"}}>
      <h1>Registered NSFs</h1>
      {/* NSF 목록 테이블 */}
      <table className='nsf-table'>
        <tbody>
          <tr>
            <th>Name</th>
            <th>Version</th>
            <th>Access Information</th>
            <th>Specification</th>
          </tr>
          {posts.map((val, key) => {
            const isEvenRow = key % 2 === 0;
            const rowStyle = {
              backgroundColor: isEvenRow
                ? mode === 'dark' ? '#444444' : '#f2f2f2'
                : mode === 'dark' ? '#333333' : '#e6e6e6',
              borderBottom: 'thin solid #000000'
            };
            return (
              <tr key={key} style={rowStyle}>
                <td style={{borderBottom:"thin solid #000000"}} ><label className="nsfname" style={{color: mode === 'dark' ? '#00BFFF' : '#0070FF'}} onClick={(e) => {setOpenModal(true);setValue(val)}}>{val["nsf-name"]}</label></td>
                <td style={{borderBottom:"thin solid #000000"}}>{val["version"]}</td>
                <td style={{borderBottom:"thin solid #000000"}}>
                  <table style={{ margin: "auto",border:0}}>
                    <tbody>
                    <tr style={{textAlign:"right"}}>
                      IP:
                      <td >
                        {val["nsf-access-info"]["ip"]}
                      </td>
                    </tr>
                    <tr style={{textAlign:"right"}}>
                      Protocol: 
                      <td>
                        {val["nsf-access-info"]["management-protocol"]}
                      </td>
                    </tr>
                    <tr style={{textAlign:"right"}}>
                      Port: 
                      <td>
                        {val["nsf-access-info"]["port"]}
                      </td>
                    </tr>
                    </tbody>
                  </table> 
                </td>
                <td style={{borderBottom:"thin solid #000000"}}>
                <table style={{ margin: "auto",border:0}}>
                    <tr style={{textAlign:"right"}}>
                      CPU:
                      <td>
                        {val["nsf-specification"]["cpu"]["model"]}
                      </td>
                    </tr>
                    <tr style={{textAlign:"right"}}>
                      Memory: 
                      <td>
                      8192 MB
                      </td>
                    </tr>
                    <tr style={{textAlign:"right"}}>
                      Bandwidth:
                      <td>
                      {numberWithCommas(val["nsf-specification"]["bandwidth"]["inbound"]/1000000)} MBps
                      </td>
                    </tr>
                  </table> 
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {/* 모달 창이 열려 있을 때 Nsfmodal 컴포넌트 렌더링 */}
      {openModal && <Nsfmodal closeModal={setOpenModal} mode={mode} data={value}/>} 
    </div>
    
  )
}
