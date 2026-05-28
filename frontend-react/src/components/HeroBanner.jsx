import { getGenreGradient, getCleanTitle, getYear, getGenres } from '../utils/movieUtils'
import './HeroBanner.css'

export default function HeroBanner({ movie, onMoreInfo }) {
  const cleanTitle = getCleanTitle(movie.title)
  const year = getYear(movie.title)
  const genres = getGenres(movie.genres)
  const gradient = getGenreGradient(movie.genres)

  return (
    <div className="hero" style={{ '--hero-gradient': gradient }}>
      <div className="hero-bg" />
      <div className="hero-left-fade" />

      <div className="hero-content">
        <div className="hero-badges">
          {year && <span className="hero-year-badge">{year}</span>}
          {genres.slice(0, 3).map(g => (
            <span key={g} className="hero-genre-badge">{g}</span>
          ))}
        </div>

        <h1 className="hero-title">{cleanTitle}</h1>

        {movie.score && (
          <p className="hero-meta">
            <span className="hero-star">★</span>
            {Number(movie.score).toFixed(2)}
            {movie.vote_count && (
              <span className="hero-votes"> · {movie.vote_count.toLocaleString()} ratings</span>
            )}
          </p>
        )}

        <div className="hero-actions">
          <button className="hero-btn-play">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z" />
            </svg>
            Play
          </button>
          <button className="hero-btn-info" onClick={onMoreInfo}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 16v-4M12 8h.01" />
            </svg>
            More Info
          </button>
        </div>
      </div>

      <div className="hero-bottom-fade" />
    </div>
  )
}
