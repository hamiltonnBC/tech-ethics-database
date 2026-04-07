-- 1. Providers Table (Centers, Departments, Clubs)
CREATE TABLE providers (
    provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    provider_type TEXT, -- e.g., 'Department', 'Center', 'Club'
    location TEXT,
    website TEXT,
    contact_email TEXT,
    contact_name TEXT   
);

-- 2. Students Table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    dorm_name TEXT, -- e.g., 'Ecovillage', 'Danforth'
    class_year TEXT, -- e.g., 'Freshman', 'Sophomore', 'Junior', 'Senior', 'Alum'
    is_non_traditional INTEGER DEFAULT 0, -- 0 for No, 1 for Yes
    is_international INTEGER DEFAULT 0
);

-- 3. Academic Programs (Majors and Minors)
CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name TEXT NOT NULL UNIQUE
);

-- 4. Student-Program Bridge (The Many-to-Many Link)
CREATE TABLE student_programs (
    student_id INTEGER,
    program_id INTEGER,
    type TEXT NOT NULL, -- 'Major' or 'Minor'
    PRIMARY KEY (student_id, program_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

-- 5. Resources Table
CREATE TABLE resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT, -- e.g., 'Financial', 'Academic', 'Career'
    description TEXT,
    expiration_date TEXT, -- Stored as 'YYYY-MM-DD'
    
    -- Eligibility Requirements (Data-driven logic)
    req_non_trad_only INTEGER DEFAULT 0, 
    req_dorm_specific TEXT, -- e.g., 'Ecovillage' or NULL if open to all
    req_min_class_year TEXT, -- e.g., 'Junior'
    
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

-- 6. Resource Interaction Log
CREATE TABLE resource_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    interaction_date TEXT DEFAULT (CURRENT_DATE), -- Auto-fills with 'YYYY-MM-DD'
    notes TEXT, -- Optional: "Student requested follow-up" or "Resume reviewed"
    
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);