import random
import os

# We want 1000 students
TOTAL_STUDENTS = 1000

# Names database
first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Oliver", "Isabella", "Elijah", "Sophia", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Harper", "Henry", "Evelyn", "Alexander", "Abigail", "Michael", "Emily", "Ethan", "Elizabeth", "Daniel", "Mila", "Matthew", "Ella", "Aiden", "Avery", "Joseph", "Sofia", "Jackson", "Camila", "Samuel", "Aria", "Sebastian", "Scarlett", "David", "Victoria", "Carter", "Madison", "Wyatt", "Luna", "Jayden", "Grace", "John", "Chloe", "Owen", "Penelope", "Dylan", "Layla", "Luke", "Riley", "Gabriel", "Zoey", "Anthony", "Nora", "Isaac", "Lily", "Grayson", "Eleanor", "Jack", "Hannah", "Julian", "Lillian", "Levi", "Addison", "Christopher", "Aubrey", "Joshua", "Ellie", "Andrew", "Stella", "Lincoln", "Natalie", "Mateo", "Zoe", "Ryan", "Leah", "Jaxon", "Hazel", "Nathan", "Violet", "Aaron", "Aurora", "Isaiah", "Savannah", "Thomas", "Audrey", "Charles", "Brooklyn", "Caleb", "Bella", "Josiah", "Claire", "Christian", "Skylar", "Hunter"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"]
domains = ["campus.edu", "student.campus.edu"]
dorms_options = ["Draper", "Pearsons", "MAC", "Seabury", "Off Campus"]

# Prepare balanced values
# 250 of each class year
class_years = ["first year"] * 250 + ["second year"] * 250 + ["third year"] * 250 + ["fourth year"] * 250

# Demographics logic
# 20 students: BOTH non traditional (1) and international (1)
# 80 students: ONLY non traditional (1) and not international (0) -- total 100 non trad
# 180 students: ONLY international (1) and not non traditional (0)  -- total 200 intl
# 720 students: NEITHER (0, 0)
flags = [(1, 1)] * 20 + [(1, 0)] * 80 + [(0, 1)] * 180 + [(0, 0)] * 720

# Shuffle them so they're randomly distributed 
random.shuffle(class_years)
random.shuffle(flags)

students = []
used_emails = set()
off_campus_nontrad_count = 0

for i in range(TOTAL_STUDENTS):
    while True:
        first = random.choice(first_names)
        last = random.choice(last_names)
        domain = random.choice(domains)
        email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@{domain}"
        if email not in used_emails:
            used_emails.add(email)
            break
            
    full_name = f"{first} {last}"
    c_year = class_years[i]
    n_trad, intl = flags[i]
    
    if n_trad == 1 and intl == 0:
        if off_campus_nontrad_count < 15:
            dorm = "Off Campus"
            off_campus_nontrad_count += 1
        else:
            dorm = "Ecovillage"
    elif n_trad == 1 and intl == 1:
        dorm = "Ecovillage"
    else:
        dorm = random.choice(["Draper", "Pearsons", "MAC", "Seabury", "Off Campus"])
    
    # Create the SQL row string
    row = f"('{full_name}', '{email}', '{dorm}', '{c_year}', {n_trad}, {intl})"
    students.append(row)

# Combine them into a single SQL block
sql_content = "-- 1B: Insert Students (Independent Table)\n"
sql_content += "INSERT INTO students (full_name, email, dorm_name, class_year, is_non_traditional, is_international) VALUES\n"
sql_content += ",\n".join(students) + ";\n"

# Output to target file
output_path = os.path.join(os.path.dirname(__file__), "1b_insert_students.sql")
with open(output_path, "w") as f:
    f.write(sql_content)

print(f"Successfully generated {TOTAL_STUDENTS} students and saved to {output_path}")
