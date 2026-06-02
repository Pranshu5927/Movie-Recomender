import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/auth'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
}

export const moviesAPI = {
  getAll: () => api.get('/movies'),
  search: (q) => api.get(`/movies/search?query=${encodeURIComponent(q)}`),
}

export const recommendationsAPI = {
  getHomepage: () => api.get('/recommendations'),
  getContentBased: (title) =>
    api.get(`/recommendations/content?movie_title=${encodeURIComponent(title)}`),
}

export const ratingsAPI = {
  rate: (movieId, rating) => api.post('/rate', { movie_id: movieId, rating }),
}

export const watchlistAPI = {
  get: () => api.get('/watchlist'),
  add: (movieId) => api.post('/watchlist/add', { movie_id: movieId }),
  remove: (movieId) => api.delete(`/watchlist/${movieId}`),
}

export const usersAPI = {
  getMe: () => api.get('/me'),
}
