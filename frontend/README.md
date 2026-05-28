# CineMatch - Production-Ready Movie Recommender Frontend

A beautiful, professional Streamlit frontend for the movie recommendation system powered by FastAPI backend.

## 🎨 Features

- **Professional UI Design**: Modern dark theme with gradient styling and smooth animations
- **Secure Authentication**: Signup and login with JWT token management
- **Personalized Recommendations**: Get movies based on popularity trends
- **Movie Search**: Search and discover movies by title
- **Watchlist Management**: Add movies to your personal watchlist
- **Rating System**: Rate movies on a scale of 1-5 stars
- **Responsive Design**: Works seamlessly on desktop and tablet
- **Production-Ready**: Error handling, loading states, and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Backend API running (FastAPI server on `http://127.0.0.1:8000`)

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd Projects/Habitat/Movie-Recommender
   ```

2. **Create a virtual environment** (if not already created)
   ```bash
   python -m venv Recommender_venv
   # On Windows
   Recommender_venv\Scripts\activate
   # On macOS/Linux
   source Recommender_venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Backend is Running**
   ```bash
   cd backend
   python main.py
   # Backend should be running on http://127.0.0.1:8000
   ```

5. **Start the Streamlit App** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📚 How to Use

### 1. **Sign Up**
   - Click "Sign Up" tab
   - Enter username, email, and password
   - Click "🎬 Sign Up" button
   - Account will be created and ready to login

### 2. **Login**
   - Click "Login" tab
   - Enter your email and password
   - Click "🔓 Login" button
   - You'll be logged in and see your personalized recommendations

### 3. **View Recommendations** 🎬
   - **Recommendations** tab shows movies based on popularity
   - Each movie displays:
     - Average rating (⭐)
     - Number of ratings (👥)
     - Genres
   - Actions available:
     - **📌 Add to Watchlist**: Save movies for later
     - **⭐ Rate**: Submit your rating (0.5-5.0 stars)

### 4. **Search Movies** 🔍
   - Use the **Search** tab to find specific movies
   - Type movie title and click "🔍 Search"
   - Results show matching movies
   - Add any movie to your watchlist

### 5. **Manage Watchlist** 📌
   - **Watchlist** tab shows all your saved movies
   - Rate movies directly from watchlist
   - Watch for remove functionality in future updates

### 6. **Settings** ⚙️
   - View your profile information
   - Check application settings
   - Logout from your account

## 🎯 UI/UX Highlights

### Color Scheme
- **Primary**: Deep blue gradient (`#1a1a2e` to `#16213e`)
- **Accent**: Vibrant red (`#e94560`, `#ff6b6b`)
- **Text**: Light gray (`#e0e0e0`)

### Components
- **Movie Cards**: Beautiful cards with hover effects and left accent border
- **Rating Badges**: Prominent display of movie ratings
- **Genre Tags**: Color-coded genre pills
- **Action Buttons**: Clear, intuitive button layout
- **Status Messages**: Toast notifications and inline alerts

### Responsive Layout
- Multi-column layouts that adapt to screen size
- Tab-based navigation for organized sections
- Consistent spacing and padding throughout

## 🔧 Technical Details

### Session State Management
- `token`: JWT authentication token
- `username`: Current logged-in username
- `page`: Current page state
- `search_results`: Cached search results

### API Integration
All API calls are handled through `api.py`:
- `signup()`: Create new account
- `login()`: Authenticate user
- `search_movies()`: Search by title
- `get_recommendations()`: Fetch personalized recommendations
- `add_to_watchlist()`: Add movie to watchlist
- `rate_movie()`: Submit rating
- `get_watchlist()`: Fetch all watchlist items

### Configuration
- **Theme Colors**: Customizable in `.streamlit/config.toml`
- **Custom CSS**: Embedded in `app.py` for styling
- **Backend URL**: Set in `api.py` (default: `http://127.0.0.1:8000`)

## 🛠️ Customization

### Change Backend URL
Edit `frontend/api.py`:
```python
BASE_URL = "http://your-backend-url:8000"
```

### Modify Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#your-color"
backgroundColor = "#your-bg-color"
```

### Add More Features
- Create new pages in `frontend/pages/`
- Extend `api.py` with new API calls
- Add more tabs in the main app navigation

## 🚀 Deployment

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Deploy the app

### Environment Variables
Create `.env` file in `frontend/`:
```
BACKEND_URL=http://your-backend-url:8000
```

## 📝 Notes

- Backend must be running for the app to work
- Database must be populated with movies and ratings
- JWT tokens are stored in session state and expire after login
- All API calls include proper error handling

## 🎬 Future Enhancements

- [ ] User profile management
- [ ] Rating history
- [ ] Movie recommendations by genre
- [ ] Collaborative filtering recommendations
- [ ] Movie details (cast, director, synopsis)
- [ ] Social features (follow users, share lists)
- [ ] Mobile app version

## 📧 Support

For issues or questions, please check the backend API documentation or contact the development team.

---

**Built with ❤️ using Streamlit & FastAPI**

*Version 1.0 - Production Ready*
