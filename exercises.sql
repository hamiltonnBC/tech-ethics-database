-- ==============================================
-- SQL Workshop Exercises: Campus Resource Hub
-- ==============================================

-- Directions: Write your SQL queries below each exercise prompt.
-- To run this file against your database:
-- sqlite3 campus_resources.db < exercises.sql

-- ----------------------------------------------
-- Part 1: Select Queries
-- ----------------------------------------------

-- 1. Select all the student records.
-- Type your SELECT statement here:


-- 2. Select only the full names and emails of all students who live in the 'Ecovillage' dorm.
-- Type your SELECT statement here:


-- 3. Select all the resources that belong to the 'Financial' category.
-- Type your SELECT statement here:


-- ----------------------------------------------
-- Part 2: Alter and Update
-- ----------------------------------------------

-- 4. The providers table needs to store phone numbers. 
-- Alter the table to add a new TEXT column named "phone_number".
-- Type your ALTER statement here:


-- 5. A student named Alice (student_id=1) just became a 'Junior'.
-- Update her class_year in the students table.
-- Type your UPDATE statement here:


-- ----------------------------------------------
-- Part 3: Insert and Delete
-- ----------------------------------------------

-- 6. A new academic program just launched! 
-- Insert a new record into the programs table for 'Data Science'.
-- Type your INSERT statement here:


-- 7. The 'Math Club' provider is moving to a new office.
-- Update their location to 'Science Center, Room 304'.
-- Type your UPDATE statement here:


-- 8. The resource with resource_id = 3 was a mistake and needs to be deleted.
-- Delete the resource where resource_id = 3.
-- Type your DELETE statement here:


-- ----------------------------------------------
-- Part 4: Challenge Questions (JOINs)
-- ----------------------------------------------

-- 9. Which provider offers the "Summer Internship Grant"? 
-- Write a JOIN query to list the Resource Title and the Provider Name.
-- Type your JOIN statement here:


-- 10. List all students along with the names of the programs they are taking (either 'Major' or 'Minor').
-- Write a JOIN query that connects students, student_programs, and programs.
-- Type your JOIN statement here:


-- ----------------------------------------------
-- Part 5: Resource Interactions
-- ----------------------------------------------

-- 11. Log a new interaction! 
-- Insert a record into the resource_interactions table for student_id = 1 and resource_id = 2.
-- Type your INSERT statement here:


-- 12. Write a JOIN query to find all notes from resource_interactions along with the student's full name.
-- Type your JOIN statement here:

