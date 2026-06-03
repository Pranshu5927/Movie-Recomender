import { useState, useRef, useEffect } from 'react'
import Navbar from '../components/Navbar'
import MovieCard from '../components/MovieCard'
import MovieModal from '../components/MovieModal'
import { chatAPI } from '../api/api'
import './Chat.css'

const STARTERS = [
  'Recommend mind-bending sci-fi movies',
  'Something dark and atmospheric like Blade Runner',
  'Funny movies for a family night',
  'Intense thrillers under 2 hours',
]

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedMovie, setSelectedMovie] = useState(null)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const buildHistory = (msgs) =>
    msgs.map(m => ({ role: m.role, content: m.content }))

  const sendMessage = async (text) => {
    const trimmed = text.trim()
    if (!trimmed || loading) return

    const userMsg = { id: Date.now(), role: 'user', content: trimmed, movies: [] }
    const nextMessages = [...messages, userMsg]

    setMessages(nextMessages)
    setInput('')
    setLoading(true)

    try {
      const res = await chatAPI.send(trimmed, buildHistory(messages))
      const { reply, movies } = res.data

      setMessages(prev => [
        ...prev,
        { id: Date.now() + 1, role: 'assistant', content: reply, movies: movies || [] },
      ])
    } catch {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Something went wrong. Is the backend running?',
          movies: [],
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleStarterClick = (s) => {
    sendMessage(s)
  }

  const isEmpty = messages.length === 0

  return (
    <div className="chat-page">
      <Navbar />

      <div className="chat-body">

        {/* ---- Messages ---- */}
        <div className="chat-messages">

          {isEmpty && !loading && (
            <div className="chat-empty">
              <div className="chat-empty-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <h2 className="chat-empty-title">What are you in the mood for?</h2>
              <p className="chat-empty-sub">
                Ask me anything — I remember the full conversation, so refine as you go.
              </p>
              <div className="chat-starters">
                {STARTERS.map(s => (
                  <button key={s} className="chat-starter" onClick={() => handleStarterClick(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map(msg => (
            <div key={msg.id} className={`chat-msg chat-msg--${msg.role}`}>

              {msg.role === 'assistant' && (
                <div className="chat-avatar">
                  <span className="ai-dot" />
                </div>
              )}

              <div className="chat-msg-body">
                <div className={`chat-bubble chat-bubble--${msg.role}`}>
                  {msg.content}
                </div>

                {msg.role === 'assistant' && msg.movies.length > 0 && (
                  <div className="chat-movie-strip">
                    {msg.movies.slice(0, 6).map(movie => (
                      <MovieCard
                        key={movie.movie_id}
                        movie={movie}
                        onClick={setSelectedMovie}
                      />
                    ))}
                  </div>
                )}
              </div>

            </div>
          ))}

          {loading && (
            <div className="chat-msg chat-msg--assistant">
              <div className="chat-avatar">
                <span className="ai-dot ai-dot--pulse" />
              </div>
              <div className="chat-msg-body">
                <div className="chat-bubble chat-bubble--assistant chat-bubble--thinking">
                  <span className="thinking-dot" />
                  <span className="thinking-dot" />
                  <span className="thinking-dot" />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* ---- Input bar ---- */}
        <div className="chat-input-area">
          <form className="chat-form" onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              type="text"
              className="chat-input"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask for a recommendation..."
              autoComplete="off"
              disabled={loading}
            />
            <button
              type="submit"
              className="chat-send-btn"
              disabled={loading || !input.trim()}
              aria-label="Send"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <path d="M22 2 11 13M22 2 15 22l-4-9-9-4 20-7z" />
              </svg>
            </button>
          </form>
          {!isEmpty && (
            <p className="chat-context-hint">
              AI remembers this conversation — just say "something darker" or "nothing too old" to refine
            </p>
          )}
        </div>

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
