// Navbar 컴포넌트 정의 (페이지 상단 네비게이션 바)
// React와 useState, useEffect 훅 불러오기 (상태 관리 및 사이드 이펙트 처리)
// CSS 파일 불러오기 (Navbar 스타일 적용)
import React, { useState, useEffect } from "react";
import "./navbar.css"


// Navbar 컴포넌트 정의 및 내보내기
export default function Navbar() {
    // 스크롤에 따른 네비게이션 바 그림자 효과를 위한 상태 변수와 이벤트 리스너 설정
    // navShadow 상태 변수, setnavShadow 함수 정의, 초기값은 "0px 0px 5px" (네비게이션 바에 그림자 효과 적용)
    const [navShadow, setnavShadow] = useState("0px 0px 5px");
    
    // listenScrollEvent 함수: 스크롤 위치에 따라 navShadow 상태를 변경    
    const listenScrollEvent = () => {
        window.scrollY > 0 ? setnavShadow("0px 0px 5px") : setnavShadow("0px 0px 5px");
    };

    // useEffect 훅을 사용하여 컴포넌트가 마운트될 때와 언마운트될 때 스크롤 이벤트 리스너를 추가 및 제거
    // useEffect는 두 번째 인자를 기반으로 실행되는데, 두 번째 인자가 빈 배열([])이면 컴포넌트가 처음 마운트될 때 한 번만 실행됨
    useEffect(() => {
      window.addEventListener("scroll", listenScrollEvent);
      return () => {
        window.removeEventListener("scroll", listenScrollEvent);
      };
    }, []);
  

    // JSX 문법으로 네비게이션 바 UI 정의
    // nav 태그에 navShadow 상태를 스타일로 적용하여 스크롤에 따른 그림자 효과 구현
    return (
        <nav className="bg-white"
          style={{
            boxShadow: navShadow,
            transition: "all 1s"
          }}
        >
            <a href="/home" className="site-title" style={{fontFamily:"Audiowide"}}>I2NSF</a> {/* 사이트 제목 및 홈 링크 */}

            <ul style={{fontFamily:"Audiowide"}}className="navbar-items"> {/* 네비게이션 바 항목들 */}
                <li>
                    <a className="navbar-items" href="/registration">Endpoint</a> {/*  네비게이션 바의 Endpoint 링크 */}
                </li>
                <li>
                    <a className="navbar-items" href="/configuration">Configuration</a> {/*  네비게이션 바의 Configuration 링크 */}
                </li>
                <li>
                    <a className="navbar-items" href="/NSFs">NSFs</a> {/*  네비게이션 바의 NSFs 링크 */}
                </li>
            </ul>
        </nav>
    );
}