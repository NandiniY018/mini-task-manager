-- =============================================================
-- queries.sql  –  Florix Technologies Intern Assessment
-- Part C: The SQL Queries (Separate from Django database)
-- =============================================================

-- Table schema as specified in the assessment PDF:
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    priority TEXT,
    status TEXT,
    due_date TEXT
);

-- Exact sample records as specified in the assessment PDF:
INSERT INTO tasks VALUES
    (1, 'Prepare slides', 'High', 'Pending', '2026-11-12'),
    (2, 'Pay electricity bill', 'Medium', 'Done', '2026-11-03'),
    (3, 'Fix login bug', 'High', 'Pending', '2026-11-08'),
    (4, 'Buy groceries', 'Low', 'Pending', '2026-11-09'),
    (5, 'Update resume', 'Medium', 'Pending', '2026-11-15'),
    (6, 'Team meeting notes', 'Low', 'Done', '2026-11-06');


-- =============================================================
-- QUERY 1: Show all tasks that have High priority and are still Pending.
-- Filters rows where priority is 'High' AND status is 'Pending'.
-- =============================================================
SELECT *
FROM tasks
WHERE priority = 'High'
  AND status = 'Pending';

-- Expected Output:
-- 1|Prepare slides|High|Pending|2026-11-12
-- 3|Fix login bug|High|Pending|2026-11-08


-- =============================================================
-- QUERY 2: Show how many tasks there are for each status.
-- Groups records by status ('Done', 'Pending') and counts occurrences.
-- =============================================================
SELECT status, COUNT(*) AS count
FROM tasks
GROUP BY status;

-- Expected Output:
-- Done|2
-- Pending|4


-- =============================================================
-- QUERY 3: Show the tasks that are not Done and have a due date before 2026-11-10, earliest due date first.
-- Filters where status != 'Done' and due_date < '2026-11-10', ordered ascending by due_date.
-- =============================================================
SELECT *
FROM tasks
WHERE status != 'Done'
  AND due_date < '2026-11-10'
ORDER BY due_date ASC;

-- Expected Output:
-- 3|Fix login bug|High|Pending|2026-11-08
-- 4|Buy groceries|Low|Pending|2026-11-09


-- =============================================================
-- QUERY 4: Show the title and due date of the Pending task that is due first.
-- Filters for status = 'Pending', orders by earliest due_date, and limits result to 1.
-- =============================================================
SELECT title, due_date
FROM tasks
WHERE status = 'Pending'
ORDER BY due_date ASC
LIMIT 1;

-- Expected Output:
-- Fix login bug|2026-11-08
