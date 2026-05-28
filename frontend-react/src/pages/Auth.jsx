import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Auth.css'

export default function Auth() {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { user, login, signup } = useAuth()
  const navigate = useNavigate()

  if (user) return <Navigate to="/" replace />

  const set = (field) => (e) => setForm(p => ({ ...p, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (mode === 'signup' && !form.username.trim()) {
      return setError('Username is required')
    }
    setLoading(true)
    try {
      if (mode === 'login') {
        await login(form.email, form.password)
      } else {
        await signup(form.username.trim(), form.email, form.password)
      }
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const switchMode = () => {
    setMode(m => m === 'login' ? 'signup' : 'login')
    setError('')
    setForm({ username: '', email: '', password: '' })
  }

  return (
    <div className="auth-page">
      <div className="auth-bg" />

      <header className="auth-header">
        <span className="auth-logo">FILMIX</span>
      </header>

      <main className="auth-main">
        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <h1 className="auth-heading">
            {mode === 'login' ? 'Sign In' : 'Create Account'}
          </h1>

          {mode === 'signup' && (
            <div className="auth-field">
              <input
                id="auth-username"
                type="text"
                value={form.username}
                onChange={set('username')}
                placeholder=" "
                autoComplete="username"
                required
              />
              <label htmlFor="auth-username">Username</label>
            </div>
          )}

          <div className="auth-field">
            <input
              id="auth-email"
              type="email"
              value={form.email}
              onChange={set('email')}
              placeholder=" "
              autoComplete="email"
              required
            />
            <label htmlFor="auth-email">Email</label>
          </div>

          <div className="auth-field">
            <input
              id="auth-password"
              type="password"
              value={form.password}
              onChange={set('password')}
              placeholder=" "
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              required
            />
            <label htmlFor="auth-password">Password</label>
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" className="auth-submit" disabled={loading}>
            {loading
              ? <span className="btn-spinner" />
              : mode === 'login' ? 'Sign In' : 'Create Account'
            }
          </button>

          <p className="auth-switch">
            {mode === 'login' ? 'New to Filmix?' : 'Already have an account?'}
            {' '}
            <button type="button" onClick={switchMode}>
              {mode === 'login' ? 'Sign up now.' : 'Sign in.'}
            </button>
          </p>
        </form>
      </main>
    </div>
  )
}
