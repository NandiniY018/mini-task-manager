# 📋 Mini Task Manager

A clean, responsive, full-stack Task Management web application built with **Django** (Python) and **Vanilla JavaScript / HTML / CSS**, backed by **SQLite**.

Created as part of the **Software Developer Intern Practical Assessment** for **Florix Technologies**.

---

## 🛠️ Technologies Used

- **Backend**: Python 3, Django 5.x (using plain Django Views and `JsonResponse`)
- **Database**: SQLite3 (default Django file-based database)
- **Frontend**: HTML5, Vanilla CSS3 (custom responsive styling, no external frameworks like Bootstrap or Tailwind), Vanilla JavaScript (using modern `fetch()` API and Async/Await)

---

## ✨ Features

- **Automatic Task Loading**: Tasks load automatically on page load via REST API.
- **Task Creation**: Add tasks with title, optional description, priority (Low, Medium, High), and due date.
- **Task Completion**: Instant 1-click "Mark as Done" action updating status in database via PATCH API.
- **Task Deletion**: Delete tasks with confirmation prompt via DELETE API.
- **Live Filtering**: Filter tasks by Status (*All*, *Pending*, *Done*) and Priority (*High*, *Medium*, *Low*) independently or together.
- **Real-Time Pending Counter**: Automatically updates the count of pending tasks upon adding, completing, or deleting tasks.
- **Data Persistence**: All task states are persistently stored in SQLite across page reloads.
- **User-Friendly Error Handling**: Informative inline visual alerts (green for success, red for errors) directly on the UI without relying purely on browser `alert()`.
- **Django Admin Integration**: Fully configured Django Admin panel to manage and inspect tasks.

---

## 📁 Project Structure

```text
task-manager/
│
├── manage.py                  # Django administrative script
├── requirements.txt           # Project dependencies (Django)
├── queries.sql                # Standalone SQL queries for assessment Part C
├── README.md                  # Complete documentation and setup guide
├── .gitignore                 # Excludes venv, db.sqlite3, __pycache__
│
├── taskmanager/               # Main project configuration folder
│   ├── __init__.py
│   ├── settings.py            # App settings, DB config, templates & static paths
│   ├── urls.py                # Root URL routing (Frontend + API routing)
│   └── wsgi.py                # WSGI entry point for web deployment
│
├── tasks/                     # Task management app folder
│   ├── __init__.py
│   ├── admin.py               # Task model registration for Django Admin
│   ├── models.py              # Task database model definition
│   ├── urls.py                # API URL patterns (/api/tasks/)
│   ├── views.py               # REST API views with input validation & JsonResponse
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py    # Initial migration creating the Task table
│
├── templates/
│   └── index.html             # Single-page frontend template served by Django
│
└── static/
    ├── css/
    │   └── style.css          # Clean, modern, responsive custom CSS styling
    └── js/
        └── script.js          # Client-side API interactions with fetch()
```

---

## 🚀 Setup and Installation Guide

### Prerequisites
- Python 3.10+ installed on your system.
- Git installed (optional, for cloning).

### 1. Clone or Download the Repository
```bash
git clone <your-repository-url>
cd "Mini Task Manager"
```

### 2. Create and Activate a Virtual Environment
- **Windows (Command Prompt / PowerShell)**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
Create the SQLite database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an Admin Superuser (Optional, to access Django Admin)
```bash
python manage.py createsuperuser
```
*(Enter your preferred username, email, and password)*

### 6. Start the Development Server
```bash
python manage.py runserver
```

---

## 🌐 Application Access URLs

- **Web Application Frontend**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Tasks API Endpoint**: [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/)

> 📸 **Reminder**: Capture 2–3 screenshots of the application running in your browser (e.g. main view with pending count, task creation, and filtered view) and place them in the project folder to reference here!

---

## 🔌 API Documentation

| Method | Endpoint | Description | Request Body | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/tasks/` | Retrieve all tasks (supports query params `?status=` and `?priority=`) | None | `200 OK` |
| **POST** | `/api/tasks/` | Create a new task with validation | JSON (title, priority, due_date, optional description) | `201 Created` |
| **PATCH** / **PUT** | `/api/tasks/<id>/` | Update task fields (e.g. mark status as `Done`) | JSON (fields to update) | `200 OK` |
| **DELETE** | `/api/tasks/<id>/` | Delete task by ID | None | `200 OK` |

### Validation Rules
- `title`: Required, non-empty, maximum 100 characters.
- `priority`: Required, must be one of `Low`, `Medium`, `High`.
- `due_date`: Required, valid date format `YYYY-MM-DD`.
- Missing/invalid input returns **HTTP 400 Bad Request** with `{"error": "message"}`.
- Non-existent Task ID returns **HTTP 404 Not Found** with `{"error": "message"}`.

### Example API Requests

#### 1. Create a Task (POST)
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Prepare slides", "priority": "High", "due_date": "2026-11-12", "description": "Presentation for team"}'
```

