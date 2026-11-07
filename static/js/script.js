/*
=============================================================
  script.js  –  Mini Task Manager frontend logic

  This file communicates with the Django REST API using
  the browser's built-in fetch() function.

  Structure:
    1. Constants & state
    2. API helpers (fetchTasks, createTask, updateTask, deleteTask)
    3. UI helpers (renderTasks, showNotification, updateCounts)
    4. Event listeners (form submit, filter buttons, delete, done)
=============================================================
*/

'use strict';

// ============================================================
// 1. Constants & Application State
// ============================================================

// Base URL for all API calls – Django backend
const API_BASE = '/api/tasks/';

// Keep track of active filters so we can re-fetch when needed
let currentStatusFilter   = '';
let currentPriorityFilter = '';
let currentSort           = 'created_at';   // default sort

// Today's date string (YYYY-MM-DD) for overdue detection
const TODAY = new Date().toISOString().split('T')[0];

// ============================================================
// 2. API Helper Functions
//    Each function calls one API endpoint and returns data.
// ============================================================

/**
 * fetchTasks(status, priority)
 * Calls GET /api/tasks/?status=...&priority=...
 * Returns a Promise that resolves to an array of task objects.
 */
async function fetchTasks(status = '', priority = '') {
    // Build query string from active filters
    const params = new URLSearchParams();
    if (status)   params.append('status',   status);
    if (priority) params.append('priority', priority);

    const url = API_BASE + (params.toString() ? '?' + params.toString() : '');

    // fetch() sends an HTTP GET request
    const response = await fetch(url);

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch tasks.');
    }

    // .json() parses the JSON text the server sent into a JS array
    return await response.json();
}

/**
 * createTask(taskData)
 * Calls POST /api/tasks/ with JSON body.
 * Returns the created task object.
 */
async function createTask(taskData) {
    const response = await fetch(API_BASE, {
        method: 'POST',
        // Tell the server we're sending JSON
        headers: { 'Content-Type': 'application/json' },
        // JSON.stringify converts a JS object to a JSON string
        body: JSON.stringify(taskData),
    });

    const data = await response.json();

    if (!response.ok) {
        // Server returned an error (4xx or 5xx)
        throw new Error(data.error || 'Failed to create task.');
    }

    return data;
}

/**
 * updateTask(taskId, taskData)
 * Calls PATCH /api/tasks/<id>/ with JSON body.
 * Used for marking done AND for the edit form.
 */
