"""
tasks/views.py

This file contains all the API logic.

A "view" in Django is a Python function that:
  1. Receives an HTTP request
  2. Does something (read/write database)
  3. Returns an HTTP response (here: always JSON)

We use JsonResponse to return JSON instead of HTML.

API Endpoints:
  GET    /api/tasks/        → list all tasks (with optional filters)
  POST   /api/tasks/        → create a new task
  PUT    /api/tasks/<id>/   → update a task (full or partial)
  PATCH  /api/tasks/<id>/   → update a task (partial, same handler)
  DELETE /api/tasks/<id>/   → delete a task
"""

import json
from datetime import date, datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Task


# ---------------------------------------------------------------------------
# Helper function: convert a Task object → Python dict (for JSON output)
# ---------------------------------------------------------------------------
def task_to_dict(task):
    """
    Serialise a Task model instance into a plain dictionary.
    JsonResponse can only return plain Python dicts/lists, not Django objects.
    """
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description or '',       # Return empty string if None
        'priority': task.priority,
        'status': task.status,
        'due_date': task.due_date.strftime('%Y-%m-%d'),  # Format as string
        'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }


# ---------------------------------------------------------------------------
# Helper function: validate incoming task data
# Returns (cleaned_data, error_message)
# If error_message is not None, validation failed.
# ---------------------------------------------------------------------------
def validate_task_data(data, is_update=False):
    """
    Validate incoming JSON data for creating or updating a task.

    Parameters:
        data      – dict parsed from the request body
        is_update – if True, fields are optional (partial update allowed)

    Returns:
        (cleaned, error) where:
          cleaned = dict of validated values  (or None on error)
          error   = string error message      (or None on success)
    """
    cleaned = {}

    # --- Title ---
    if 'title' in data or not is_update:
        title = data.get('title', '').strip()
        if not title:
            return None, 'Title cannot be empty.'
        if len(title) > 100:
            return None, 'Title cannot exceed 100 characters.'
        cleaned['title'] = title

    # --- Description (optional) ---
    if 'description' in data:
        cleaned['description'] = data.get('description', '').strip()

    # --- Priority ---
    if 'priority' in data or not is_update:
        priority = data.get('priority', '').strip()
        valid_priorities = ['Low', 'Medium', 'High']
        if priority not in valid_priorities:
            return None, f"Priority must be one of: {', '.join(valid_priorities)}."
        cleaned['priority'] = priority

    # --- Status (only validated when explicitly provided) ---
    if 'status' in data:
        status = data.get('status', '').strip()
        valid_statuses = ['Pending', 'Done']
        if status not in valid_statuses:
            return None, f"Status must be one of: {', '.join(valid_statuses)}."
        cleaned['status'] = status

    # --- Due Date ---
    if 'due_date' in data or not is_update:
        due_date_str = data.get('due_date', '').strip()
        if not due_date_str:
            return None, 'Due date is required.'
        try:
            # Strictly parse YYYY-MM-DD format
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            cleaned['due_date'] = due_date
        except ValueError:
            return None, 'Due date must be a valid date in YYYY-MM-DD format.'

    return cleaned, None


# ---------------------------------------------------------------------------
# View 1: Handle /api/tasks/  (GET + POST)
# ---------------------------------------------------------------------------
@csrf_exempt   # Disable CSRF for API endpoints (safe for this assessment)
@require_http_methods(['GET', 'POST'])
def task_list(request):
    """
    GET  /api/tasks/           → Return all tasks as JSON
    GET  /api/tasks/?status=Pending  → Filter by status
    GET  /api/tasks/?priority=High   → Filter by priority
    GET  /api/tasks/?status=Pending&priority=High → Both filters
    POST /api/tasks/           → Create a new task
    """

    if request.method == 'GET':
        # Start with all tasks
        tasks = Task.objects.all()

        # --- Apply filters if query parameters are provided ---
        status_filter = request.GET.get('status')
        priority_filter = request.GET.get('priority')

        if status_filter:
            # Validate the filter value
            if status_filter not in ['Pending', 'Done']:
                return JsonResponse(
                    {'error': 'Invalid status filter. Use Pending or Done.'},
                    status=400
                )
            tasks = tasks.filter(status=status_filter)

        if priority_filter:
            if priority_filter not in ['Low', 'Medium', 'High']:
                return JsonResponse(
                    {'error': 'Invalid priority filter. Use Low, Medium, or High.'},
                    status=400
                )
            tasks = tasks.filter(priority=priority_filter)

        # Convert each Task object to a dict, then return as JSON list
        task_list_data = [task_to_dict(task) for task in tasks]
        return JsonResponse(task_list_data, safe=False)

    elif request.method == 'POST':
        # --- Parse the JSON request body ---
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON in request body.'},
                status=400
            )

        # --- Validate the data ---
        cleaned, error = validate_task_data(data, is_update=False)
        if error:
            return JsonResponse({'error': error}, status=400)

        # --- Create the task in the database ---
        task = Task.objects.create(
            title=cleaned['title'],
            description=cleaned.get('description', ''),
            priority=cleaned['priority'],
            status=cleaned.get('status', 'Pending'),  # Default to Pending
            due_date=cleaned['due_date'],
        )

        # Return the created task with HTTP 201 Created
        return JsonResponse(task_to_dict(task), status=201)


# ---------------------------------------------------------------------------
# View 2: Handle /api/tasks/<id>/  (PUT, PATCH, DELETE)
# ---------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(['PUT', 'PATCH', 'DELETE'])
def task_detail(request, task_id):
    """
    PUT   /api/tasks/<id>/  → Full update of a task
    PATCH /api/tasks/<id>/  → Partial update (e.g. just mark as Done)
    DELETE /api/tasks/<id>/ → Delete the task
    """

    # --- Find the task or return 404 ---
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse(
            {'error': f'Task with id {task_id} does not exist.'},
            status=404
        )

    if request.method in ('PUT', 'PATCH'):
        # --- Parse JSON body ---
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON in request body.'},
                status=400
            )

        # For PATCH: is_update=True → fields are optional
        # For PUT:   is_update=True too, to allow partial updates gracefully
        cleaned, error = validate_task_data(data, is_update=True)
        if error:
            return JsonResponse({'error': error}, status=400)

        # --- Apply validated changes to the task ---
        # Only update fields that were provided in the request
        if 'title' in cleaned:
            task.title = cleaned['title']
        if 'description' in cleaned:
            task.description = cleaned['description']
        if 'priority' in cleaned:
            task.priority = cleaned['priority']
        if 'status' in cleaned:
            task.status = cleaned['status']
        if 'due_date' in cleaned:
            task.due_date = cleaned['due_date']

        # Save the changes to the database
        task.save()

        return JsonResponse(task_to_dict(task))

    elif request.method == 'DELETE':
        # Delete the task from the database
        task.delete()
        # Return 204 No Content (success, nothing to return)
        return JsonResponse(
            {'message': f'Task {task_id} deleted successfully.'},
            status=200
        )

