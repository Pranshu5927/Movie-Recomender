import { useState } from 'react'
import Navbar from '../components/Navbar'
import MovieCard from '../components/MovieCard'
import MovieModal from '../components/MovieModal'
import { aiAPI } from '../api/api'
import './AIRecommend.css'

const EXAMPLE_QUERIES = [
  'dark sci-fi movies like Interstellar',
  'funny family movies for the weekend',
  'mind-bending psychological thrillers',
  'action movies like John Wick',
]

export default function AIRecommend() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedMovie, setSelectedMovie] = useState(null)

  const runQuery = async (q) => {
    const trimmed = q.trim()
    if (!trimmed) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await aiAPI.recommend(trimmed)
      setResult(res.data)
    } catch {
      setError('Could not get recommendations. Check that the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    runQuery(query)
  }

  const handleChipClick = (chip) => {
    setQuery(chip)
    runQuery(chip)
  }

  return (
    <div className="ai-page">
      <Navbar />

      <div className="ai-content">

        <div className="ai-header">
          <div className="ai-title-row">
            <span className="ai-badge">AI</span>
            <h1 className="ai-title">AI Picks</h1>
          </div>
          <p className="ai-subtitle">
            Describe what you want to watch in plain English
          </p>
        </div>

        <form className="ai-form" onSubmit={handleSubmit}>
          <div className="ai-input-wrap">
            <svg
              className="ai-input-icon"
              width="18" height="18"
              viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2"
            >
              <path d="M12 2a10 10 0 1 0 10 10" />
              <path d="M12 8v4l3 3" />
              <circle cx="19" cy="5" r="3" fill="currentColor" stroke="none" />
            </svg>
            <input
              type="text"
              className="ai-input"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="e.g. dark sci-fi movies like Interstellar"
              autoComplete="off"
              disabled={loading}
            />
            <button
              type="submit"
              className="ai-submit-btn"
              disabled={loading || !query.trim()}
            >
              {loading ? (
                <span className="ai-btn-spinner" />
              ) : (
                'Find Movies'
              )}
            </button>
          </div>
        </form>

        {!result && !loading && !error && (
          <div className="ai-examples">
            <p className="ai-examples-label">Try asking for</p>
            <div className="ai-chips">
              {EXAMPLE_QUERIES.map(q => (
                <button
                  key={q}
                  className="ai-chip"
                  onClick={() => handleChipClick(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="ai-loading">
            <div className="ai-loading-dots">
              <span /><span /><span />
            </div>
            <p className="ai-loading-label">AI is analysing your request...</p>
          </div>
        )}

        {error && !loading && (
          <div className="ai-error">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
              <circle cx="12" cy="12" r="10" /><path d="M12 8v4m0 4h.01" />
            </svg>
            <p>{error}</p>
          </div>
        )}

        {result && !loading && (
          <div className="ai-results">

            <div className="ai-explanation-card">
              <div className="ai-explanation-header">
                <span className="ai-badge ai-badge--sm">AI</span>
                <span className="ai-explanation-title">Why these films</span>
              </div>
              <p className="ai-explanation-text">{result.explanation}</p>
            </div>

            <p className="ai-results-count">
              {result.movies.length} recommendation{result.movies.length !== 1 ? 's' : ''} for{' '}
              <strong>"{result.query}"</strong>
            </p>

            <div className="ai-grid">
              {result.movies.map(movie => (
                <MovieCard
                  key={movie.movie_id}
                  movie={movie}
                  onClick={setSelectedMovie}
                />
              ))}
            </div>

            <button
              className="ai-retry-btn"
              onClick={() => { setResult(null); setQuery('') }}
            >
              Ask something else
            </button>

          </div>
        )}

      </div>

      {selectedMovie && (
        <MovieModal
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
          onMovieClick={setSelectedMovie}
        />
      )}
    </div>
  )
}
