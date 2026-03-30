-- WORKSHOP EXERCISE 1: Creating your first table
-- Scenario: Building a database for local community gardens to track food distribution.

CREATE TABLE community_gardens (
    id SERIAL PRIMARY KEY,
    garden_name VARCHAR(100) NOT NULL,
    location TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    date_established DATE
);

-- TO RUN THIS: 
-- Or use the terminal: psql -U postgres -d workshop -f exercises.sql
