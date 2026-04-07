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

def main():
    st.set_page_config(page_title="Campus Hub", layout="wide")
    
    # Check if DB exists, if not sqlite3 connect will create an empty one
    conn = sqlite3.connect("campus_resources.db", check_same_thread=False)
    
    st.sidebar.title("Navigation")
    route = st.sidebar.radio("Go to", ["Home", "Student View", "Log Interaction", "Admin Dashboard"])
    
    if route == "Home":
        st.title("Welcome to the Campus Hub UI")
        st.markdown("""
        This dashboard serves as a graphical interface over the `campus_resources.db` SQLite database.
        
        Using the navigation menu on the left, you can explore the database from different perspectives:
        - **Student View:** See how individual profiles alter what data is surfaced to them based on logic in the `resources` table.
        - **Log Interaction:** Let front-desk staff log into the `resource_interactions` table smoothly.
        - **Admin Dashboard:** Monitor the raw tables and insert new data directly.
        """)
        
        st.info("To manually run SQL script files or completely reset the database, use the terminal.")
        
    elif route == "Student View":
        student_view(conn)
    elif route == "Log Interaction":
        log_interaction(conn)
    elif route == "Admin Dashboard":
        admin_view(conn)
        
    conn.close()

if __name__ == "__main__":
    main()
