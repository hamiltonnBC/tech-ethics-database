-- Schema: Campus Resource Hub
-- Database: SQLite
-- 

-- 1. Departments Table
-- This table stores information about the different departments
-- across the campus that maintain resources.
CREATE TABLE IF NOT EXISTS Departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    contact_email TEXT
);

-- 2. Resources Table
-- This table lists every specific item or offering available to students.
-- It links to the Departments table using a Foreign Key to show ownership.
CREATE TABLE IF NOT EXISTS Resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL,     -- e.g., 'Hardware', 'Software', 'Room', 'Book'
    department_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES Departments(id)
);

-- 3. Students Table
-- A list of all active students who are eligible to borrow items.
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    enrollment_year INTEGER NOT NULL
);

-- 4. ResourceLog Table
-- This table tracks transactions whenever a student borrows a resource.
-- It has two foreign keys to link Students and Resources.
CREATE TABLE IF NOT EXISTS ResourceLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    resource_id INTEGER,
    borrowed_date DATE NOT NULL,
    returned_date DATE,
    status TEXT NOT NULL,   -- e.g., 'Active', 'Returned', 'Overdue'
    FOREIGN KEY(student_id) REFERENCES Students(id),
    FOREIGN KEY(resource_id) REFERENCES Resources(id)
);

-- 5. Reviews Table
-- Allows students to rate their experience with specific resources.
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    resource_id INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- Rating must be 1 to 5
    comment TEXT,
    FOREIGN KEY(student_id) REFERENCES Students(id),
    FOREIGN KEY(resource_id) REFERENCES Resources(id)
);
