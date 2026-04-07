-- ==============================================================
-- Tech Ethics & SQL Analysis Guide
-- Finding Inherent Bias and Representational Discrepancies
-- ==============================================================

-- ==============================================================
-- PART 1: BASELINE DEMOGRAPHICS
-- Before analyzing interactions, we must understand our student body.
-- What is the "expected" turnout if everything is fair and equal?
-- ==============================================================

-- 1. Total Student Count
SELECT COUNT(*) AS total_students FROM students;

-- 2. General Demographics: International Students
-- How many are international vs domestic, and what is the percentage?
SELECT 
    is_international,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 2) AS percentage
FROM students
GROUP BY is_international;

-- 3. General Demographics: Non-Traditional Students
-- How many are non-traditional vs traditional?
SELECT 
    is_non_traditional,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 2) AS percentage
FROM students
GROUP BY is_non_traditional;

-- 4. General Demographics: Dormitory Representation
-- What is the baseline percentage of student population in each dorm?
SELECT 
    dorm_name, 
    COUNT(*) AS resident_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 2) AS percentage
FROM students
GROUP BY dorm_name
ORDER BY resident_count DESC;

-- ==============================================================
-- PART 2: BASELINE INTERACTIONS
-- Does overall campus resource usage match our baseline demographics? 
-- ==============================================================

-- 5. Overall Interactions by International Status
-- Are international students using resources at roughly their baseline rate (~20%)?
SELECT 
    s.is_international,
    COUNT(ri.interaction_id) AS total_interactions,
    ROUND(COUNT(ri.interaction_id) * 100.0 / (SELECT COUNT(*) FROM resource_interactions), 2) AS percentage_of_interactions
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
GROUP BY s.is_international;

-- 6. Overall Interactions by Non-Traditional Status
-- Are non-traditional students using resources matching their baseline?
SELECT 
    s.is_non_traditional,
    COUNT(ri.interaction_id) AS total_interactions,
    ROUND(COUNT(ri.interaction_id) * 100.0 / (SELECT COUNT(*) FROM resource_interactions), 2) AS percentage_of_interactions
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
GROUP BY s.is_non_traditional;

-- 7. Overall Interactions by Dorm
-- Is any dorm generally isolated from campus resources as a whole?
SELECT 
    s.dorm_name,
    COUNT(ri.interaction_id) AS total_interactions,
    ROUND(COUNT(ri.interaction_id) * 100.0 / (SELECT COUNT(*) FROM resource_interactions), 2) AS percentage_of_interactions
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
GROUP BY s.dorm_name
ORDER BY total_interactions DESC;

-- ==============================================================
-- PART 3: PINPOINTING DISCREPANCIES (THE HIDDEN BIASES)
-- Now we investigate specific resources to see if certain demographics 
-- are systemically left out of particular services.
-- ==============================================================

-- 8. Identify Bias: Low International Turnout
-- Look at "Drop-In Writing Tutoring" (Resource ID 4)
-- The baseline international population is 20%. Let's see who is attending this specific resource.
SELECT 
    r.title,
    s.is_international,
    COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total_resource_interactions.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (
    SELECT COUNT(*) AS total 
    FROM resource_interactions 
    WHERE resource_id = 4
) AS total_resource_interactions
WHERE ri.resource_id = 4
GROUP BY s.is_international, r.title;


-- 9. Identify Bias: Low Non-Traditional Turnout
-- Look at "Free Flu Vaccine Clinic" (Resource ID 30)
-- The baseline non-traditional population is 10%. Are they making it to the clinic?
SELECT 
    r.title,
    s.is_non_traditional,
    COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total_resource_interactions.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (
    SELECT COUNT(*) AS total 
    FROM resource_interactions 
    WHERE resource_id = 30
) AS total_resource_interactions
WHERE ri.resource_id = 30
GROUP BY s.is_non_traditional, r.title;


-- 10. Identify Bias: Geographic/Dorm Isolation
-- Look at "Sunday Evening Dinner" (Resource ID 18)
-- Are students from the Draper dorm attending safely?
SELECT 
    r.title,
    s.dorm_name,
    COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total_resource_interactions.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (
    SELECT COUNT(*) AS total 
    FROM resource_interactions 
    WHERE resource_id = 18
) AS total_resource_interactions
WHERE ri.resource_id = 18
GROUP BY s.dorm_name, r.title
ORDER BY interaction_count DESC;


-- ==============================================================
-- PART 4: AUTOMATED DISCOVERY (ADVANCED)
-- ==============================================================

-- 11. Find ANY Resource with a heavily biased dorm turnout naturally.
-- This query ranks resources and dorms to find anomalies without knowing the answer beforehand.
-- It filters for cases where a specific dorm makes up LESS than 3% of the turnout for a resource.
WITH ResourceDormCounts AS (
    SELECT 
        ri.resource_id,
        r.title,
        s.dorm_name,
        COUNT(ri.interaction_id) AS dorm_turnout
    FROM resource_interactions ri
    JOIN students s ON ri.student_id = s.student_id
    JOIN resources r ON ri.resource_id = r.resource_id
    GROUP BY ri.resource_id, r.title, s.dorm_name
),
ResourceTotals AS (
    SELECT 
        resource_id,
        SUM(dorm_turnout) AS total_turnout
    FROM ResourceDormCounts
    GROUP BY resource_id
)
SELECT 
    rdc.title,
    rdc.dorm_name,
    rdc.dorm_turnout,
    rt.total_turnout,
    ROUND(rdc.dorm_turnout * 100.0 / rt.total_turnout, 2) AS dorm_percentage
FROM ResourceDormCounts rdc
JOIN ResourceTotals rt ON rdc.resource_id = rt.resource_id
WHERE ROUND(rdc.dorm_turnout * 100.0 / rt.total_turnout, 2) < 3.0
ORDER BY dorm_percentage ASC;
