-- 2B: Insert Student Programs (Relies on 'students' and 'programs')
-- Link Alice (id:1) to Computer Science (id:1) as Major
-- Link Carlos (id:2) to Ethics (id:2) as Minor
INSERT INTO student_programs (student_id, program_id, type) VALUES
(1, 1, 'Major'),
(2, 2, 'Minor'),
(3, 1, 'Major');
