-- Enable foreign key enforcement
PRAGMA foreign_keys = ON;

CREATE TABLE department (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    faculty TEXT
);

CREATE TABLE program (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    degree_awarded TEXT,
    duration_years INTEGER,
    enrolment_details TEXT
);

CREATE TABLE lecturer (
    lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    name TEXT,
    course_load INTEGER,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER,
    advisor_id INTEGER,
    name TEXT,
    date_of_birth DATE,
    contact_info TEXT,
    year_of_study INTEGER,
    graduation_status TEXT,
    FOREIGN KEY (program_id) REFERENCES program(program_id),
    FOREIGN KEY (advisor_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    course_code TEXT,
    name TEXT,
    description TEXT,
    level TEXT,
    credits INTEGER,
    schedule TEXT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE non_academic_staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    name TEXT,
    job_title TEXT,
    employment_type TEXT,
    contract_details TEXT,
    salary REAL,
    emergency_contact TEXT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE research_project (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    head_lecturer_id INTEGER UNIQUE,
    dept_id INTEGER,
    title TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (head_lecturer_id) REFERENCES lecturer(lecturer_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE disciplinary_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    incident_date DATE,
    description TEXT,
    action_taken TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE student_grade (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    assessment_type TEXT,
    grade INTEGER,
    date_recorded DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE lecturer_qualification (
    qualification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER,
    qualification_name TEXT,
    institution TEXT,
    year_awarded INTEGER,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_expertise (
    expertise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER,
    area TEXT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_research_interest (
    interest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER,
    interest TEXT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE publication (
    publication_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER,
    title TEXT,
    journal TEXT,
    publication_date DATE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course_material (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    title TEXT,
    material_type TEXT,
    url TEXT,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE department_research_area (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    area TEXT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE project_funding (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    source_name TEXT,
    amount REAL,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_publication (
    project_pub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    title TEXT,
    publication_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_outcome (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    description TEXT,
    outcome_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE student_course (
    student_id INTEGER,
    course_id INTEGER,
    semester TEXT,
    enrolment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE lecturer_course (
    lecturer_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (lecturer_id, course_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE course_prerequisite (
    course_id INTEGER,
    prerequisite_id INTEGER,
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (prerequisite_id) REFERENCES course(course_id)
);

CREATE TABLE program_course (
    program_id INTEGER,
    course_id INTEGER,
    is_required INTEGER,
    PRIMARY KEY (program_id, course_id),
    FOREIGN KEY (program_id) REFERENCES program(program_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE research_project_member (
    project_id INTEGER,
    student_id INTEGER,
    PRIMARY KEY (project_id, student_id),
    FOREIGN KEY (project_id) REFERENCES research_project(project_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

