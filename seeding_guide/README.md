# Database Seeding Guide

Welcome to the data seeding tutorial!

When building a relational database, you cannot insert data in a completely random order. Relational databases enforce **referential integrity** using Foreign Keys. This means that if a record in Table A relies on a record in Table B (like a resource needing a provider), the record in Table B *must exist first*.

Our `campus_resources.db` has six tables, and several of them are dependent on others.

## The Dependency Chain
To avoid foreign key constraint errors, we must insert our mock data in a specific order:

1. **Independent Tables** (Can be seeded anytime, they rely on nothing):
   - `providers`
   - `students`
   - `programs`

2. **First-Level Dependent Tables** (Rely on the independent tables):
   - `resources` (Depends on `providers` existing)
   - `student_programs` (Depends on both `students` and `programs` existing)

3. **Second-Level Dependent Tables** (Rely on first-level tables):
   - `resource_interactions` (Depends on both `students` and `resources` existing)

## Step-By-Step Seeding

We have split the data seeding into individual script files (`1a`, `1b`, `2a`, etc.) so you can see exactly which level you are inserting into.

### Instructions:
1. Open your terminal and connect to your database at the root of the project:
   ```bash
   sqlite3 campus_resources.db
   ```
2. Run the seed files one by one to see how the schema builds up safely:
   ```sql
   .read seeding_guide/1a_insert_providers.sql
   .read seeding_guide/1b_insert_students.sql
   .read seeding_guide/1c_insert_programs.sql
   .read seeding_guide/2a_insert_resources.sql
   .read seeding_guide/2b_insert_student_programs.sql
   .read seeding_guide/3a_insert_resource_interactions.sql
   ```

*(Alternatively, if you want to insert everything automatically at once, we've provided a `seed_all.sql` file. Just run: `.read seeding_guide/seed_all.sql`)*

3. Verify the data successfully went in:
   ```sql
   SELECT * FROM resources;
   ```
   *(Don't forget to use `.mode box` first for a pretty layout!)*

Now head back to the root `README.md` and start with your exercises!
