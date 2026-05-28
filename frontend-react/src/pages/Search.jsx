import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import MovieCard from '../components/MovieCard'
import MovieModal from '../components/MovieModal'
import { moviesAPI } from '../api/api'
import './Search.css'

export default function Search() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [query, setQuery] = useState(searchParams.get('q') || '')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [selectedMovie, setSelectedMovie] = useState(null)
  const inputRef = useRef(null)
  const debounceRef = useRef(null)

  const doSearch = useCallback(async (q) => {
    if (!q.trim()) { setResults([]); setHasSearched(false); return }
    setLoading(true)
    setHasSearched(true)
    try {
      const res = await moviesAPI.search(q)
      setResults(res.data)
    } catch {
      setResults([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    inputRef.current?.focus()
    const q = searchParams.get('q')
    if (q) { setQuery(q); doSearch(q) }
  }, [])

  const handleChange = (e) => {
    const val = e.target.value
    setQuery(val)
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => doSearch(val), 380)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    clearTimeout(debounceRef.current)
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`, { replace: true })
      doSearch(query)
    }
  }

  const clearSearch = () => {
    setQuery('')
    setResults([])
    setHasSearched(false)
    inputRef.current?.focus()
  }

  return (
    <div className="search-page">
      <Navbar />
      <div className="search-content">

        <form className="search-form" onSubmit={handleSubmit}>
          <div className="search-input-wrap">
            <svg className="search-icon-svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
              <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
            </svg>
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={handleChange}
              placeholder="Search movies, genres..."
              className="search-input"
              autoComplete="off"
            />
            {query && (
              <button
                type="button"
                className="search-clear-btn"
                onClick={clearSearch}
                aria-label="Clear"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M18 6 6 18M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </form>

        {loading && (
          <div className="search-loading"><div className="spinner" /></div>
        )}

        {!loading && !hasSearched && (
          <div className="search-placeholder">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2">
              <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
            </svg>
            <p>Find your next favourite film</p>
          </div>
        )}

        {!loading && hasSearched && results.length === 0 && (
          <div className="search-no-results">
            <p>No results for <strong>"{query}"</strong></p>
            <p>Try a different search term</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <>
            <p className="search-results-count">
              {results.length} result{results.length !== 1 ? 's' : ''} for{' '}
              <strong>"{query}"</strong>
            </p>
            <div className="search-grid">
              {results.map(movie => (
                <MovieCard key={movie.movie_id} movie={movie} onClick={setSelectedMovie} />
              ))}
            </div>
          </>
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
