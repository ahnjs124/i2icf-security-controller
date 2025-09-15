// React 프로젝트의 진입점 파일 (index.js)
// 이 파일에서 React 컴포넌트를 HTML에 렌더링함
// React와 ReactDOM은 필수, App은 메인 컴포넌트
// CSS 파일도 불러와서 스타일 적용

// React 라이브러리 불러오기 (UI를 컴포넌트 단위로 만들 때 필요)
import React from 'react';
// ReactDOM 라이브러리 불러오기 (React 컴포넌트를 실제 브라우저 화면에 렌더링할 때 필요)
import ReactDOM from 'react-dom';
// App 컴포넌트 불러오기 (프로젝트의 메인 컴포넌트)
import App from './App';
// CSS 파일 불러오기 (navbar 스타일 적용)
import './components/navbar.css'

// ReactDOM.render() : 실제 HTML의 root div에 React 컴포넌트를 렌더링
ReactDOM.render(
  // StrictMode: 잠재적인 문제를 감지하기 위한 개발 모드 도구
  <React.StrictMode>
    {/* App 컴포넌트를 렌더링 */}
    <App />
  </React.StrictMode>,
  // HTML의 id가 'root'인 요소에 렌더링
  document.getElementById('root')
);