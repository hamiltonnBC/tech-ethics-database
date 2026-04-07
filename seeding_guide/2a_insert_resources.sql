-- 2A: Insert Resources (Relies on 'providers')
-- Notice how provider_id points to the IDs generated above
-- provider_id 1 is 'Career Services', 2 is 'Math Club', 3 is 'First-Gen Center'
INSERT INTO resources (provider_id, title, category, description, expiration_date, req_non_trad_only, req_dorm_specific, req_min_class_year) VALUES
(1, 'Summer Internship Grant', 'Financial', 'A $1000 grant for summer internships.', '2026-06-01', 0, NULL, 'Junior'),
(3, 'First-Gen Textbook Fund', 'Academic', 'Assistance for purchasing core textbooks.', '2026-09-01', 0, NULL, 'Freshman'),
(2, 'Math Tutoring Center', 'Academic', 'Drop-in tutoring for all math courses.', NULL, 0, NULL, NULL);