#### 2. Filter Tasks by Status & Priority (GET)
```bash
curl "http://127.0.0.1:8000/api/tasks/?status=Pending&priority=High"
```

#### 3. Mark Task as Done (PATCH)
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "Done"}'
```

#### 4. Delete a Task (DELETE)
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/
```

---

## 💡 How Django Serves the Frontend

Instead of running separate Node.js or frontend development servers, Django serves both the REST API and the single-page frontend on the exact same port (`http://127.0.0.1:8000/`):

1. **Templates**: In `taskmanager/settings.py`, `TEMPLATES['DIRS']` points to `[BASE_DIR / 'templates']`. When a user visits `/`, `taskmanager/urls.py` routes the request directly to `TemplateView.as_view(template_name='index.html')`.
2. **Static Files**: CSS and JavaScript files reside in `static/css/style.css` and `static/js/script.js`. With `STATIC_URL = '/static/'` and `STATICFILES_DIRS = [BASE_DIR / 'static']`, Django's `{% static '...' %}` template tag dynamically generates the correct browser paths.
3. **No CORS Issues**: Because the frontend and the `/api/tasks/` endpoints share the exact same origin (`http://127.0.0.1:8000`), client-side `fetch()` calls work seamlessly without requiring Cross-Origin Resource Sharing (CORS) middleware.

---

## 🗄️ Part C: How to Execute `queries.sql`

`queries.sql` contains the four assessment SQL queries written for a standalone `tasks` table with the exact sample dataset from the assessment.

### Option 1: Using Python's built-in SQLite (Easiest)
Run in terminal:
```bash
python -c "import sqlite3; conn = sqlite3.connect(':memory:'); conn.cursor().executescript(open('queries.sql').read()); print('All queries executed successfully!')"
```

### Option 2: Using the `sqlite3` CLI
```bash
sqlite3 sample.db < queries.sql
```

### Option 3: Using DB Browser for SQLite
1. Open DB Browser for SQLite.
2. Select **Open Database** or create a temporary database.
3. Switch to the **Execute SQL** tab, paste the contents of `queries.sql`, and press **Run (F5)**.

---

## 🔍 Assumptions Made

1. **Plain Django Views vs DRF**: Plain Django views with `JsonResponse` were deliberately chosen over Django REST Framework to keep the project lightweight, dependency-free, and easy to explain line-by-line during the interview.
2. **CSRF Handling on API**: For simplicity of testing using `fetch()` and standard API clients without token handshakes, `@csrf_exempt` was applied to the JSON API endpoints.
3. **Standalone SQL Exercise**: As instructed in the assessment PDF, `queries.sql` is a completely independent exercise with its own schema and 6 sample rows, kept separate from Django's internal database.

---

## 💭 Reflections (Draft Ideas for Personal Customization)

*(As instructed, here are 2–3 honest starter ideas for each section so you can adapt them into your own words)*

### 1. What was the hardest part, and how did you solve it?
- *Idea 1*: Designing clean input validation in plain Django views without DRF serializers. Solved by writing a reusable `validate_task_data()` helper that validates both creation and partial updates.
- *Idea 2*: Keeping the pending count and table in sync after every asynchronous `fetch()` call. Solved by decoupling data fetching (`loadTasks()`) from DOM rendering (`renderTasks()`).

### 2. What did you learn that was new to you?
- *Idea 1*: Structuring a unified Django project where Django directly serves both the static single-page app and the JSON API under the same domain without CORS complications.
- *Idea 2*: Handling partial updates gracefully with the `PATCH` method using plain `json.loads(request.body)`.

### 3. If you had two more days, what would you add or improve?
- *Idea 1*: User authentication and authorization (letting multiple users have private to-do lists).
- *Idea 2*: Drag-and-drop task reordering and categorization with tags/labels.
- *Idea 3*: Automated email or browser notifications for tasks approaching their due date.

