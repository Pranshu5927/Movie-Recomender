import requests
import json
from typing import Dict, List, Optional

BASE_URL = "http://127.0.0.1:8000"

# Timeout for all requests (seconds)
REQUEST_TIMEOUT = 10


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
        return response.json()
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
        return response.json()
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
        return response.json()
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
        return response.json()
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