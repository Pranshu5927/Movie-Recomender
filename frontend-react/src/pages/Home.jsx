import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import HeroBanner from '../components/HeroBanner'
import MovieRow from '../components/MovieRow'
import MovieModal from '../components/MovieModal'
import { recommendationsAPI } from '../api/api'
import './Home.css'

export default function Home() {
  const [sections, setSections] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedMovie, setSelectedMovie] = useState(null)

  useEffect(() => {
    recommendationsAPI.getHomepage()
      .then(res => setSections(res.data))
      .catch(() => setError('Could not load recommendations. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  const heroMovie = sections?.must_watch?.movies?.[0] || null

  return (
    <div className="home-page">
      <Navbar />

      {loading && (
        <div className="home-loading">
          <div className="spinner" />
          <p>Loading your recommendations...</p>
        </div>
      )}

      {error && !loading && (
        <div className="home-error">
          <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="12" cy="12" r="10" /><path d="M12 8v4m0 4h.01" />
          </svg>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Try Again</button>
        </div>
      )}

      {!loading && !error && (
        <>
          {heroMovie && (
            <HeroBanner
              movie={heroMovie}
              onMoreInfo={() => setSelectedMovie(heroMovie)}
            />
          )}
          <div className="home-rows">
            {sections && Object.entries(sections).map(([key, section]) =>
              section?.movies?.length > 0 && (
                <MovieRow
                  key={key}
                  title={section.title}
                  movies={section.movies}
                  onMovieClick={setSelectedMovie}
                />
              )
            )}
          </div>
        </>
      )}

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
