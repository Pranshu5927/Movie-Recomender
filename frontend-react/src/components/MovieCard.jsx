import { getGenreGradient, getCleanTitle, getYear, getGenres } from '../utils/movieUtils'
import './MovieCard.css'

export default function MovieCard({ movie, onClick }) {
  const cleanTitle = getCleanTitle(movie.title)
  const year = getYear(movie.title)
  const genres = getGenres(movie.genres)
  const gradient = getGenreGradient(movie.genres)

  return (
    <div
      className="movie-card"
      onClick={() => onClick?.(movie)}
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick?.(movie)}
    >
      <div className="card-bg" style={{ background: gradient }} />

      {/* Default view */}
      <div className="card-default">
        {movie.score && (
          <div className="card-score">★ {Number(movie.score).toFixed(1)}</div>
        )}
        <div className="card-info">
          <div className="card-genre-tags">
            {genres.slice(0, 2).map(g => (
              <span key={g} className="card-genre-tag">{g}</span>
            ))}
          </div>
          <h3 className="card-title">{cleanTitle}</h3>
          {year && <p className="card-year">{year}</p>}
        </div>
      </div>

      {/* Hover overlay */}
      <div className="card-hover-overlay">
        <div className="card-play-icon">
          <svg viewBox="0 0 24 24" fill="white" width="28" height="28">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
        <div className="card-hover-text">
          <p className="card-hover-title">{cleanTitle}</p>
          <p className="card-hover-genres">{genres.slice(0, 3).join(' · ')}</p>
        </div>
      </div>
    </div>
  )
}
