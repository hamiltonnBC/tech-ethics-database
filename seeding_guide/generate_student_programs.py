import random
import os

TOTAL_STUDENTS = 1000
PROGRAM_IDS = list(range(1, 26))

student_ids = list(range(1, TOTAL_STUDENTS + 1))
random.shuffle(student_ids)

# Distributions
# 20: triple majors
# 200: double majors
# 300: 1 major + 1 minor (from the pool that only has 1 major)
# remaining 480: 1 major only
triple_majors = student_ids[:20]
double_majors = student_ids[20:220]
single_major_with_minor = student_ids[220:520]
single_major_only = student_ids[520:]

records = []

def assign_programs(student_id, num_majors, num_minors):
    chosen_programs = random.sample(PROGRAM_IDS, num_majors + num_minors)
    majors = chosen_programs[:num_majors]
    minors = chosen_programs[num_majors:]
    
    for major_id in majors:
        records.append((student_id, major_id, 'Major'))
    for minor_id in minors:
        records.append((student_id, minor_id, 'Minor'))

for sid in triple_majors:
    assign_programs(sid, 3, 0)
for sid in double_majors:
    assign_programs(sid, 2, 0)
for sid in single_major_with_minor:
    assign_programs(sid, 1, 1)
for sid in single_major_only:
    assign_programs(sid, 1, 0)

# Sort by student_id to group records visually together for the same student
records.sort(key=lambda x: x[0])

# Convert tuples to SQL syntax
sql_values = [f"({r[0]}, {r[1]}, '{r[2]}')" for r in records]

sql_content = "-- 2B: Insert Student Programs (Relies on 'students' and 'programs')\n"
sql_content += "INSERT INTO student_programs (student_id, program_id, type) VALUES\n"
sql_content += ",\n".join(sql_values) + ";\n"

# Output explicitly to 2b_insert_student_programs.sql
output_path = os.path.join(os.path.dirname(__file__), "2b_insert_student_programs.sql")
with open(output_path, "w") as f:
    f.write(sql_content)

print(f"Successfully generated {len(records)} student-program associations for 1000 students.")
