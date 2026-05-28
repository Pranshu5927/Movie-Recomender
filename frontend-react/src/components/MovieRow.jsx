import { useRef, useState, useEffect } from 'react'
import MovieCard from './MovieCard'
import './MovieRow.css'

export default function MovieRow({ title, movies, onMovieClick }) {
  const trackRef = useRef(null)
  const [showLeft, setShowLeft] = useState(false)
  const [showRight, setShowRight] = useState(false)

  const checkArrows = () => {
    const el = trackRef.current
    if (!el) return
    setShowLeft(el.scrollLeft > 10)
    setShowRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 10)
  }

  useEffect(() => {
    checkArrows()
    const el = trackRef.current
    el?.addEventListener('scroll', checkArrows, { passive: true })
    window.addEventListener('resize', checkArrows, { passive: true })
    return () => {
      el?.removeEventListener('scroll', checkArrows)
      window.removeEventListener('resize', checkArrows)
    }
  }, [movies])

  const scroll = (dir) => {
    trackRef.current?.scrollBy({ left: dir === 'right' ? 680 : -680, behavior: 'smooth' })
  }

  if (!movies?.length) return null

  return (
    <section className="movie-row">
      <h2 className="row-title">{title}</h2>
      <div className="row-container">
        {showLeft && (
          <button className="row-arrow row-arrow-left" onClick={() => scroll('left')} aria-label="Scroll left">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="m15 18-6-6 6-6" />
            </svg>
          </button>
        )}

        <div className="row-track" ref={trackRef}>
          {movies.map(movie => (
            <MovieCard key={movie.movie_id} movie={movie} onClick={onMovieClick} />
          ))}
        </div>

        {showRight && (
          <button className="row-arrow row-arrow-right" onClick={() => scroll('right')} aria-label="Scroll right">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="m9 18 6-6-6-6" />
            </svg>
          </button>
        )}
      </div>
    </section>
  )
}
