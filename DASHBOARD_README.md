# Launching the Interactive UI Dashboard

Welcome to the Tech Ethics Database Dashboard window! This UI is built entirely in Python using **Streamlit** and relies on **uv** as an ultra-fast package manager. Using `uv`, you don't even need to worry about manually installing Python or setting up Virtual Environments. It handles standardizing all requirements across both Windows and Mac seamlessly!

## Step 1: Install `uv`
If you do not have `uv` installed, you will need it first. `uv` is a blazing fast package manager written in Rust.

**Windows (PowerShell):**
Open PowerShell (as Administrator if possible, or standard user if Bypass is allowed) and run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac / Linux / WSL:**
Open your terminal and run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

*(Note: You may need to restart your terminal or close and reopen it after installing `uv` so it registers the command!)*

## Step 2: Seed the Database
Before running the dashboard, the application expects `campus_resources.db` to have some data! Ensure you have followed the main SQL Workshop and run our seeding scripts:
1. Open your terminal at the root of the repository.
2. Run this command to build the tables: 
   ```bash
   sqlite3 campus_resources.db ".read create_tables.sql"
   ```
3. Run this command to fill them with dummy data: 
   ```bash
   sqlite3 campus_resources.db ".read seeding_guide/seed_all.sql"
   ```

## Step 3: Run the Application!
Now that `uv` is installed and the database is ready, running the application is a single command. 

Ensure your terminal is opened in this repository folder, and run:

```bash
uvx --from streamlit streamlit run dashboard.py
```

`uv` will automatically download Python (if needed), install the necessary requirements (Streamlit and Pandas) in an isolated pocket, and securely spin up a local web server!

Once the command finishes, it should automatically open a port locally in your default web browser (usually at `http://localhost:8501`).

### What's happening behind the scenes?
If you open `dashboard.py` and look at the top, you'll see a special block of code:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "streamlit",
#     "pandas",
# ]
# ///
```
This is **inline script metadata**. `uv` reads this block, figures out exactly what dependencies the Python script needs to run, downloads them transparently into an ephemeral cache, and flawlessly executes it for you without leaving messy global packages installed on your laptop! Easy!
