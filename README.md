Moody TV

📌 Overview

Moody TV is a movie recommendation web app that suggests movies based on the user's emotions, preferred genre, and reason for watching. Users can also add recommended movies to their watchlist. The project is built using Django (backend) and JavaScript (frontend).

🚀 Features

🎭 Emotion-Based Recommendations – Get movie suggestions based on your current mood.

🎬 Genre Selection – Filter recommendations by your favorite genres.

🎯 Reason for Watching – Fine-tune suggestions based on why you want to watch (e.g., relaxation, inspiration, excitement).

📌 Watchlist Management – Add and remove movies from your personal watchlist.

🎯 Distinctiveness and Complexity

This project meets the distinctiveness and complexity requirements because:

It is not a simple CRUD application; it integrates a recommendation system based on multiple user inputs (emotion, genre, and reason).

The combination of Django, JavaScript, and API-based data handling adds significant depth to both the backend and frontend implementation.

Dynamic UI interactions allow users to add and remove movies from their watchlist without reloading the page.

The system could be extended to integrate external APIs (e.g., IMDb, TMDb) for enhanced recommendations.

🛠 Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite (or PostgreSQL, MySQL)

API: Custom movie recommendation logic

📦 Installation

1️⃣ Clone the Repository

git clone https://github.com/yourusername/moody-tv.git
cd moody-tv

2️⃣ Create a Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Run Database Migrations

python manage.py migrate

4️⃣ Start the Development Server

python manage.py runserver

Access the app at http://127.0.0.1:8000/.

📂 Project Structure

moody-tv/
│-- moodytv/                # Main Django project folder
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│-- movies/                 # App for recommendations & watchlist
│   ├── models.py           # Movie model
│   ├── views.py            # API endpoints
│   ├── urls.py             # App-specific routes
│-- static/                 # Frontend assets (CSS, JS)
│-- templates/              # HTML templates
│-- manage.py               # Django management script
│-- requirements.txt        # Python dependencies
│-- README.md               # Project documentation

🔧 How to Run the Application

Select your emotion, preferred genre, and reason for watching.

Receive movie recommendations based on your inputs.

Click Add to Watchlist to save movies.

Manage your watchlist by removing unwanted movies.

🎯 API Endpoints



📝 Additional Information

This project supports scalability and can be extended with user authentication, external API integrations, and advanced recommendation algorithms.

The recommendation logic can be improved using machine learning models.

The UI follows modern, mobile-friendly design principles.

🔥 Future Improvements

✅ User Authentication (Login, Signup)

✅ More advanced recommendation algorithm

✅ Dark mode UI



📜 License

This project is open-source under the MIT License.

💬 Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

Made with ❤️ by Hein Khant Zaw

