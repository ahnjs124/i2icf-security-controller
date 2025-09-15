import React from 'react'
import { useState } from 'react';

// 모달 컴포넌트 불러오기, 각 모달은 함수로 되어 있음
import Usermodal from '../modals_components/usermodal';
import Devicemodal from '../modals_components/devicemodal';
import Locationmodal from '../modals_components/locationmodal';
import Urlmodal from '../modals_components/urlmodal';
import './registration.css'


// Registration 컴포넌트 정의 및 내보내기
export default function Registration(props) {

  // variables for user group modal
  const [openModal, setOpenModal] = useState(false); // UserGroup 창 열림/닫힘 관리 상태 변수
  
  // variables for device group modal
  const [openDeviceModal, setOpenDeviceModal] = useState(false); // DeviceGroup 창 열림/닫힘 관리 상태 변수

  // variables for the location group modal
  const [openLocationModal, setOpenLocationModal] = useState(false); // LocationGroup 창 열림/닫힘 관리 상태 변수

  // variables for the URL group modal
  const [openUrlModal, setOpenUrlModal] = useState(false); // UrlGroup 창 열림/닫힘 관리 상태 변수


  // return이 있는 부분이 실제로 화면에서 보이는 부분
  return (
    // css 클래스 registration 적용
    <div className='registration'>
        {/* 버튼 클릭 시 각 group 모달 창 열림 상태를 true로 변경하여 창 내용 표시 */}
        
        {/* User Groups 버튼과 모달 창 */}
        <button className={props.mode === 'dark' ? 'dark-button' : 'light-button'} style={{marginTop:"100px"}} onClick={() => {setOpenModal(true);}}>User Groups</button>
        {/* 버튼 클릭시 openModal이 true가 되어 Usermodal 컴포넌트 렌더링(보여줌) */}
        {openModal && <Usermodal closeModal={setOpenModal} mode={props.mode}/>}
        
        {/* Device Groups 버튼과 모달 창 */}
        <button className={props.mode === 'dark' ? 'dark-button' : 'light-button'} onClick={() => {setOpenDeviceModal(true);}}>Device Groups</button>
        {/* 버튼 클릭시 openDeviceModal이 true가 되어 Devicemodal 컴포넌트 렌더링(보여줌) */}
        {openDeviceModal && <Devicemodal closeDeviceModal={setOpenDeviceModal} mode={props.mode}/>}

        {/* Location Groups 버튼과 모달 창 */}
        <button className={props.mode === 'dark' ? 'dark-button' : 'light-button'}  onClick={() => {setOpenLocationModal(true);}}>Location Groups</button>
        {/* 버튼 클릭시 openLocationModal이 true가 되어 Locationmodal 컴포넌트 렌더링(보여줌) */}
        {openLocationModal && <Locationmodal closeLocationModal={setOpenLocationModal} mode={props.mode}/>}

        {/* URL Groups 버튼과 모달 창 */}
        <button className={props.mode === 'dark' ? 'dark-button' : 'light-button'} onClick={() => {setOpenUrlModal(true);}}>URL Groups</button>
        {/* 버튼 클릭시 openUrlModal이 true가 되어 Urlmodal 컴포넌트 렌더링(보여줌) */}
        {openUrlModal && <Urlmodal closeUrlModal={setOpenUrlModal} mode={props.mode}/>}
    </div>
  )
}
