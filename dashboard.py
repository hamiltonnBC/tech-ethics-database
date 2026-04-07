# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "streamlit",
#     "pandas",
# ]
# ///

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def get_eligible_resources(conn, student):
    resources = pd.read_sql_query("SELECT r.*, p.name as provider_name FROM resources r JOIN providers p ON r.provider_id = p.provider_id", conn)
    
    year_rank = {"Freshman": 1, "Sophomore": 2, "Junior": 3, "Senior": 4, "Alum": 5}
    st_rank = year_rank.get(student['class_year'], 0)
    
    eligible = []
    for _, res in resources.iterrows():
        # Check non trad
        if res['req_non_trad_only'] == 1 and student['is_non_traditional'] == 0:
            continue
        # Check dorm
        if pd.notna(res['req_dorm_specific']) and res['req_dorm_specific'] != student['dorm_name']:
            continue
        # Check year
        if pd.notna(res['req_min_class_year']):
            req_rank = year_rank.get(res['req_min_class_year'], 0)
            if st_rank < req_rank:
                continue
        eligible.append(res)
    
    if eligible:
        return pd.DataFrame(eligible)[['title', 'category', 'provider_name', 'description']]
    else:
        return pd.DataFrame()

def student_view(conn):
    st.header("Student Perspective")
    st.write("View the database through the lens of a specific student to see which resources they are individually eligible for.")
    
    with st.expander("Show SQL Command: Fetch Students"):
        st.code("SELECT * FROM students;", language="sql")
        
    students = pd.read_sql_query("SELECT * FROM students", conn)
    if students.empty:
        st.warning("No students found. Please seed the database.")
        return
    
    # Dropdown
    student_dict = {row['student_id']: f"{row['full_name']} ({row['class_year']})" for idx, row in students.iterrows()}
    st_id = st.selectbox("Select Student Profile", options=list(student_dict.keys()), format_func=lambda x: student_dict[x])
    
    selected = students[students['student_id'] == st_id].iloc[0]
    
    st.markdown("---")
    st.subheader(f"Profile: {selected['full_name']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Dorm", selected['dorm_name'] if pd.notna(selected['dorm_name']) else "Off-Campus")
    col2.metric("Class Year", selected['class_year'])
    col3.metric("Non-Traditional", "Yes" if selected['is_non_traditional'] else "No")
    
    st.markdown("---")
    st.subheader("Your Eligible Resources")
    
    with st.expander("Show SQL Command: Eligible Resources Logic"):
        st_non_trad = selected['is_non_traditional']
        st_dorm = selected['dorm_name'] if pd.notna(selected['dorm_name']) else "NULL"
        sql_logic = f"""-- Here is the conceptual SQL filtering out resources you cannot access:
SELECT r.title, r.category, p.name as provider_name, r.description
FROM resources r
JOIN providers p ON r.provider_id = p.provider_id
WHERE (r.req_non_trad_only = 0 OR r.req_non_trad_only <= {st_non_trad})
  AND (r.req_dorm_specific IS NULL OR r.req_dorm_specific = '{st_dorm}')
  -- Note: Class year ranking logic is handled by Python in this app!
"""
        st.code(sql_logic, language="sql")
        
    eligible_df = get_eligible_resources(conn, selected)
    if not eligible_df.empty:
        st.dataframe(eligible_df, use_container_width=True, hide_index=True)
    else:
        st.info("No resources available for this profile criteria right now.")
        
    st.markdown("---")
    st.subheader("My Interaction History")
    
    history_query = f"""SELECT r.title as Resource, ri.interaction_date as Date, ri.notes as Notes
FROM resource_interactions ri
JOIN resources r ON ri.resource_id = r.resource_id
WHERE ri.student_id = {st_id}
ORDER BY ri.interaction_date DESC"""

    with st.expander("Show SQL Command: Interaction History"):
        st.code(history_query, language="sql")

    history = pd.read_sql_query(history_query, conn)
    if not history.empty:
        st.dataframe(history, use_container_width=True, hide_index=True)
    else:
        st.write("You haven't requested any resources yet.")

