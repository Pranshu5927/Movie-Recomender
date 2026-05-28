import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import MovieCard from '../components/MovieCard'
import MovieModal from '../components/MovieModal'
import { watchlistAPI } from '../api/api'
import './Watchlist.css'

export default function Watchlist() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedMovie, setSelectedMovie] = useState(null)

  const fetchWatchlist = () => {
    setLoading(true)
    watchlistAPI.get()
      .then(res => setMovies(res.data))
      .catch(() => setMovies([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchWatchlist() }, [])

  const handleModalClose = () => {
    setSelectedMovie(null)
    fetchWatchlist()
  }

  return (
    <div className="watchlist-page">
      <Navbar />
      <div className="watchlist-content">
        <div className="watchlist-header">
          <h1 className="watchlist-title">My List</h1>
          {!loading && (
            <p className="watchlist-count">
              {movies.length} {movies.length === 1 ? 'title' : 'titles'}
            </p>
          )}
        </div>

        {loading ? (
          <div className="wl-loading"><div className="spinner" /></div>
        ) : movies.length === 0 ? (
          <div className="wl-empty">
            <div className="wl-empty-icon">
              <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2">
                <path d="M12 5v14M5 12h14" />
              </svg>
            </div>
            <h2>Your list is empty</h2>
            <p>Browse movies and add ones you want to watch</p>
            <Link to="/" className="wl-cta">Browse Movies</Link>
          </div>
        ) : (
          <div className="watchlist-grid">
            {movies.map(movie => (
              <MovieCard key={movie.movie_id} movie={movie} onClick={setSelectedMovie} />
            ))}
          </div>
        )}
      </div>

      {selectedMovie && (
        <MovieModal
          movie={selectedMovie}
          onClose={handleModalClose}
          onMovieClick={setSelectedMovie}
        />
      )}
    </div>
  )
}
