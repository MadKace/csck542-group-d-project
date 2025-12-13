"""Generate seed data using Faker.

Usage:
    python scripts/generate_seed_data.py
"""

from pathlib import Path

from faker import Faker

fake = Faker(["en_GB", "en_US", "en_IN", "es", "it", "fr_FR"])
Faker.seed(42)


def sql(value: str | None) -> str:
    """Format a value for SQL."""
    if value is None:
        return "NULL"
    return f"'{value.replace(chr(39), chr(39)+chr(39))}'"


def generate_sql() -> str:
    """Generate SQL insert statements."""
    lines = ["-- Seed data generated using Faker library", ""]

    # Departments
    departments = [
        ("Computer Science", "Science and Engineering"),
        ("Mathematics", "Science and Engineering"),
        ("Physics", "Science and Engineering"),
        ("English", "Arts and Humanities"),
        ("Business", "Business School"),
    ]
    for name, faculty in departments:
        lines.append(
            f"INSERT INTO department (name, faculty) "
            f"VALUES ({sql(name)}, {sql(faculty)});"
        )
    lines.append("")

    # Programmes
    programmes = [
        ("BSc Computer Science", "BSc", 3),
        ("MSc Computer Science", "MSc", 1),
        ("MSc Data Science", "MSc", 1),
        ("BA English Literature", "BA", 3),
        ("MBA Business Administration", "MBA", 2),
        ("BSc Mathematics", "BSc", 3),
        ("PhD Computer Science", "PhD", 4),
    ]
    for name, degree, years in programmes:
        lines.append(
            f"INSERT INTO programme (name, degree_awarded, duration_years) "
            f"VALUES ({sql(name)}, {sql(degree)}, {years});"
        )
    lines.append("")

    # Lecturers (10)
    lines.append("-- Lecturers")
    for i in range(10):
        name = f"Dr {fake.name()}"
        dept_id = (i % 5) + 1
        lines.append(
            f"INSERT INTO lecturer (dept_id, name, course_load) "
            f"VALUES ({dept_id}, {sql(name)}, 3);"
        )
    lines.append("")

    # Students (20)
    lines.append("-- Students")
    for i in range(20):
        name = fake.name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=25)
        email = fake.email()
        prog_id = (i % 7) + 1
        advisor_id = (i % 10) + 1
        year = (i % 4) + 1
        lines.append(
            f"INSERT INTO student (programme_id, advisor_id, name, "
            f"date_of_birth, contact_info, year_of_study, graduation_status) "
            f"VALUES ({prog_id}, {advisor_id}, {sql(name)}, '{dob}', "
            f"{sql(email)}, {year}, 'enrolled');"
        )
    lines.append("")

    # Courses
    courses = [
        (1, "CS101", "Introduction to Programming", "Undergraduate", 15),
        (1, "CS201", "Data Structures", "Undergraduate", 15),
        (1, "CS301", "Databases and Information Systems", "Undergraduate", 15),
        (1, "CS401", "Machine Learning", "Postgraduate", 20),
        (2, "MA101", "Calculus", "Undergraduate", 15),
        (2, "MA201", "Linear Algebra", "Undergraduate", 15),
        (3, "PH101", "Classical Mechanics", "Undergraduate", 15),
        (4, "EN101", "Introduction to Literature", "Undergraduate", 15),
        (5, "BA101", "Principles of Management", "Undergraduate", 15),
        (5, "BA201", "Financial Accounting", "Undergraduate", 15),
    ]
    for dept_id, code, name, level, credits in courses:
        lines.append(
            f"INSERT INTO course (dept_id, course_code, name, level, credits) "
            f"VALUES ({dept_id}, {sql(code)}, {sql(name)}, {sql(level)}, {credits});"
        )
    lines.append("")

    # Non-academic staff (5)
    lines.append("-- Non-academic staff")
    jobs = ["Admin Assistant", "Lab Technician", "IT Support", "HR Officer", "Finance"]
    for i in range(5):
        name = fake.name()
        lines.append(
            f"INSERT INTO non_academic_staff (dept_id, name, job_title, "
            f"employment_type, salary) VALUES ({i + 1}, {sql(name)}, "
            f"{sql(jobs[i])}, 'full-time', 35000);"
        )
    lines.append("")

    # Research projects (3)
    lines.append("-- Research projects")
    projects = [
        (1, 1, "Neural Network Architectures"),
        (2, 1, "Sustainable Computing"),
        (3, 2, "Applied Statistics"),
    ]
    for head_id, dept_id, title in projects:
        lines.append(
            f"INSERT INTO research_project (head_lecturer_id, dept_id, title, "
            f"start_date, end_date) VALUES ({head_id}, {dept_id}, {sql(title)}, "
            f"'2024-01-01', '2025-12-31');"
        )
    lines.append("")

    # Lecturer qualifications
    lines.append("-- Lecturer qualifications")
    unis = ["University of Liverpool", "University of Oxford", "UCL", "Imperial",
            "Cambridge", "Edinburgh", "Manchester", "Bristol", "Warwick", "Glasgow"]
    for i in range(10):
        lines.append(
            f"INSERT INTO lecturer_qualification (lecturer_id, qualification_name, "
            f"institution, year_awarded) VALUES ({i + 1}, 'PhD', {sql(unis[i])}, 2015);"
        )
    lines.append("")

    # Lecturer expertise
    lines.append("-- Lecturer expertise")
    areas = ["Machine Learning", "Databases", "Networks", "Security", "AI",
             "Algebra", "Statistics", "Quantum", "Literature", "Finance"]
    for i in range(10):
        lines.append(
            f"INSERT INTO lecturer_expertise (lecturer_id, area) "
            f"VALUES ({i + 1}, {sql(areas[i])});"
        )
    lines.append("")

    # Student-course enrolments (each student in 3 courses)
    lines.append("-- Student enrolments")
    for student_id in range(1, 21):
        for course_id in range(1, 4):
            lines.append(
                f"INSERT INTO student_course (student_id, course_id, semester) "
                f"VALUES ({student_id}, {course_id}, 'Autumn 2024');"
            )
    lines.append("")

    # Lecturer-course assignments
    lines.append("-- Lecturer assignments")
    for course_id in range(1, 11):
        lecturer_id = ((course_id - 1) % 10) + 1
        lines.append(
            f"INSERT INTO lecturer_course (lecturer_id, course_id) "
            f"VALUES ({lecturer_id}, {course_id});"
        )
    lines.append("")

    # Student grades
    lines.append("-- Student grades")
    for student_id in range(1, 21):
        for course_id in range(1, 4):
            grade = 50 + (student_id * 2) % 40
            lines.append(
                f"INSERT INTO student_grade (student_id, course_id, "
                f"assessment_type, grade, date_recorded) VALUES "
                f"({student_id}, {course_id}, 'exam', {grade}, '2024-12-01');"
            )
    lines.append("")

    # Programme-course mappings
    lines.append("-- Programme courses")
    prog_courses = [(1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (6, 5), (6, 6)]
    for prog_id, course_id in prog_courses:
        lines.append(
            f"INSERT INTO programme_course (programme_id, course_id, is_required) "
            f"VALUES ({prog_id}, {course_id}, 1);"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Generate and write seed data."""
    output = Path(__file__).parent.parent / "database" / "seed_data.sql"
    output.write_text(generate_sql(), encoding="utf-8")
    print(f"Written to: {output}")


if __name__ == "__main__":
    main()