async function updateTask(taskId, taskData) {
    const response = await fetch(`${API_BASE}${taskId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Failed to update task.');
    }

    return data;
}

/**
 * deleteTask(taskId)
 * Calls DELETE /api/tasks/<id>/
 */
async function deleteTask(taskId) {
    const response = await fetch(`${API_BASE}${taskId}/`, {
        method: 'DELETE',
    });

    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to delete task.');
    }

    return true;
}

// ============================================================
// 3. UI Helper Functions
// ============================================================

/**
 * showNotification(message, type)
 * Displays a temporary message on the page.
 * type = 'success' or 'error'
 */
function showNotification(message, type = 'success') {
    const box = document.getElementById('notification');
    box.textContent = (type === 'success' ? '✅ ' : '❌ ') + message;
    box.className = `notification ${type}`;   // set CSS class for colour
    box.classList.remove('hidden');

    // Auto-hide after 4 seconds
    clearTimeout(box._timer);
    box._timer = setTimeout(() => {
        box.classList.add('hidden');
    }, 4000);
}

/**
 * getPriorityOrder(priority)
 * Returns a number so we can sort tasks by priority weight.
 */
function getPriorityOrder(priority) {
    return { 'High': 1, 'Medium': 2, 'Low': 3 }[priority] || 2;
}

/**
 * sortTasks(tasks, sortKey)
 * Sorts the task array in-place based on the selected key.
 */
function sortTasks(tasks, sortKey) {
    tasks.sort((a, b) => {
        if (sortKey === 'due_date') {
            // Earlier date comes first
            return a.due_date.localeCompare(b.due_date);
        }
        if (sortKey === 'priority') {
            // High → Medium → Low
            return getPriorityOrder(a.priority) - getPriorityOrder(b.priority);
        }
        // Default: newest first (created_at descending)
        return b.created_at.localeCompare(a.created_at);
    });
}

/**
 * updateCounts(tasks)
 * Updates the stats bar: pending count and total count.
 */
function updateCounts(tasks) {
    const pending = tasks.filter(t => t.status === 'Pending').length;
    document.getElementById('pending-count').textContent = pending;
    document.getElementById('total-count').textContent   = tasks.length;
}

/**
 * renderTasks(tasks)
 * Takes an array of task objects and builds the HTML table rows.
 * This is called every time we load or refresh the task list.
 */
function renderTasks(tasks) {
    const tbody    = document.getElementById('task-tbody');
    const emptyRow = document.getElementById('empty-row');

    // Sort tasks before rendering
    sortTasks(tasks, currentSort);

    // Update the stats
    updateCounts(tasks);

    if (tasks.length === 0) {
        // Show the "no tasks" message
        tbody.innerHTML = '';
        tbody.appendChild(emptyRow);
        emptyRow.classList.remove('hidden');
        return;
    }

    // Build HTML for all rows
    // We use template literals (backtick strings) to build HTML strings
    const rows = tasks.map(task => {
        const isOverdue = task.status !== 'Done' && task.due_date < TODAY;
        const isDone    = task.status === 'Done';

        // Choose CSS class for the row
        let rowClass = '';
        if (isDone)    rowClass = 'row-done';
        if (isOverdue) rowClass = 'row-overdue';

        // Priority badge CSS class
        const priorityClass = `badge-${task.priority.toLowerCase()}`;
        // Status badge CSS class
        const statusClass   = `badge-${task.status.toLowerCase()}`;

        // Overdue indicator text
        const overdueTag = isOverdue
            ? ' <span class="badge badge-high" title="Overdue">⚠ Overdue</span>'
            : '';

        return `
        <tr class="${rowClass}" data-id="${task.id}">
            <td class="task-title">
                ${escapeHtml(task.title)}${overdueTag}
                ${task.description
                    ? `<div class="task-desc">${escapeHtml(task.description)}</div>`
                    : ''}
            </td>
            <td>
                <span class="badge ${priorityClass}">${task.priority}</span>
            </td>
            <td>${task.due_date}</td>
            <td>
                <span class="badge ${statusClass}">${task.status}</span>
            </td>
            <td class="actions-col">
                <div class="action-buttons">
                    ${!isDone ? `
                        <button class="btn btn-success done-btn"
                                data-id="${task.id}"
                                title="Mark as Done">
                            ✓ Done
                        </button>
                    ` : ''}
                    <button class="btn btn-edit edit-btn"
                            data-id="${task.id}"
                            title="Edit task">
                        ✏ Edit
                    </button>
                    <button class="btn btn-danger delete-btn"
                            data-id="${task.id}"
                            title="Delete task">
                        🗑 Delete
                    </button>
                </div>
            </td>
        </tr>`;
    });

    tbody.innerHTML = rows.join('');
}

/**
 * escapeHtml(str)
 * Prevents XSS (cross-site scripting) by converting special
 * characters to safe HTML entities before inserting user text.
 */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * loadTasks()
 * Main function to fetch tasks from the server and render them.
 * Called on page load and after every add/delete/update.
 */
async function loadTasks() {
    // Show loading indicator
    document.getElementById('loading').classList.remove('hidden');

    try {
        const tasks = await fetchTasks(currentStatusFilter, currentPriorityFilter);
        renderTasks(tasks);
    } catch (err) {
        showNotification(err.message, 'error');
    } finally {
        // Always hide loading indicator when done
        document.getElementById('loading').classList.add('hidden');
    }
}

// ============================================================
// 4. Event Listeners
//    These run when the user interacts with the page.
// ============================================================

// ---- Page Load ----
// When the browser finishes loading the HTML, load tasks automatically.
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();

    // Set today as default due date in the form
    document.getElementById('due_date').value = TODAY;
});

// ---- Add Task Form Submit ----
document.getElementById('task-form').addEventListener('submit', async (event) => {
    // Prevent the form from doing a full-page reload (default browser behavior)
    event.preventDefault();

    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Adding…';

    // Read form values
    const taskData = {
        title:       document.getElementById('title').value.trim(),
        description: document.getElementById('description').value.trim(),
        priority:    document.getElementById('priority').value,
        due_date:    document.getElementById('due_date').value,
    };

    try {
        await createTask(taskData);

        // Clear the form after successful creation
        document.getElementById('task-form').reset();
        document.getElementById('due_date').value = TODAY;  // reset date to today
        document.getElementById('title-counter').textContent = '0 / 100';

        showNotification('Task added successfully!', 'success');

        // Reload task list to show the new task
        await loadTasks();
    } catch (err) {
        showNotification(err.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '➕ Add Task';
    }
});

// ---- Clear Form Button ----
document.getElementById('clear-btn').addEventListener('click', () => {
    document.getElementById('task-form').reset();
    document.getElementById('due_date').value = TODAY;
    document.getElementById('title-counter').textContent = '0 / 100';
});

// ---- Title character counter ----
document.getElementById('title').addEventListener('input', function () {
    document.getElementById('title-counter').textContent =
        `${this.value.length} / 100`;
});

// ---- Filter Buttons (All / Pending / Done) ----
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove 'active' class from all filter buttons
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        // Add 'active' to the clicked button
        btn.classList.add('active');

        // Update state
        currentStatusFilter = btn.dataset.status;

        // Reload tasks with new filter
        loadTasks();
    });
});

// ---- Priority filter dropdown ----
document.getElementById('priority-filter').addEventListener('change', function () {
    currentPriorityFilter = this.value;
    loadTasks();
});

// ---- Sort dropdown ----
document.getElementById('sort-select').addEventListener('change', function () {
    currentSort = this.value;
    loadTasks();
});

// ---- Table row action buttons (Done, Edit, Delete) ----
// We use "event delegation": one listener on the table body catches clicks
// on all buttons inside it, even ones added later by renderTasks().
document.getElementById('task-tbody').addEventListener('click', async (event) => {
    const btn = event.target.closest('button');
    if (!btn) return;   // Click was not on a button

    const taskId = btn.dataset.id;
    if (!taskId) return;

    // --- Mark Done ---
    if (btn.classList.contains('done-btn')) {
        btn.disabled = true;
        try {
            await updateTask(taskId, { status: 'Done' });
            showNotification('Task marked as Done! 🎉', 'success');
            await loadTasks();
        } catch (err) {
            showNotification(err.message, 'error');
            btn.disabled = false;
        }
    }

    // --- Delete ---
    if (btn.classList.contains('delete-btn')) {
        // Ask for confirmation before deleting
        if (!confirm('Are you sure you want to delete this task?')) return;
        btn.disabled = true;
        try {
            await deleteTask(taskId);
            showNotification('Task deleted.', 'success');
            await loadTasks();
        } catch (err) {
            showNotification(err.message, 'error');
            btn.disabled = false;
        }
    }

    // --- Edit ---
    if (btn.classList.contains('edit-btn')) {
        // Find the task data from the row's data-id
        openEditModal(taskId);
    }
});

// ============================================================
// 5. Edit Modal Logic
// ============================================================

/**
 * openEditModal(taskId)
 * Fetches the latest task data and populates the edit form.
 */
async function openEditModal(taskId) {
    try {
        // Fetch all tasks and find the one we want to edit
        // (We re-fetch to get the latest data from the server)
        const tasks = await fetchTasks();
        const task  = tasks.find(t => String(t.id) === String(taskId));

        if (!task) {
            showNotification('Task not found.', 'error');
            return;
        }

        // Fill in the edit form
        document.getElementById('edit-task-id').value   = task.id;
        document.getElementById('edit-title').value     = task.title;
        document.getElementById('edit-description').value = task.description || '';
        document.getElementById('edit-priority').value  = task.priority;
        document.getElementById('edit-due-date').value  = task.due_date;
        document.getElementById('edit-status').value    = task.status;

        // Show the modal
        document.getElementById('edit-modal').classList.remove('hidden');
        document.getElementById('edit-title').focus();

    } catch (err) {
        showNotification(err.message, 'error');
    }
}

/** Close the edit modal */
function closeEditModal() {
    document.getElementById('edit-modal').classList.add('hidden');
    document.getElementById('edit-form').reset();
}

document.getElementById('modal-close-btn').addEventListener('click',  closeEditModal);
document.getElementById('cancel-edit-btn').addEventListener('click',  closeEditModal);

// Close modal when clicking outside the modal box
document.getElementById('edit-modal').addEventListener('click', (event) => {
    if (event.target === document.getElementById('edit-modal')) {
        closeEditModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeEditModal();
});

// ---- Edit Form Submit ----
document.getElementById('edit-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const taskId = document.getElementById('edit-task-id').value;

    const taskData = {
        title:       document.getElementById('edit-title').value.trim(),
        description: document.getElementById('edit-description').value.trim(),
        priority:    document.getElementById('edit-priority').value,
        due_date:    document.getElementById('edit-due-date').value,
        status:      document.getElementById('edit-status').value,
    };

    try {
        await updateTask(taskId, taskData);
        showNotification('Task updated successfully!', 'success');
        closeEditModal();
        await loadTasks();
    } catch (err) {
        showNotification(err.message, 'error');
    }
});

