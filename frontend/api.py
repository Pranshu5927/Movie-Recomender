import requests
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load environment variables from .env file in the frontend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# TMDB API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Timeout for all requests (seconds)
REQUEST_TIMEOUT = 10

# TMDB session with retry logic to handle Windows ConnectionResetError (10054)
_tmdb_retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
_tmdb_session = requests.Session()
_tmdb_session.mount("https://", HTTPAdapter(max_retries=_tmdb_retry))
_tmdb_session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})


# ============================================================
# ERROR HANDLING
# ============================================================
class APIError(Exception):
    """Custom exception for API errors"""
    pass


def handle_response(response):
    """Handle API response and raise errors if needed"""
    try:
        if response.status_code == 401:
            raise APIError("Unauthorized - Please login again")
        elif response.status_code == 403:
            raise APIError("Forbidden - Access denied")
        elif response.status_code == 404:
            raise APIError("Not found - Resource doesn't exist")
        elif response.status_code >= 500:
            raise APIError("Server error - Please try again later")
        elif response.status_code >= 400:
            data = response.json()
            error_msg = data.get("detail", "An error occurred")
            raise APIError(f"Error: {error_msg}")
        return response
    except requests.exceptions.RequestException as e:
        raise APIError(f"Connection error: {str(e)}")


# ============================================================
# TMDB POSTER FETCHING
# ============================================================
def get_movie_poster_by_title(title: str, year: Optional[int] = None) -> Optional[str]:
    """
    Fetch movie poster from TMDB by title
    
    Args:
        title: Movie title
        year: Optional release year for better matching
    
    Returns:
        Poster URL or None if not found
    """
    if not TMDB_API_KEY or len(TMDB_API_KEY.strip()) == 0:
        return None
    
    try:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "page": 1
        }
        
        if year:
            params["year"] = year
        
        response = _tmdb_session.get(search_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                poster_path = data["results"][0].get("poster_path")
                if poster_path:
                    return f"{TMDB_IMAGE_BASE}{poster_path}"
        elif response.status_code == 401:
            print(f"TMDB API Error: Invalid API key")
            return None
        elif response.status_code == 429:
            print(f"TMDB API Error: Rate limit exceeded")
            return None
        
        return None
    except requests.exceptions.Timeout:
        print(f"TMDB API timeout for '{title}'")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"TMDB Connection error for '{title}': {str(e)}")
        return None
    except Exception as e:
        print(f"TMDB Error fetching poster for '{title}': {str(e)}")
        return None


def get_popular_movies_with_posters(limit: int = 20) -> List[Dict]:
    """
    Get popular movies with poster images from TMDB
    
    Args:
        limit: Number of movies to return
    
    Returns:
        List of popular movies with poster URLs
    """
    if not TMDB_API_KEY or len(TMDB_API_KEY.strip()) == 0:
        print("TMDB_API_KEY is not configured")
        return []
    
    try:
        url = f"{TMDB_BASE_URL}/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "page": 1
        }
        
        # Shorter timeout to fail faster
        response = _tmdb_session.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            movies = []
            
            for movie in data.get("results", [])[:limit]:
                poster_url = None
                if movie.get("poster_path"):
                    poster_url = f"{TMDB_IMAGE_BASE}{movie['poster_path']}"
                
                movies.append({
                    "title": movie.get("title", "Unknown"),
                    "poster_url": poster_url,
                    "genres": ", ".join([str(g) for g in movie.get("genre_ids", [])]),
                    "rating": movie.get("vote_average", 0),
                    "overview": movie.get("overview", "")
                })
            
            return movies
        elif response.status_code == 401:
            print("TMDB API Error: Invalid API key - check your TMDB_API_KEY in .env")
            return []
        elif response.status_code == 429:
            print("TMDB API Error: Rate limit exceeded - too many requests")
            return []
        else:
            print(f"TMDB API Error: HTTP {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("TMDB API timeout - request took too long")
        return []
    except requests.exceptions.ConnectionError as e:
        print(f"TMDB Connection error: {str(e)}")
        print("This could be a network issue or TMDB server issue")
        return []
    except Exception as e:
        print(f"Error fetching popular movies: {str(e)}")
        return []


# ============================================================
# AUTH
# ============================================================
def signup(username: str, email: str, password: str) -> Dict:
    """
    Create a new user account
    
    Args:
        username: User's username
        email: User's email address
        password: User's password
    
    Returns:
        Response object with status and data
    """
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json={
                "username": username,
                "email": email,
                "password": password
            },
            timeout=REQUEST_TIMEOUT
        )
        return handle_response(response)
    except requests.exceptions.Timeout:
        raise APIError("Request timeout - Server took too long to respond")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server - Check if backend is running")


def login(email: str, password: str) -> Dict:
    """
    Authenticate user and get JWT token
    
    Args:
        email: User's email address
        password: User's password
    
    Returns:
        Response object with access_token
    """
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=REQUEST_TIMEOUT
        )
        return handle_response(response)
    except requests.exceptions.Timeout:
        raise APIError("Request timeout - Server took too long to respond")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server - Check if backend is running")


