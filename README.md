# Personalized Workout Plan API

## 📌 Project Overview
RESTful API for a Personalized Workout Plan system that allows users to create and manage customized workout plans and track their fitness goals. The system provides a structured way to plan workouts, incorporating predefined exercises with detailed descriptions, and enables progress tracking in real-time.

## 🚀 Features
- **User Authentication/Registration**: Secure access to the API endpoints using JWT
- **Personalized Workout Plan**: Users can create tailored workout plans, specifying workout frequency, goals, exercise types, and daily session duration. they can also select exercises from the predefined list and customize their workout by setting repetitions, sets, duration, or distance.
- **Tracking and goals**: Users can track their weight over time and set personal fitness goals, including weight objectives and exercise-specific achievements.
- **Swagger API Documentation**: Easy testing and interaction with API endpoints - Navigate to: `http://127.0.0.1:8000/swagger/`
- **Workout Mode**: A guided, real-time workout feature showing next exercises, sets, repetitions, and rest periods during a workout session. Users can mark exercises as complete and note any adjustments to the planned workout.
- **Logging**: Logs API requests and errors for debugging. Stored in a 'logs/' directory


## 🛠 Installation & Setup

- **Prerequisites**

- Python 3.10+

- Django

- Django REST Framework

- SQLite (default) 

- Docker (optional, for containerized deployment)

### Clone the Repository:

```bash
git clone <[repository-url](https://github.com/UuTTsU/djangoProject4.git)>
cd <djangoProject4>
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Apply Migrations:
```bash
python manage.py migrate
```

### Create Superuser:
```bash
python manage.py createsuperuser
```

### Run Development Server:
```bash
python manage.py runserver
```

## 🐳 Docker Setup
To run the project using Docker:
1. Build the Docker image:
   ```bash
   docker build -t workout-mode-api .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 workout-mode-api
   ```

## 🤝 Contributor
- **Giorgi Utsunashvili** - Backend Developer



