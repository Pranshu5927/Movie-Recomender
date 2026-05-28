import { useState, useEffect } from 'react'
import { recommendationsAPI, ratingsAPI, watchlistAPI } from '../api/api'
import MovieCard from './MovieCard'
import { getGenreGradient, getCleanTitle, getYear, getGenres } from '../utils/movieUtils'
import './MovieModal.css'

export default function MovieModal({ movie, onClose, onMovieClick }) {
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [ratingDone, setRatingDone] = useState(false)
  const [inWatchlist, setInWatchlist] = useState(false)
  const [wlLoading, setWlLoading] = useState(false)
  const [similar, setSimilar] = useState([])
  const [similarLoading, setSimilarLoading] = useState(true)
  const [toast, setToast] = useState('')

  const cleanTitle = getCleanTitle(movie.title)
  const year = getYear(movie.title)
  const genres = getGenres(movie.genres)
  const gradient = getGenreGradient(movie.genres)

  useEffect(() => {
    document.body.style.overflow = 'hidden'
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = ''
      document.removeEventListener('keydown', onKey)
    }
  }, [onClose])

  useEffect(() => {
    setRating(0)
    setRatingDone(false)
    setInWatchlist(false)
    setSimilar([])
    setSimilarLoading(true)

    watchlistAPI.get()
      .then(res => setInWatchlist(res.data.some(m => m.movie_id === movie.movie_id)))
      .catch(() => {})

    recommendationsAPI.getContentBased(movie.title)
      .then(res => setSimilar(res.data?.movies?.slice(0, 9) || []))
      .catch(() => {})
      .finally(() => setSimilarLoading(false))
  }, [movie.movie_id])

  const showToast = (msg) => {
    setToast(msg)
    setTimeout(() => setToast(''), 3000)
  }

  const handleRate = async (val) => {
    setRating(val)
    try {
      await ratingsAPI.rate(movie.movie_id, val)
      setRatingDone(true)
      showToast('Rating saved!')
    } catch {
      showToast('Could not save rating')
    }
  }

  const toggleWatchlist = async () => {
    setWlLoading(true)
    try {
      if (inWatchlist) {
        await watchlistAPI.remove(movie.movie_id)
        setInWatchlist(false)
        showToast('Removed from My List')
      } else {
        await watchlistAPI.add(movie.movie_id)
        setInWatchlist(true)
        showToast('Added to My List')
      }
    } catch {
      showToast('Something went wrong')
    } finally {
      setWlLoading(false)
    }
  }

  const handleSimilarClick = (m) => {
    onClose()
    setTimeout(() => onMovieClick?.(m), 120)
  }

  const activeStars = hoverRating || rating

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>

        {toast && <div className="modal-toast">{toast}</div>}

        {/* Hero */}
        <div className="modal-hero" style={{ '--modal-gradient': gradient }}>
          <div className="modal-hero-bg" />
          <div className="modal-hero-left-fade" />
          <button className="modal-close-btn" onClick={onClose} aria-label="Close">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
          <div className="modal-hero-content">
            <h2 className="modal-hero-title">{cleanTitle}</h2>
            {year && <p className="modal-hero-year">{year}</p>}
          </div>
          <div className="modal-hero-bottom-fade" />
        </div>

        {/* Body */}
        <div className="modal-body">
          {/* Meta row */}
          <div className="modal-meta-row">
            <div className="modal-genres">
              {genres.map(g => (
                <span key={g} className="modal-genre-tag">{g}</span>
              ))}
            </div>
            {movie.score && (
              <div className="modal-score">
                <span className="score-star">★</span>
                {Number(movie.score).toFixed(2)}
                {movie.vote_count && (
                  <span className="score-votes"> ({movie.vote_count.toLocaleString()})</span>
                )}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="modal-actions">
            <button
              className={`modal-wl-btn ${inWatchlist ? 'active' : ''}`}
              onClick={toggleWatchlist}
              disabled={wlLoading}
            >
              {inWatchlist ? (
                <>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M20 6 9 17l-5-5" />
                  </svg>
                  In My List
                </>
              ) : (
                <>
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M12 5v14M5 12h14" />
                  </svg>
                  My List
                </>
              )}
            </button>
          </div>

          {/* Rating */}
          <div className="modal-rating-section">
            <p className="modal-rating-label">
              {ratingDone ? 'Your rating' : 'Rate this movie'}
            </p>
            <div className="stars-row">
              {[1, 2, 3, 4, 5].map(s => (
                <button
                  key={s}
                  className={`star-btn ${activeStars >= s ? 'lit' : ''}`}
                  onMouseEnter={() => setHoverRating(s)}
                  onMouseLeave={() => setHoverRating(0)}
                  onClick={() => handleRate(s)}
                  aria-label={`Rate ${s} stars`}
                >
                  ★
                </button>
              ))}
              {ratingDone && <span className="rating-value">{rating} / 5</span>}
            </div>
          </div>

          {/* Similar movies */}
          <div className="modal-similar">
            <h3 className="modal-similar-heading">More Like This</h3>
            {similarLoading ? (
              <div className="similar-loading"><div className="spinner" style={{ width: 28, height: 28, borderWidth: 2 }} /></div>
            ) : similar.length > 0 ? (
              <div className="similar-track">
                {similar.map(m => (
                  <MovieCard key={m.movie_id} movie={m} onClick={handleSimilarClick} />
                ))}
              </div>
            ) : (
              <p className="similar-empty">No similar movies found</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
