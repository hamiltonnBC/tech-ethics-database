-- 3A: Insert Resource Interactions (Relies on 'students' and 'resources')
-- Log that Alice (student 1) interacted with the Summer Internship Grant (resource 1)
INSERT INTO resource_interactions (student_id, resource_id, interaction_date, notes) VALUES
(1, 1, '2026-04-07', 'Alice requested an application form.'),
(2, 3, '2026-04-06', 'Carlos dropped in for Calc II help.');