def log_interaction(conn):
    st.header("Log Interaction (Staff View)")
    st.write("Staff can use this form to easily insert a new record into the `resource_interactions` table.")
    
    with st.expander("Show SQL Commands: Populate Dropdowns"):
        st.code("""-- Fetching lists to fill the dropdown menus:
SELECT student_id, full_name FROM students;
SELECT resource_id, title FROM resources;""", language="sql")
        
    students = pd.read_sql_query("SELECT student_id, full_name FROM students", conn)
    resources = pd.read_sql_query("SELECT resource_id, title FROM resources", conn)
    
    if students.empty or resources.empty:
        st.warning("Ensure Students and Resources exist before logging interactions.")
        return
        
    st_opts = {row['student_id']: row['full_name'] for _, row in students.iterrows()}
    res_opts = {row['resource_id']: row['title'] for _, row in resources.iterrows()}
    
    with st.expander("Show SQL Command: Insert Interaction"):
        st.code("""INSERT INTO resource_interactions (student_id, resource_id, interaction_date, notes) 
VALUES (?, ?, ?, ?);
-- The '?' symbols are parameterized inputs protected from SQL injection!""", language="sql")
        
    with st.form("interaction_form", clear_on_submit=True):
        st_id = st.selectbox("Select Student", options=list(st_opts.keys()), format_func=lambda x: st_opts[x])
        res_id = st.selectbox("Select Resource", options=list(res_opts.keys()), format_func=lambda x: res_opts[x])
        notes = st.text_area("Interaction Notes (Optional)")
        
        submitted = st.form_submit_button("Log Interaction")
        if submitted:
            cursor = conn.cursor()
            date_str = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO resource_interactions (student_id, resource_id, interaction_date, notes) VALUES (?, ?, ?, ?)", (st_id, res_id, date_str, notes))
            conn.commit()
            st.success(f"Successfully logged interaction for {st_opts[st_id]}!")

