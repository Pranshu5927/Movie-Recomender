import streamlit as st
import time
import os
from dotenv import load_dotenv
from api import (
    signup,
    login,
    search_movies,
    get_recommendations,
    add_to_watchlist,
    rate_movie,
    get_watchlist,
    get_all_movies,
    get_popular_movies_with_posters,
    TMDB_API_KEY
)

# ============================================================
# PAGE CONFIG & STYLING
# ============================================================
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
custom_css = """
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
    }
    
    .movie-card {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid #e94560;
        border-left: 4px solid #e94560;
        box-shadow: 0 8px 32px rgba(233, 69, 96, 0.1);
        transition: all 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(233, 69, 96, 0.2);
        border-color: #ff6b6b;
    }
    
    .rating-badge {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin-right: 12px;
    }
    
    .genre-tag {
        background: rgba(233, 69, 96, 0.2);
        color: #ff6b6b;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(233, 69, 96, 0.4);
    }
    
    .auth-container {
        background: rgba(15, 52, 96, 0.6);
        border-radius: 12px;
        padding: 32px;
        border: 1px solid rgba(233, 69, 96, 0.2);
        max-width: 500px;
        margin: 32px auto;
    }
    
    .header-title {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 12px;
    }
    
    .stat-badge {
        background: rgba(233, 69, 96, 0.1);
        border: 1px solid rgba(233, 69, 96, 0.3);
        padding: 8px 16px;
        border-radius: 6px;
        display: inline-block;
        margin-right: 12px;
        color: #e0e0e0;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "home" if not st.session_state.token else "recommendations"
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "popular_movies_loaded" not in st.session_state:
    st.session_state.popular_movies_loaded = False

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def render_movie_card(movie, show_rating=True, show_watchlist=True):
    """Render a beautiful movie card"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(
            f"<div class='movie-card'>"
            f"<h3 style='color: #ff6b6b; margin-bottom: 12px;'>{movie['title']}</h3>",
            unsafe_allow_html=True
        )
        
        # Genres
        genres = movie.get('genres', '').split('|') if isinstance(movie.get('genres'), str) else []
        genre_html = "".join([f"<span class='genre-tag'>{g.strip()}</span>" for g in genres[:3]])
        st.markdown(f"<div>{genre_html}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Rating
        avg_rating = movie.get('avg_rating', 0)
        rating_count = movie.get('rating_count', 0)
        st.markdown(
            f"<div class='stat-badge'>⭐ {avg_rating}/5</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='stat-badge'>👥 {rating_count}</div>", unsafe_allow_html=True)
    
    with col3:
        if show_watchlist and st.session_state.token:
            if st.button("📌 Add", key=f"watchlist_{movie['movie_id']}"):
                add_to_watchlist(st.session_state.token, movie["movie_id"])
                st.toast("✅ Added to watchlist!", icon="📌")
                st.rerun()


def render_movie_card_with_poster(movie, movie_id=None, allow_watchlist=True):
    """Render a movie card with poster image"""
    col_poster, col_info = st.columns([1, 2])
    
    with col_poster:
        poster_url = movie.get('poster_url')
        if poster_url:
            st.image(poster_url, width=150)
        else:
            st.markdown(
                "<div style='background: #16213e; width: 150px; height: 225px; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 1px solid #e94560; color: #999;'>"
                "No Poster<br/>Available"
                "</div>",
                unsafe_allow_html=True
            )
    
    with col_info:
        # Title and rating
        title = movie.get('title', 'Unknown')
        st.markdown(
            f"<h3 style='color: #ff6b6b; margin: 0;'>{title}</h3>",
            unsafe_allow_html=True
        )
        
        # Genres
        genres = movie.get('genres', '')
        if genres:
            genres_list = genres.split('|') if isinstance(genres, str) else []
            genre_html = "".join([f"<span class='genre-tag'>{g.strip()}</span>" for g in genres_list[:3]])
            st.markdown(f"<div style='margin: 10px 0;'>{genre_html}</div>", unsafe_allow_html=True)
        
        # Rating display
        if 'avg_rating' in movie:
            avg_rating = movie.get('avg_rating', 0)
            rating_count = movie.get('rating_count', 0)
            st.markdown(
                f"<div style='margin: 10px 0;'>"
                f"<span class='rating-badge'>⭐ {avg_rating}/5</span>"
                f"<span class='stat-badge'>{rating_count} ratings</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        elif 'rating' in movie:
            rating = movie.get('rating', 0)
            st.markdown(
                f"<div style='margin: 10px 0;'>"
                f"<span class='rating-badge'>⭐ {rating:.1f}/10</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        # Overview
        overview = movie.get('overview', '')
        if overview:
            st.markdown(f"<p style='color: #bbb; font-size: 0.9em; margin: 10px 0;'>{overview[:150]}...</p>", unsafe_allow_html=True)
        
        # Action buttons
        if allow_watchlist and st.session_state.token and movie_id:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📌 Add to Watchlist", key=f"add_poster_{movie_id}"):
                    add_to_watchlist(st.session_state.token, movie_id)
                    st.toast("✅ Added!", icon="📌")
            
            with col2:
                rating = st.select_slider(
                    "Rate",
                    options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                    value=3.0,
                    key=f"rate_poster_{movie_id}"
                )
                if st.button("⭐ Rate", key=f"submit_poster_{movie_id}"):
                    rate_movie(st.session_state.token, movie_id, rating)
                    st.toast(f"✅ Rated {rating}!", icon="⭐")


def render_rating_section(movie):
    """Render movie rating section"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        rating = st.slider(
            "Your Rating",
            min_value=0.5,
            max_value=5.0,
            value=3.0,
            step=0.5,
            key=f"rating_slider_{movie['movie_id']}"
        )
    
    with col2:
        if st.button("Submit ⭐", key=f"submit_rating_{movie['movie_id']}"):
            rate_movie(st.session_state.token, movie["movie_id"], rating)
            st.toast(f"✅ Rated {rating} stars!", icon="⭐")

def logout():
    """Handle logout"""
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.page = "home"
    st.toast("✅ Logged out successfully!", icon="👋")
    st.rerun()

# ============================================================
# HEADER & NAVIGATION
# ============================================================
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown(
        "<h1 style='font-size: 2em; margin: 0;'>🎬</h1>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<h1 class='header-title'>CineMatch</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color: #999; margin: 0; font-size: 0.9em;'>Discover movies tailored to your taste</p>",
        unsafe_allow_html=True
    )

with col3:
    if st.session_state.token:
        col_user, col_logout = st.columns(2)
        with col_user:
            st.markdown(
                f"<div style='text-align: right; padding: 10px 0;'>"
                f"<span style='color: #ff6b6b; font-weight: bold;'>{st.session_state.username}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_logout:
            if st.button("🚪 Logout"):
                logout()

st.divider()

# ============================================================
# MAIN NAVIGATION
# ============================================================
if st.session_state.token:
    # User is logged in - show main navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎬 Recommendations",
        "🔍 Search",
        "📌 Watchlist",
        "⚙️ Settings"
    ])
    
    # ========================================================
    # TAB 1: RECOMMENDATIONS
    # ========================================================
    with tab1:
        st.markdown("### Your Personalized Recommendations")
        st.markdown("<p style='color: #999; margin-bottom: 20px;'>Based on popularity trends</p>", unsafe_allow_html=True)
        
        if st.button("🔄 Refresh Recommendations", key="refresh_rec"):
            st.rerun()
        
        try:
            with st.spinner("Loading your recommendations..."):
                recommendations = get_recommendations(st.session_state.token)
            
            if recommendations:
                st.success(f"✅ Found {len(recommendations)} recommendations for you!")
                st.markdown("")
                
                for idx, movie in enumerate(recommendations):
                    with st.container():
                        st.markdown(f"#### {idx + 1}. {movie['title']}", )
                        render_movie_card_with_poster(movie, movie.get('movie_id'), allow_watchlist=True)
                        st.divider()
            else:
                st.info("📭 No recommendations found. Try rating some movies first!")
        
        except Exception as e:
            st.error(f"❌ Error loading recommendations: {str(e)}")
    
    # ========================================================
    # TAB 2: SEARCH MOVIES
    # ========================================================
    with tab2:
        st.markdown("### Search for Movies")
        
        col_search, col_btn = st.columns([4, 1])
        
        with col_search:
            search_query = st.text_input(
                "Search movies by title",
                placeholder="e.g., Inception, The Dark Knight...",
                label_visibility="collapsed"
            )
        
        with col_btn:
            search_button = st.button("🔍 Search", key="search_btn")
        
        if search_query and search_button:
            try:
                with st.spinner("Searching..."):
                    movies = search_movies(search_query)
                
                if movies:
                    st.success(f"✅ Found {len(movies)} movie(s)")
                    st.markdown("")
                    
                    for idx, movie in enumerate(movies):
                        with st.container():
                            render_movie_card_with_poster(movie, movie.get('movie_id'), allow_watchlist=True)
                            st.divider()
                else:
                    st.warning(f"❌ No movies found for '{search_query}'")
            
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")
        
        else:
            # Show 20 movie preview when no search
            st.markdown("#### 🎬 Browse Popular Movies")
            st.markdown("<p style='color: #999; margin-bottom: 20px;'>Browse from a collection of popular movies</p>", unsafe_allow_html=True)
            
            if st.button("🔄 Load Popular Movies", key="load_popular"):
                st.session_state.popular_movies_loaded = True
            
            if st.session_state.get("popular_movies_loaded", False):
                try:
                    with st.spinner("Loading popular movies..."):
                        popular_movies = get_popular_movies_with_posters(20)
                    
                    if popular_movies:
                        st.success(f"✅ Loaded {len(popular_movies)} popular movies!")
                        st.markdown("")
                        
                        # Display in grid format (3 columns)
                        cols = st.columns(3)
                        
                        for idx, movie in enumerate(popular_movies):
                            with cols[idx % 3]:
                                with st.container():
                                    # Movie poster
                                    poster_url = movie.get('poster_url')
                                    if poster_url:
                                        st.markdown(
                                            f"<div style='text-align: center;'><img src='{poster_url}' width='150' style='border-radius: 8px;'/></div>",
                                            unsafe_allow_html=True
                                        )
                                    else:
                                        st.markdown(
                                            "<div style='display: flex; justify-content: center;'><div style='background: #16213e; width: 150px; height: 225px; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 1px solid #e94560; color: #999;'>No Poster</div></div>",
                                            unsafe_allow_html=True
                                        )
                                    
                                    # Movie title and rating
                                    st.markdown(
                                        f"<p style='color: #ff6b6b; font-weight: bold; margin: 10px 0; text-align: center;'>{movie['title']}</p>",
                                        unsafe_allow_html=True
                                    )
                                    
                                    # Rating
                                    rating = movie.get('rating', 0)
                                    st.markdown(
                                        f"<div style='text-align: center; color: #fff;'>⭐ {rating:.1f}/10</div>",
                                        unsafe_allow_html=True
                                    )
                                    
                                    # Overview (short)
                                    overview = movie.get('overview', '')
                                    if overview:
                                        st.markdown(
                                            f"<p style='color: #bbb; font-size: 0.8em; text-align: center;'>{overview[:80]}...</p>",
                                            unsafe_allow_html=True
                                        )
                    else:
                        st.warning("⚠️ Could not load popular movies")
                        if not TMDB_API_KEY or len(TMDB_API_KEY.strip()) == 0:
                            st.error("❌ TMDB API Key is not configured!")
                            st.markdown("""
                            **To enable movie posters:**
                            1. Get a free API key: https://www.themoviedb.org/settings/api
                            2. Add to `frontend/.env`:
                               ```
                               TMDB_API_KEY=your_key_here
                               ```
                            3. Restart the app
                            """)
                        else:
                            st.info("""
                            **Possible issues:**
                            - Invalid API key
                            - Rate limit exceeded
                            - Network connectivity issue
                            - Check console for detailed error logs
                            """)
                
                except Exception as e:
                    st.error(f"❌ Error loading popular movies")
                    st.info(f"Check the console for error details. Error: {str(e)}")
    
    # ========================================================
    # TAB 3: WATCHLIST
    # ========================================================
    with tab3:
        st.markdown("### Your Watchlist")
        
        if st.button("🔄 Refresh Watchlist", key="refresh_wl"):
            st.rerun()
        
        try:
            with st.spinner("Loading watchlist..."):
                watchlist = get_watchlist(st.session_state.token)
            
            if watchlist:
                st.success(f"✅ You have {len(watchlist)} movie(s) in your watchlist")
                st.markdown("")
                
                for movie in watchlist:
                    with st.container():
                        render_movie_card_with_poster(movie, movie.get('movie_id'), allow_watchlist=False)
                        
                        col_rate, col_remove = st.columns(2)
                        
                        with col_rate:
                            rating = st.select_slider(
                                "Rate this movie",
                                options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                                value=3.0,
                                key=f"wl_rating_{movie['movie_id']}"
                            )
                            if st.button("✅ Rate", key=f"wl_submit_{movie['movie_id']}"):
                                rate_movie(st.session_state.token, movie["movie_id"], rating)
                                st.toast(f"✅ Rated {rating} stars!", icon="⭐")
                        
                        with col_remove:
                            if st.button("🗑️ Remove", key=f"wl_remove_{movie['movie_id']}"):
                                st.info("Remove feature coming soon!")
                        
                        st.divider()
            else:
                st.info("📭 Your watchlist is empty. Start adding movies!")
        
        except Exception as e:
            st.error(f"❌ Error loading watchlist: {str(e)}")
    
    # ========================================================
    # TAB 4: SETTINGS
    # ========================================================
    with tab4:
        st.markdown("### Account Settings")
        
        st.markdown("#### Your Profile")
        st.info(f"📧 Logged in as: **{st.session_state.username}**")
        
        st.markdown("#### Application Settings")
        st.markdown("- 🎨 **Theme**: Dark Mode (Professional)")
        st.markdown("- 🔔 **Notifications**: Enabled")
        st.markdown("- 📊 **Recommendations**: Based on Popularity")
        
        st.markdown("#### API Configuration")
        
        # Check TMDB API Key status
        if TMDB_API_KEY and len(TMDB_API_KEY) > 0:
            st.success(f"✅ **TMDB API Key**: Configured ({len(TMDB_API_KEY)} characters)")
            st.markdown("Movie posters should load from TMDB database")
        else:
            st.warning("⚠️ **TMDB API Key**: Not configured")
            st.markdown("""
            To see movie posters:
            1. Get a free API key from: https://www.themoviedb.org/settings/api
            2. Add it to `frontend/.env`:
               ```
               TMDB_API_KEY=your_key_here
               ```
            3. Restart the app
            """)
        
        st.markdown("---")
        
        if st.button("🚪 Logout from Account", key="logout_settings"):
            logout()
        
        st.divider()
        
        st.markdown("#### About")
        st.markdown("**CineMatch** v1.0")
        st.markdown("A production-ready movie recommendation system")
        st.markdown("Built with ❤️ using FastAPI & Streamlit")

else:
    # User not logged in - show auth pages
    st.markdown("")
    st.markdown("")
    
    # Center content
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("### Welcome to CineMatch")
        st.markdown("<p style='text-align: center; color: #999;'>Sign in to discover your next favorite movie</p>", unsafe_allow_html=True)
        st.markdown("")
        
        auth_choice = st.radio(
            "Choose an option",
            ["Login", "Sign Up"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        if auth_choice == "Login":
            st.markdown("### 🔑 Welcome Back")
            st.markdown("<p style='color: #999; margin-bottom: 20px; text-align: center;'>Login to your account</p>", unsafe_allow_html=True)
            
            email = st.text_input(
                "Email Address",
                placeholder="you@example.com",
                key="login_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="login_password"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                    if email and password:
                        with st.spinner("Logging in..."):
                            try:
                                response = login(email, password)
                                
                                if response.status_code == 200:
                                    data = response.json()
                                    st.session_state.token = data["access_token"]
                                    st.session_state.username = email.split("@")[0]
                                    st.success("✅ Login successful!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid email or password")
                            except Exception as e:
                                st.error(f"❌ Login failed: {str(e)}")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            with col_btn2:
                if st.button("Cancel", use_container_width=True, key="cancel_login"):
                    st.rerun()
        
        else:  # Sign Up
            st.markdown("### 🚀 Join CineMatch")
            st.markdown("<p style='color: #999; margin-bottom: 20px; text-align: center;'>Create a new account</p>", unsafe_allow_html=True)
            
            username = st.text_input(
                "Username",
                placeholder="john_doe",
                key="signup_username"
            )
            
            email = st.text_input(
                "Email Address",
                placeholder="you@example.com",
                key="signup_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="signup_password"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="••••••••",
                key="signup_confirm"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🎬 Sign Up", use_container_width=True, key="signup_btn"):
                    if username and email and password and confirm_password:
                        if password != confirm_password:
                            st.error("❌ Passwords don't match")
                        elif len(password) < 6:
                            st.warning("⚠️ Password must be at least 6 characters")
                        else:
                            with st.spinner("Creating account..."):
                                try:
                                    response = signup(username, email, password)
                                    
                                    if response.status_code == 200:
                                        st.success("✅ Account created! Please login.")
                                        time.sleep(1.5)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Sign up failed: {response.json()}")
                                except Exception as e:
                                    st.error(f"❌ Sign up error: {str(e)}")
                    else:
                        st.warning("⚠️ Please fill in all fields")
            
            with col_btn2:
                if st.button("Cancel", use_container_width=True, key="cancel_signup"):
                    st.rerun()
    
    st.markdown("")
    st.markdown("")
    
    # Footer info
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "<p>🎬 <strong>CineMatch</strong> - Your Personal Movie Recommender</p>"
        "<p style='font-size: 0.9em;'>Discover movies tailored to your taste with our AI-powered recommendation system</p>"
        "</div>",
        unsafe_allow_html=True
    )