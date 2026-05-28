import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Navbar.css'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const menuRef = useRef(null)
  const searchRef = useRef(null)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    setSearchOpen(false)
    setSearchQuery('')
    setMenuOpen(false)
  }, [location.pathname])

  useEffect(() => {
    const handler = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false)
      if (searchRef.current && !searchRef.current.contains(e.target)) setSearchOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
  }

  const handleLogout = () => {
    logout()
    navigate('/auth')
  }

  const initials = user?.username?.slice(0, 2).toUpperCase() || 'U'

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-left">
        <Link to="/" className="navbar-logo">FILMIX</Link>
        <div className="navbar-links">
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
          <Link to="/watchlist" className={location.pathname === '/watchlist' ? 'active' : ''}>My List</Link>
          <Link to="/search" className={location.pathname === '/search' ? 'active' : ''}>Browse</Link>
        </div>
      </div>

      <div className="navbar-right">
        <form
          ref={searchRef}
          className={`navbar-search ${searchOpen ? 'open' : ''}`}
          onSubmit={handleSearch}
        >
          <button
            type="button"
            className="search-icon-btn"
            onClick={() => setSearchOpen(v => !v)}
            aria-label="Search"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
              <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
            </svg>
          </button>
          {searchOpen && (
            <input
              autoFocus
              type="text"
              placeholder="Titles, genres..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          )}
        </form>

        <div ref={menuRef} className="navbar-profile" onClick={() => setMenuOpen(v => !v)}>
          <div className="avatar">{initials}</div>
          <svg
            className={`chevron ${menuOpen ? 'open' : ''}`}
            width="12" height="12"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"
          >
            <path d="m6 9 6 6 6-6" />
          </svg>

          {menuOpen && (
            <div className="profile-menu" onClick={e => e.stopPropagation()}>
              <div className="profile-menu-user">
                <div className="avatar-sm">{initials}</div>
                <div>
                  <p className="menu-username">{user?.username}</p>
                  <p className="menu-email">{user?.email}</p>
                </div>
              </div>
              <div className="menu-divider" />
              <Link to="/watchlist" className="menu-item">My List</Link>
              <div className="menu-divider" />
              <button onClick={handleLogout} className="menu-logout">Sign Out</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
