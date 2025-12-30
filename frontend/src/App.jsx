// frontend/src/App.jsx
import { useState } from 'react'
import MainPage from './pages/MainPage'
import './App.css'

function App() {
  // 사이드바 열림/닫힘 상태 관리
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // 사이드바 토글 함수
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="app-container">
      {/* 1. 상단 Navbar */}
      <nav className="navbar">
        <div className="navbar-left">
          <button className="icon-btn menu-toggle" onClick={toggleSidebar}>
            ☰
          </button>
          <span className="logo-text">KOREA TRIP</span>
        </div>

        <div className="navbar-center">
          <div className="search-wrapper">
            <span className="search-icon">🔍</span>
            <input 
              type="text" 
              className="main-search-input" 
              placeholder="어디로 떠나고 싶으신가요? (AI 여행 코스 추천)" 
            />
          </div>
        </div>

        <div className="navbar-right">
          <button className="icon-btn">🔔</button>
          <div className="profile-avatar">👤</div>
        </div>
      </nav>

      <div className="content-wrapper">
        {/* 2. 세로 사이드바 */}
        <aside className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
          <ul className="sidebar-menu">
            <li className="active">🏠 홈</li>
            <li>📅 AI 일정 만들기</li>
            <li>🥘 현지인 맛집 칼럼</li>
            <li>🔥 실시간 숏폼</li>
            <li>✈️ 항공권 예약</li>
            <div className="divider"></div>
            <li>❤️ 찜한 장소</li>
            <li>⚙️ 설정</li>
            <li>📞 고객센터</li>
          </ul>
        </aside>

        {/* 3. 메인 컨텐츠 영역 */}
        {/* 사이드바가 열리면 오른쪽으로 밀림 (shifted 클래스) */}
        <main className={`main-content ${isSidebarOpen ? 'shifted' : ''}`}>
          <MainPage />
        </main>

        {/* ★ 삭제됨: <div className="overlay"> 코드를 제거해서 흐려짐 효과 없앰 ★ */}
      </div>
    </div>
  )
}

export default App