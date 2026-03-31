-- Dummy Data Seed: Campus Resource Hub
-- Database: SQLite

-- Enable foreign key checking (SQLite has it disabled by default)
PRAGMA foreign_keys = ON;

-- Clear out any existing data (Optional, useful when rerunning)
DELETE FROM Reviews;
DELETE FROM ResourceLog;
DELETE FROM Students;
DELETE FROM Resources;
DELETE FROM Departments;

-- Insert Departments
INSERT INTO Departments (name, location, contact_email) 
VALUES 
('Media Studies', 'Communications Bldg, Room 201', 'media@campus.edu'),
('Computer Science', 'Tech Lab A', 'cs@campus.edu'),
('Library Services', 'Main Library Hub', 'library@campus.edu');

-- Insert Resources
INSERT INTO Resources (name, description, type, department_id) 
VALUES 
('Canon EOS 80D', 'DSLR Camera for student media projects', 'Hardware', 1),
('MacBook Pro M2', 'Laptop with Adobe Suite and Xcode', 'Hardware', 2),
('Private Study Room 4A', 'Quiet workspace with whiteboard', 'Room', 3),
('JetBrains IntelliJ IDEA IDE', 'Educational Software License Keys', 'Software', 2);

-- Insert Students
INSERT INTO Students (first_name, last_name, email, enrollment_year) 
VALUES 
('Alice', 'Smith', 'asmith@campus.edu', 2022),
('Bob', 'Johnson', 'bjohnson@campus.edu', 2023),
('Charlie', 'Brown', 'cbrown@campus.edu', 2024),
('Diana', 'Prince', 'dprince@campus.edu', 2023);

-- Insert ResourceLogs
INSERT INTO ResourceLog (student_id, resource_id, borrowed_date, returned_date, status) 
VALUES 
(1, 1, '2023-10-10', '2023-10-15', 'Returned'),
(2, 3, '2023-11-01', '2023-11-01', 'Returned'),
(3, 2, '2024-01-15', NULL, 'Active'),
(1, 4, '2024-02-01', NULL, 'Active');

-- Insert Reviews
INSERT INTO Reviews (student_id, resource_id, rating, comment)
VALUES
(1, 1, 5, 'Great camera, easy to use.'),
(2, 3, 4, 'Nice and quiet, but the markers were dry.');