def admin_view(conn):
    st.header("Admin Dashboard")
    st.write("Directly manage the database and add new Providers or Resources.")
    
    tab1, tab2, tab3 = st.tabs(["Raw Data Viewer", "Add New Provider", "Add New Resource"])
    
    with tab1:
        st.subheader("Database Tables")
        table = st.selectbox("Select Table to View", ["providers", "resources", "students", "programs", "student_programs", "resource_interactions"])
        
        with st.expander(f"Show SQL Command: View {table}"):
            st.code(f"SELECT * FROM {table};", language="sql")
            
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Insert New Provider")
        
        with st.expander("Show SQL Command: Insert Provider"):
            st.code("""INSERT INTO providers (name, provider_type, location, website, contact_email, contact_name) 
VALUES (?, ?, ?, ?, ?, ?);""", language="sql")
            
        with st.form("add_provider", clear_on_submit=True):
            p_name = st.text_input("Name")
            p_type = st.selectbox("Type", ["Department", "Center", "Club"])
            p_loc = st.text_input("Location")
            p_web = st.text_input("Website")
            p_email = st.text_input("Contact Email")
            p_contact = st.text_input("Contact Name")
            if st.form_submit_button("Add Provider"):
                if p_name and p_type:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO providers (name, provider_type, location, website, contact_email, contact_name) VALUES (?, ?, ?, ?, ?, ?)", 
                                   (p_name, p_type, p_loc, p_web, p_email, p_contact))
                    conn.commit()
                    st.success("Provider added successfully!")
                else:
                    st.error("Name and Type are required.")
                    
    with tab3:
        st.subheader("Insert New Resource")
        providers = pd.read_sql_query("SELECT provider_id, name FROM providers", conn)
        if not providers.empty:
            
            with st.expander("Show SQL Command: Insert Resource"):
                st.code("""INSERT INTO resources (provider_id, title, category, description, req_non_trad_only, req_dorm_specific, req_min_class_year) 
VALUES (?, ?, ?, ?, ?, ?, ?);""", language="sql")
                
            p_opts = {row['provider_id']: row['name'] for _, row in providers.iterrows()}
            with st.form("add_resource", clear_on_submit=True):
                r_prov = st.selectbox("Assign to Provider", options=list(p_opts.keys()), format_func=lambda x: p_opts[x])
                r_title = st.text_input("Resource Title")
                r_cat = st.selectbox("Category", ["Financial", "Academic", "Career", "Wellness", "Other"])
                r_desc = st.text_area("Description")
                
                st.write("**Eligibility Filter Requirements**")
                r_non_trad = st.checkbox("Requires Non-Traditional Status")
                r_dorm = st.text_input("Specific Dorm Required (Leave blank for open to all)")
                r_year = st.selectbox("Minimum Class Year", ["None", "Freshman", "Sophomore", "Junior", "Senior"])
                
                if st.form_submit_button("Add Resource"):
                    if r_title:
                        cursor = conn.cursor()
                        n_trad = 1 if r_non_trad else 0
                        dorm = r_dorm if r_dorm.strip() else None
                        mx_year = None if r_year == "None" else r_year
                        
                        cursor.execute("INSERT INTO resources (provider_id, title, category, description, req_non_trad_only, req_dorm_specific, req_min_class_year) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                       (r_prov, r_title, r_cat, r_desc, n_trad, dorm, mx_year))
                        conn.commit()
                        st.success("Resource added successfully!")
                    else:
                        st.error("Title is required.")
        else:
            st.warning("Please add at least one Provider to the database before creating a Resource.")
def schema_explained_view():
    st.header("Schema Explained")
    st.write("A comprehensive guide to the database structure, relationships, and design choices. Perfect for teaching and understanding the architecture.")
    
    st.markdown("---")
    st.subheader("High-Level Relationship Diagram")
    st.graphviz_chart('''
    digraph Schema {
        rankdir=LR;
        node [shape=none, fontname="Helvetica"];
        edge [color="#555555", fontsize=10];

        providers [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#4A90E2"><font color="white"><b>Providers</b></font></td></tr>
            <tr><td port="id" align="left"><u>provider_id (PK)</u></td></tr>
            <tr><td align="left">name</td></tr>
            <tr><td align="left">provider_type</td></tr>
            <tr><td align="left">location</td></tr>
            <tr><td align="left">website</td></tr>
            <tr><td align="left">contact_email</td></tr>
            <tr><td align="left">contact_name</td></tr>
          </table>
        >];
        
        resources [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#3498DB"><font color="white"><b>Resources</b></font></td></tr>
            <tr><td port="id" align="left"><u>resource_id (PK)</u></td></tr>
            <tr><td port="fk_prov" align="left">provider_id (FK)</td></tr>
            <tr><td align="left">title</td></tr>
            <tr><td align="left">category</td></tr>
            <tr><td align="left">description</td></tr>
            <tr><td align="left">expiration_date</td></tr>
            <tr><td align="left">req_non_trad_only</td></tr>
            <tr><td align="left">req_dorm_specific</td></tr>
            <tr><td align="left">req_min_class_year</td></tr>
          </table>
        >];

        interactions [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#F5A623"><font color="black"><b>Resource_Interactions</b></font></td></tr>
            <tr><td port="id" align="left"><u>interaction_id (PK)</u></td></tr>
            <tr><td port="fk_res" align="left">resource_id (FK)</td></tr>
            <tr><td port="fk_stu" align="left">student_id (FK)</td></tr>
            <tr><td align="left">interaction_date</td></tr>
            <tr><td align="left">notes</td></tr>
          </table>
        >];

        students [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#BB6BD9"><font color="white"><b>Students</b></font></td></tr>
            <tr><td port="id" align="left"><u>student_id (PK)</u></td></tr>
            <tr><td align="left">full_name</td></tr>
            <tr><td align="left">email</td></tr>
            <tr><td align="left">dorm_name</td></tr>
            <tr><td align="left">class_year</td></tr>
            <tr><td align="left">is_non_traditional</td></tr>
            <tr><td align="left">is_international</td></tr>
          </table>
        >];

        programs [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#FF7A59"><font color="white"><b>Programs</b></font></td></tr>
            <tr><td port="id" align="left"><u>program_id (PK)</u></td></tr>
            <tr><td align="left">program_name</td></tr>
          </table>
        >];

        bridge [label=<
          <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#D3D3D3"><font color="black"><b>Student_Programs</b></font></td></tr>
            <tr><td port="fk_stu" align="left">student_id (PK, FK)</td></tr>
            <tr><td port="fk_prog" align="left">program_id (PK, FK)</td></tr>
            <tr><td align="left">type</td></tr>
          </table>
        >];

        providers:id -> resources:fk_prov [label=" 1:M "];
        resources:id -> interactions:fk_res [label=" 1:M "];
        students:id -> interactions:fk_stu [label=" 1:M "];
        students:id -> bridge:fk_stu [label=" 1:M "];
        programs:id -> bridge:fk_prog [label=" 1:M "];
    }
    ''')

    st.markdown("#### Database Business Rules:")
    st.markdown("""
- **Students & Programs**: A Student can have many programs, and a Program can belong to many students. Therefore, they have a **many-to-many** relationship, and we place a bridge table (`student_programs`) between them.
- **Providers & Resources**: A Provider can provide many resources, but a Resource can only be provided by *one* provider. Therefore, the `provider_id` is in the `resources` table (linking it back to the provider), but the `resource_id` is *not* in the `providers` table.
- **Students & Resources**: A Student can log multiple interactions, and a Resource can be interacted with multiple times by different students. Therefore, `resource_interactions` connects them in a **many-to-many** relationship.
    """)

    st.markdown("---")
    st.subheader("1. Entity Justifications & Table Walkthrough")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Providers Table")
        st.markdown("**Design Choice**: One table for Departments, Centers, and Clubs.")
        st.markdown("**Justification**: Since a Department and a Club both have a name, a location, and offer resources, they share the same 'shape.' Using one table allows you to perform a single query to see every service provider on campus. The `provider_type` column preserves the distinction without the complexity of multiple identical tables.")
    with c2:
        st.code('''CREATE TABLE providers (
    provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    provider_type TEXT, -- e.g., 'Department', 'Center', 'Club'
    location TEXT,
    website TEXT,
    contact_email TEXT,
    contact_name TEXT   
);''', language='sql')

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Students Table")
        st.markdown("**Design Choice**: Use of Integers for Booleans.")
        st.markdown("**Justification**: SQLite does not have a native BOOLEAN type; it uses 0 and 1. This is a great teaching moment for storage efficiency.")
    with c2:
        st.code('''CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    dorm_name TEXT, -- e.g., 'Ecovillage', 'Danforth'
    class_year TEXT, -- 'Freshman', 'Sophomore', etc.
    is_non_traditional INTEGER DEFAULT 0, -- 0 for No, 1 for Yes
    is_international INTEGER DEFAULT 0
);''', language='sql')

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Programs & Student_Programs (The Bridge)")
        st.markdown("**Design Choice**: A separate table for the list of programs and a 'link' table.")
        st.markdown("**Justification**: This illustrates a **Many-to-Many (M:M)** relationship.")
        st.markdown("- One student can have multiple majors/minors.")
        st.markdown("- One major (e.g., Computer Science) has many students.")
        st.markdown("By using a bridge table, we avoid messy comma-separated lists in the students table, making it easy to count exactly how many 'Senior Physics Majors' exist with one simple JOIN.")
    with c2:
        st.code('''CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name TEXT NOT NULL UNIQUE
);

CREATE TABLE student_programs (
    student_id INTEGER,
    program_id INTEGER,
    type TEXT NOT NULL, -- 'Major' or 'Minor'
    PRIMARY KEY (student_id, program_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);''', language='sql')

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Resources Table")
        st.markdown("**Design Choice**: Including `req_` columns (Eligibility Attributes).")
        st.markdown("**Justification**: This moves the 'business logic' into the data. Instead of writing a new SQL query every time a resource changes its rules, the user just updates a row in the table.")
        st.markdown("**Foreign Key**: The `provider_id` creates a **One-to-Many (1:M)** relationship. One department provides many resources, but each resource belongs to one department.")
    with c2:
        st.code('''CREATE TABLE resources (
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
);''', language='sql')

    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Resource Interactions Log")
        st.markdown("Logs exactly when a student accesses or requests a resource.")
        st.markdown("Connects **Students** and **Resources** through a many-to-many relationship.")
    with c2:
        st.code('''CREATE TABLE resource_interactions (
    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    interaction_date TEXT DEFAULT (CURRENT_DATE), -- Auto-fills with 'YYYY-MM-DD'
    notes TEXT,
    
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);''', language='sql')

    st.markdown("---")
    st.subheader("2. Data Type Notes for your Workshop")
    st.markdown("""
- **`INTEGER PRIMARY KEY AUTOINCREMENT`**: This ensures every row has a unique "ID card" number that the database manages automatically.
- **`TEXT` for Dates**: Remind students that SQLite sorts dates correctly only if they are in `YYYY-MM-DD` format.
- **`NULL` vs. `NOT NULL`**: In the `student_programs` table, we don't need a "Minor" column in the student table that stays empty (`NULL`) for most people. If they don't have a minor, there is simply no row in the bridge table. This is **Normalization** at work - only storing data that actually exists.

By adding columns like `req_non_trad_only` (Boolean) to the resources table, the data tells the story.

**The Power of this approach**: You can write one "Smart Query" that works for any student!
    """)
    
    st.markdown("---")
    st.subheader("3. Why not just a 'List' of Majors?")
    st.markdown('In database terms, putting a list of values (like "Biology, Chemistry") into a single cell is called a **Multi-valued Attribute**.')
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### The 'List' Approach (The Easy Way)")
        st.markdown("**Pros**: It's easy to read when looking at the whole table. The schema stays 'thin' with fewer tables.")
        st.markdown("**Cons**:")
        st.markdown("- **Violates First Normal Form (1NF)**.")
        st.markdown("- **Searching is hard**: If you want to find all 'Biology' majors, you can't just say `WHERE major = 'Biology'`. You have to use `LIKE '%Biology%'`, which is much slower and can lead to 'false positives' (e.g., finding 'Microbiology' when searching for 'Biology').")
        st.markdown("- **Updates are messy**: If a student drops one of three majors, you have to write code to string-manipulate that specific cell to 'snipe' out the correct word.")
        st.markdown("- **Data Integrity**: There's no way to prevent a typo like 'Bilogy' because it's just a text blob.")
    
    with colB:
        st.markdown("#### The 'Bridge Table' (The Professional Way)")
        st.markdown("**Justification**: This is a Many-to-Many relationship. By having a `student_programs` table, each 'connection' is its own row.")
        st.markdown("**Workshop Takeaway**: This allows you to teach Joins. To get a student's majors, you join the student to the bridge table. This is the 'standard' way to handle any situation where 'one X can have many Ys, and one Y can have many Xs.'")


def sql_editor_view(conn):
    st.header("SQL Playground")
    st.write("Write and execute your own SQL queries against the database in real time.")
    
    with st.expander("📖 SQL Quick Lesson: From Basics to Advanced", expanded=False):
        st.markdown("""
        ### 1. The Basics: SELECT
        The `SELECT` statement is the most common command in SQL. It fetches data from a database.
        - **Fetch everything in a table:** 
          `SELECT * FROM students;`
        - **Fetch specific columns:** 
          `SELECT full_name, email FROM students;`

        ### 2. Filtering Data: WHERE
        Use `WHERE` to narrow down your results based on specific conditions.
        - **Simple condition:** 
          `SELECT * FROM students WHERE class_year = 'Senior';`
        - **Multiple conditions:** 
          `SELECT * FROM students WHERE class_year = 'Senior' AND is_non_traditional = 1;`

        ### 3. Sorting Data: ORDER BY
        Use `ORDER BY` to sort your results.
        - **Sort alphabetically:** 
          `SELECT * FROM students ORDER BY full_name ASC;`
        - **Sort by recent dates:** 
          `SELECT * FROM resource_interactions ORDER BY interaction_date DESC;`

        ### 4. Counting & Math: COUNT, LIMIT
        - **Limit results to top 5:** 
          `SELECT * FROM resources LIMIT 5;`
        - **Count the number of students:** 
          `SELECT COUNT(*) FROM students;`

        ### 5. Combining Tables: JOIN
        Databases spread data across multiple tables. Use `JOIN` to bring them together using the lines that connect them.
        - **See Provider names alongside their Resources:**
          ```sql
          SELECT providers.name, resources.title 
          FROM resources 
          JOIN providers ON resources.provider_id = providers.provider_id;
          ```
        *Tip: You use `ON` to tell the database which columns match up between the two tables!*
        
        ### 6. Aggregating: GROUP BY
        Use `GROUP BY` to group rows that have the same values into summary rows, often paired with `COUNT`.
        - **Count how many students live in each dorm:**
          ```sql
          SELECT dorm_name, COUNT(*) as student_count 
          FROM students 
          GROUP BY dorm_name;
          ```
        """)
    
    query = st.text_area("SQL Query", height=150, placeholder="SELECT * FROM students;")
    
    if st.button("Execute Query"):
        if query.strip():
            try:
                # If it's a SELECT query, we want to return a dataframe
                if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                    df = pd.read_sql_query(query, conn)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.success(f"Query returned {len(df)} rows.")
                else:
                    # For INSERT, UPDATE, DELETE, CREATE, ALTER
                    cursor = conn.cursor()
                    cursor.executescript(query) # Using executescript to allow multiple statements
                    conn.commit()
                    st.success("Query executed successfully!")
            except Exception as e:
                st.error(f"SQL Error: {e}")
        else:
            st.warning("Please enter a SQL query.")

def analysis_insights_view(conn):
    st.header("Data Analysis & Ethical Insights")
    st.write("This page demonstrates the results of our Data Analysis queries. By comparing the baseline demographics of our campus against the interaction rates at specific resources, we can uncover potential systemic barriers or hidden biases.")

    # 1. International Student Bias
    st.subheader("1. Drop-In Writing Tutoring: International Student Discrepancy")
    with st.expander("Show SQL Command"):
        st.code("""SELECT r.title, s.is_international, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (SELECT COUNT(*) AS total FROM resource_interactions WHERE resource_id = 4) AS total
WHERE ri.resource_id = 4
GROUP BY s.is_international, r.title;""", language="sql")
    
    query1 = """SELECT r.title, s.is_international, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (SELECT COUNT(*) AS total FROM resource_interactions WHERE resource_id = 4) AS total
WHERE ri.resource_id = 4
GROUP BY s.is_international, r.title;"""
    try:
        df1 = pd.read_sql_query(query1, conn)
        st.dataframe(df1, use_container_width=True, hide_index=True)
        st.info("**Conclusion:** International students generally make up ~20% of the baseline student population, yet this data shows they have disproportionately low representation at Drop-In Writing Tutoring. This suggests a systemic barrier—perhaps the tutoring center is mainly advertised through domestic-focused channels, or students feel the service isn't designed for ESL (English as a Second Language) learners.")
    except Exception as e:
        st.error(f"Error loading query: {e}")

    # 2. Non-Traditional Student Bias
    st.subheader("2. Free Flu Vaccine Clinic: Non-Traditional Student Isolation")
    with st.expander("Show SQL Command"):
        st.code("""-- Query resource 30 comparing non_traditional status
SELECT r.title, s.is_non_traditional, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri ...""", language="sql")
    
    query2 = """SELECT r.title, s.is_non_traditional, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (SELECT COUNT(*) AS total FROM resource_interactions WHERE resource_id = 30) AS total
WHERE ri.resource_id = 30
GROUP BY s.is_non_traditional, r.title;"""
    try:
        df2 = pd.read_sql_query(query2, conn)
        st.dataframe(df2, use_container_width=True, hide_index=True)
        st.info("**Conclusion:** Non-traditional students make up ~10% of the campus base, but representation at the Free Flu Vaccine Clinic is extremely low. Given that non-traditional students often commute, have full-time jobs, or support families, scheduling a clinic during standard daytime work hours inherently excludes them. Offering weekend or evening hours might resolve this discrepancy.")
    except Exception as e:
        st.error(f"Error loading query: {e}")

    # 3. Dorm Isolation
    st.subheader("3. Sunday Evening Dinner: Geographic/Dorm Isolation")
    with st.expander("Show SQL Command"):
        st.code("""-- Analyzing Resource 18 (Sunday Evening Dinner) representation by dorm...
SELECT r.title, s.dorm_name, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri ...""", language="sql")
    
    query3 = """SELECT r.title, s.dorm_name, COUNT(ri.interaction_id) AS interaction_count,
    ROUND(COUNT(ri.interaction_id) * 100.0 / total.total, 2) AS percentage_of_turnout
FROM resource_interactions ri
JOIN students s ON ri.student_id = s.student_id
JOIN resources r ON ri.resource_id = r.resource_id
CROSS JOIN (SELECT COUNT(*) AS total FROM resource_interactions WHERE resource_id = 18) AS total
WHERE ri.resource_id = 18
GROUP BY s.dorm_name, r.title
ORDER BY interaction_count DESC;"""
    try:
        df3 = pd.read_sql_query(query3, conn)
        st.dataframe(df3, use_container_width=True, hide_index=True)
        st.info("**Conclusion:** The 'Sunday Evening Dinner' shows healthy turnout from most dorms, except for residents of the 'Draper' dorm. This highlights a likely geographic or logistical issue. Perhaps Draper is located off the main campus and lacks a late Sunday bus route, making it unsafe or impossible for residents to attend the event.")
    except Exception as e:
        st.error(f"Error loading query: {e}")


def main():
    st.set_page_config(page_title="Campus Hub", layout="wide")
    
    # Check if DB exists, if not sqlite3 connect will create an empty one
    conn = sqlite3.connect("campus_resources.db", check_same_thread=False)
    
    st.sidebar.title("Navigation")
    route = st.sidebar.radio("Go to", ["Home", "Student View", "Log Interaction", "Admin Dashboard", "Schema Explained", "SQL Playground", "Analysis Insights"])
    
    if route == "Home":
        st.title("Welcome to the Campus Hub UI")
        st.markdown("""
        This dashboard serves as a graphical interface over the `campus_resources.db` SQLite database.
        
        Using the navigation menu on the left, you can explore the database from different perspectives:
        - **Student View:** See how individual profiles alter what data is surfaced to them based on logic in the `resources` table.
        - **Log Interaction:** Let front-desk staff log into the `resource_interactions` table smoothly.
        - **Admin Dashboard:** Monitor the raw tables and insert new data directly.
        - **Schema Explained:** Check out the data models and design choices.
        """)
        
        st.info("To manually run SQL script files or completely reset the database, use the terminal.")
        
    elif route == "Student View":
        student_view(conn)
    elif route == "Log Interaction":
        log_interaction(conn)
    elif route == "Admin Dashboard":
        admin_view(conn)
    elif route == "Schema Explained":
        schema_explained_view()
    elif route == "SQL Playground":
        sql_editor_view(conn)
    elif route == "Analysis Insights":
        analysis_insights_view(conn)
        
    conn.close()

if __name__ == "__main__":
    main()
