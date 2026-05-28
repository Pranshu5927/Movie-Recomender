export const GENRE_GRADIENTS = {
  Action:      'linear-gradient(160deg, #8B0000 0%, #e50914 45%, #1a0000 100%)',
  Adventure:   'linear-gradient(160deg, #92400e 0%, #f59e0b 45%, #1a0800 100%)',
  Animation:   'linear-gradient(160deg, #4c1d95 0%, #8b5cf6 45%, #1a0030 100%)',
  Comedy:      'linear-gradient(160deg, #065f46 0%, #10b981 45%, #001a0e 100%)',
  Crime:       'linear-gradient(160deg, #111827 0%, #374151 60%, #000 100%)',
  Documentary: 'linear-gradient(160deg, #0c4a6e 0%, #0ea5e9 45%, #001520 100%)',
  Drama:       'linear-gradient(160deg, #312e81 0%, #6366f1 45%, #0a0820 100%)',
  Fantasy:     'linear-gradient(160deg, #701a75 0%, #a855f7 45%, #1a0025 100%)',
  Horror:      'linear-gradient(160deg, #000 0%, #1f2937 50%, #450a0a 100%)',
  Musical:     'linear-gradient(160deg, #92400e 0%, #f59e0b 40%, #831843 100%)',
  Mystery:     'linear-gradient(160deg, #1e1b4b 0%, #312e81 60%, #0a0010 100%)',
  Romance:     'linear-gradient(160deg, #9f1239 0%, #ec4899 45%, #1a0010 100%)',
  'Sci-Fi':    'linear-gradient(160deg, #0c4a6e 0%, #6366f1 45%, #000820 100%)',
  Thriller:    'linear-gradient(160deg, #0c0c0c 0%, #292524 60%, #1c1917 100%)',
  Western:     'linear-gradient(160deg, #451a03 0%, #92400e 45%, #1a0800 100%)',
  War:         'linear-gradient(160deg, #1c1917 0%, #44403c 55%, #0a0a0a 100%)',
  'Film-Noir': 'linear-gradient(160deg, #000 0%, #1c1917 60%, #292524 100%)',
}

const DEFAULT_GRADIENT = 'linear-gradient(160deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%)'

export function getGenreGradient(genres) {
  const list = (genres || '').split('|')
  for (const g of list) {
    const key = g.trim()
    if (GENRE_GRADIENTS[key]) return GENRE_GRADIENTS[key]
  }
  return DEFAULT_GRADIENT
}

export function getCleanTitle(title) {
  return title?.replace(/\s*\(\d{4}\)\s*$/, '') || title || 'Unknown'
}

export function getYear(title) {
  const match = title?.match(/\((\d{4})\)/)
  return match ? match[1] : null
}

export function getGenres(genres) {
  return (genres || '').split('|').map(g => g.trim()).filter(Boolean)
}