# ============================================================
# MOVIES
# ============================================================
def search_movies(query: str) -> List[Dict]:
    """
    Search for movies by title
    
    Args:
        query: Search query string
    
    Returns:
        List of matching movies
    """
    try:
        response = requests.get(
            f"{BASE_URL}/movies/search",
            params={"query": query},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        movies = response.json()
        
        # Fetch posters for each movie
        for movie in movies:
            movie["poster_url"] = get_movie_poster_by_title(movie.get("title", ""))
        
        return movies
    except requests.exceptions.Timeout:
        raise APIError("Search timeout - Try a simpler query")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


def get_all_movies(limit: int = 50) -> List[Dict]:
    """
    Get list of all movies
    
    Args:
        limit: Maximum number of movies to return
    
    Returns:
        List of all movies
    """
    try:
        response = requests.get(
            f"{BASE_URL}/movies",
            params={"limit": limit},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        movies = response.json()
        
        # Fetch posters for each movie
        for movie in movies:
            movie["poster_url"] = get_movie_poster_by_title(movie.get("title", ""))
        
        return movies
    except requests.exceptions.Timeout:
        raise APIError("Request timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


# ============================================================
# RECOMMENDATIONS
# ============================================================
def get_recommendations(token: str) -> List[Dict]:
    """
    Get personalized movie recommendations
    
    Args:
        token: JWT authentication token
    
    Returns:
        List of recommended movies
    """
    try:
        response = requests.get(
            f"{BASE_URL}/recommendations",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        movies = response.json()
        
        # Fetch posters for each movie
        for movie in movies:
            movie["poster_url"] = get_movie_poster_by_title(movie.get("title", ""))
        
        return movies
    except requests.exceptions.Timeout:
        raise APIError("Recommendations timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


# ============================================================
# WATCHLIST
# ============================================================
def get_watchlist(token: str) -> List[Dict]:
    """
    Get user's watchlist
    
    Args:
        token: JWT authentication token
    
    Returns:
        List of movies in watchlist
    """
    try:
        response = requests.get(
            f"{BASE_URL}/watchlist",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        movies = response.json()
        
        # Fetch posters for each movie
        for movie in movies:
            movie["poster_url"] = get_movie_poster_by_title(movie.get("title", ""))
        
        return movies
    except requests.exceptions.Timeout:
        raise APIError("Watchlist timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


def add_to_watchlist(token: str, movie_id: int) -> Dict:
    """
    Add a movie to watchlist
    
    Args:
        token: JWT authentication token
        movie_id: ID of movie to add
    
    Returns:
        Response with success message
    """
    try:
        response = requests.post(
            f"{BASE_URL}/watchlist/add",
            headers={"Authorization": f"Bearer {token}"},
            json={"movie_id": movie_id},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        return response.json()
    except requests.exceptions.Timeout:
        raise APIError("Add to watchlist timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


def remove_from_watchlist(token: str, movie_id: int) -> Dict:
    """
    Remove a movie from watchlist
    
    Args:
        token: JWT authentication token
        movie_id: ID of movie to remove
    
    Returns:
        Response with success message
    """
    try:
        response = requests.delete(
            f"{BASE_URL}/watchlist/remove/{movie_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        return response.json()
    except requests.exceptions.Timeout:
        raise APIError("Remove from watchlist timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


# ============================================================
# RATINGS
# ============================================================
def rate_movie(token: str, movie_id: int, rating: float) -> Dict:
    """
    Rate a movie
    
    Args:
        token: JWT authentication token
        movie_id: ID of movie to rate
        rating: Rating value (0.5-5.0)
    
    Returns:
        Response with success message
    """
    try:
        # Validate rating
        if not (0.5 <= rating <= 5.0):
            raise APIError("Rating must be between 0.5 and 5.0")
        
        response = requests.post(
            f"{BASE_URL}/rate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "movie_id": movie_id,
                "rating": rating
            },
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        return response.json()
    except requests.exceptions.Timeout:
        raise APIError("Rating timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


# ============================================================
# USER
# ============================================================
def get_current_user(token: str) -> Dict:
    """
    Get current authenticated user info
    
    Args:
        token: JWT authentication token
    
    Returns:
        User information
    """
    try:
        response = requests.get(
            f"{BASE_URL}/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=REQUEST_TIMEOUT
        )
        handle_response(response)
        return response.json()
    except requests.exceptions.Timeout:
        raise APIError("User info timeout")
    except requests.exceptions.ConnectionError:
        raise APIError("Cannot connect to server")


# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def is_backend_running() -> bool:
    """Check if backend API is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_api_status() -> Dict:
    """Get backend API status information"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            return {"status": "online", "message": response.json().get("message", "API is running")}
        return {"status": "offline", "message": "API is not responding"}
    except Exception as e:
        return {"status": "offline", "message": f"Cannot connect: {str(e)}"}


