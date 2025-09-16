import React from 'react';
import Usergroupsform from './user-groups-forms';
import "./modal.css";

import styled from "styled-components";
// styled-components를 사용하여 Title 컴포넌트 스타일 정의
const Title = styled.h1`
  font-size: 1.5em;
  text-align: center;
`;

// Usermodal 컴포넌트 정의
function Usermodal({closeModal,mode}) {
  return (
    <div className='modalBackground'> 
        <div className={mode === 'dark' ? 'dark-modalContainer' : 'light-modalContainer'}> {/* 모드에 따라 다른 스타일 적용 */}
            
            {/* 닫기 버튼, 클릭 시 closeModal 함수 호출하여 모달 닫기 */}
            {/* closeModal은 registration.js에서 상속된 것으로 setOpenModal 함수에 그 값이 전달됨 */}
            {/* 그래서 클릭시 closeModal(false)가 실행되면, registration.js에서 setOpenModal(false)가 실행되고, openModal값이 false로 변경되어, 모달이 닫힘 */}
            <button className='closeModalBtn' onClick={() => {closeModal(false);} }> X </button>
            <Title>User Group Registration</Title>
            <div className='body'>
                {/* user-groups-forms.js의 Usergroupsform 컴포넌트 렌더링, mode 값 전달 */}
                <Usergroupsform mode={mode}/>
            </div>
        </div>
    </div>
  )
}

export default Usermodal