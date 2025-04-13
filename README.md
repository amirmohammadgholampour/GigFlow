GigFlow is a backend-only project designed to help freelancers and employers quickly find and manage projects.

**This project provides only an API (no frontend).**

🛠 Built With
Language: Python 3.12.3

Framework: Django

Database: MySQL (you can change it to PostgreSQL or SQLite)

**API Technologies:**
API Style: REST API

Framework: Django REST Framework (DRF)

Serialization: ModelSerializer (to convert data to JSON)

Views: APIView (class-based views)

**Installation Guide:**
Install Python (3.12.3)

Clone the repository
git clone <repo-url>

Create a virtual environment
python -m venv venv

Activate the virtual environment

On Windows: venv\Scripts\activate

On Linux/macOS: source venv/bin/activate

Install Django
pip install django

Install Django REST framework
pip install djangorestframework

Install JWT authentication
pip install djangorestframework_simplejwt

Install filtering support
pip install django-filter

(Optional) Create the config project folder
django-admin startproject config