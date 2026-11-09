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
git clone https://github.com/NandiniY018/mini-task-manager.git
cd mini-task-manager
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

## 📝 Part D — Assessment Questions & Answers

### 1. How do I set up and run Part A and Part B (include the commands, for example for migrations)?

To set up and run both the Backend API (Part A) and the Web Frontend (Part B):

1. **Clone the repository and navigate into the folder**:
   ```bash
   git clone https://github.com/NandiniY018/mini-task-manager.git
   cd mini-task-manager
   ```

2. **Create and activate a virtual environment**:
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations** (creates the SQLite database and tasks table):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **(Optional) Create an admin superuser** to access the Django Admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the local development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - **Web Page (Part B)**: Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Backend API (Part A)**: Accessible at [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/)
   - **Django Admin**: Accessible at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### 2. What was the hardest part, and how did you solve it?

- **Handling input validation cleanly without external libraries**: Writing comprehensive validation in plain Django views (without Django REST Framework serializers) for fields like `due_date` (strict `YYYY-MM-DD` parsing), non-empty `title` (max 100 characters), and restricted `priority` choices was challenging. I solved this by building a dedicated `validate_task_data()` helper that validates both full creations (`POST`) and partial updates (`PATCH`), returning consistent HTTP 400 JSON errors.
- **Keeping UI state and pending counts synchronized**: Ensuring that the "Pending Tasks" counter and table dynamically updated without requiring a full page refresh after every Add, Mark Done, or Delete action. I solved this by structuring the JavaScript into clean modular functions (`fetchTasks`, `renderTasks`, and `updateCounts`), where the pending count is recalculated directly from the latest task array on every render.

---

### 3. What did you learn that was new to you?

- **Serving a Single-Page App directly from Django**: I learned how to use Django's `TemplateView` along with static files configuration so that Django serves both the REST API and the frontend HTML/CSS/JS from the exact same address (`http://127.0.0.1:8000/`), eliminating any CORS (Cross-Origin Resource Sharing) complications.
- **Handling raw JSON requests with `PATCH`**: Working directly with `request.body` and `json.loads()` to process `PATCH` HTTP requests for partial model updates, allowing the status to be toggled to `Done` with minimal payload overhead.
- **Event Delegation in JavaScript**: Using a single event listener on the `<tbody>` element rather than attaching listeners to each button individually, making the DOM updates cleaner and avoiding memory leaks.

---

### 4. If you had two more days, what would you add or improve?

- **User Authentication**: Implement user registration and login so that multiple users can manage their own personal task lists securely.
- **Task Search & Pagination**: Add a search bar to filter tasks by title or description keyword, and paginate the task table for better performance with hundreds of tasks.
- **Overdue Task Reminders**: Add email notifications or browser alerts when a pending task's due date is within 24 hours.
- **Drag-and-Drop Task Ordering**: Allow users to drag and reorder tasks based on personal urgency.

