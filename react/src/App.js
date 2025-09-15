// Navbar 컴포넌트 불러오기 (페이지 상단 네비게이션 바)
import Navbar from "./components/navbar";

// 각 페이지 컴포넌트 불러오기
// Home, Configuration, Registration, NSFs
// 각 컴포넌트는 src/pages_components 폴더에 위치하며, 해당 페이지의 UI와 기능을 담당
import Home from "./pages_components/home";
import Configuration from "./pages_components/configuration";
import Registration from "./pages_components/registration";
import NSFs from "./pages_components/NSFs";

// App 컴포넌트의 CSS 파일 불러오기 (전체 앱 스타일 적용)
import './App.css'

// React와 useState, useEffect 훅 불러오기 (상태 관리 및 사이드 이펙트 처리)
import React, { useState, useEffect } from 'react';

/*
 🔹 useState
   - React에서 함수형 컴포넌트의 상태(state)를 관리하기 위한 훅(Hook).
   - 호출하면 [현재상태, 상태변경함수] 쌍을 반환.
   - 예: const [mode, setMode] = useState('light');
     → mode: 현재 상태값 ('light')
     → setMode: 상태를 변경하는 함수

 🔹 useEffect
   - 컴포넌트가 렌더링된 이후 실행되는 '사이드 이펙트(side effect)'를 처리하는 훅.
   - 예: 데이터 가져오기(fetch), 구독(subscription), DOM 직접 수정 등
   - 기본 구조: useEffect(() => { 실행할 코드 }, [의존성배열]);
     → [의존성배열] 안의 값이 바뀔 때마다 콜백이 실행됨
     → [] (빈 배열)일 경우, 컴포넌트가 처음 마운트될 때 한 번만 실행됨
     → 의존성을 생략하면, 매 렌더링마다 실행됨
*/


// App 컴포넌트 정의 (메인 컴포넌트)
function App() {
  // mode 상태 변수, setMode 정의
  // 초기값은 로컬 스토리지에서 읽어오거나 'light'로 설정
  // localStorage.getItem(): 로컬 스토리지에서 'mode' 키의 값을 읽어옴
  // useState의 초기값을 함수로 전달하여, 컴포넌트가 처음 렌더링될 때만 로컬 스토리지에서 값을 읽도록 최적화
  const [mode, setMode] = useState(() => {
    // Use local storage to read the current mode, or default to "light"
    return localStorage.getItem('mode') || 'light';
  });

  // toggleMode 함수: mode 상태를 'light'와 'dark' 사이에서 토글
  function toggleMode() {
    setMode(mode === 'light' ? 'dark' : 'light');
  }


  // 현재 URL 주소가 무엇이냐에 따라서 component에 들어갈 내용 결정
  // window.location.pathname: 현재 페이지의 경로를 가져옴
  let component // 렌더링 할 컴포넌트 담을 변수

  // <Home />는 import 해둔 "./pages_components/home" 컴포넌트
  // <Configuration />는 import 해둔 "./pages_components/configuration" 컴포넌트
  // <Registration />는 import 해둔 "./pages_components/registration" 컴포넌트
  // <NSFs />는 import 해둔 "./pages_components/NSFs" 컴포넌트

  switch (window.location.pathname) {
    case '/home':
      component = <Home /> // Home 컴포넌트 렌더링 및 component 변수에 할당
      break;
    case '/registration':
      component = <Registration mode={mode}/>; // mode는 props로 함수로 전달
      break;
    case '/configuration':
      component = <Configuration mode={mode}/>; // mode는 props로 함수로 전달
      break;
    case '/NSFs':
      component = <NSFs mode={mode} />; // mode는 props로 함수로 전달
      break;
  }
  
  // useEffect는 mode의 상태가 변경될 때마다 실행됨
  // mode 상태가 변경될 때마다 mode 상태를 로컬 스토리지에 저장하고, body 태그의 클래스명도 변경
  // localStorage.setItem(): 로컬 스토리지에 현재 mode 값을 저장
  // document.body.className: body 태그의 클래스명을 현재 mode 값으로 설정 (light 또는 dark)
  useEffect(() => {
    localStorage.setItem('mode', mode);
    document.body.className = mode;
  }, [mode]);



  // return이 있는 부분이 실제로 화면에서 보이는 부분
  // JSX 문법으로 UI 정의
  // 최상위 div의 클래스명은 "App"과 현재 mode 값 (light 또는 dark), 이 값들을 기준으로 CSS 스타일 적용
  return (
    <div className={`App ${mode}`}> 
      <Navbar /> {/* Navbar 컴포넌트 렌더링 */}

      {/* mode 상태에 따라 버튼의 클래스명과 텍스트를 동적으로 설정 */}
      <button className={mode === 'dark' ? 'dark-toggle' : 'light-toggle'}  onClick={toggleMode}>{mode === 'dark' ? 'Light-Mode' : 'Dark-Mode'}</button>
      
      {/* 위에서 URL 주소에 따라서 결정된 컴포넌트를 렌더링 */}
      <div className={mode}>{component}</div>
    </div>
  )
}

// App 컴포넌트를 다른 파일에서 사용할 수 있도록 내보내기
export default App;
