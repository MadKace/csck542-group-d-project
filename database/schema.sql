-- Drop existing tables
DROP TABLE IF EXISTS research_project_member;
DROP TABLE IF EXISTS programme_course;
DROP TABLE IF EXISTS course_prerequisite;
DROP TABLE IF EXISTS lecturer_course;
DROP TABLE IF EXISTS student_course;
DROP TABLE IF EXISTS project_outcome;
DROP TABLE IF EXISTS project_publication;
DROP TABLE IF EXISTS project_funding;
DROP TABLE IF EXISTS department_research_area;
DROP TABLE IF EXISTS course_material;
DROP TABLE IF EXISTS publication;
DROP TABLE IF EXISTS lecturer_research_interest;
DROP TABLE IF EXISTS lecturer_expertise;
DROP TABLE IF EXISTS lecturer_qualification;
DROP TABLE IF EXISTS student_grade;
DROP TABLE IF EXISTS disciplinary_record;
DROP TABLE IF EXISTS research_project;
DROP TABLE IF EXISTS non_academic_staff;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS lecturer;
DROP TABLE IF EXISTS programme;
DROP TABLE IF EXISTS department;

-- Enable foreign key enforcement
PRAGMA foreign_keys = ON;

CREATE TABLE department (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    faculty TEXT
);

CREATE TABLE programme (
    programme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    degree_awarded TEXT,
    duration_years INTEGER CHECK (duration_years > 0),
    enrolment_details TEXT
);

CREATE TABLE lecturer (
    lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    course_load INTEGER,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    programme_id INTEGER NOT NULL,
    advisor_id INTEGER,
    name TEXT NOT NULL,
    date_of_birth DATE,
    contact_info TEXT,
    year_of_study INTEGER CHECK (year_of_study > 0),
    graduation_status TEXT,
    FOREIGN KEY (programme_id) REFERENCES programme(programme_id),
    FOREIGN KEY (advisor_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    course_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    level TEXT,
    credits INTEGER CHECK (credits > 0),
    schedule TEXT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE non_academic_staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    name TEXT NOT NULL,
    job_title TEXT,
    employment_type TEXT,
    contract_details TEXT,
    salary REAL CHECK (salary >= 0),
    emergency_contact TEXT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE research_project (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    head_lecturer_id INTEGER NOT NULL UNIQUE,
    dept_id INTEGER,
    title TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (head_lecturer_id) REFERENCES lecturer(lecturer_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE disciplinary_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    incident_date DATE,
    description TEXT,
    action_taken TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE student_grade (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    assessment_type TEXT,
    grade INTEGER CHECK (grade >= 0 AND grade <= 100),
    date_recorded DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE lecturer_qualification (
    qualification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER NOT NULL,
    qualification_name TEXT NOT NULL,
    institution TEXT,
    year_awarded INTEGER,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_expertise (
    expertise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER NOT NULL,
    area TEXT NOT NULL,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_research_interest (
    interest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER NOT NULL,
    interest TEXT NOT NULL,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE publication (
    publication_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    journal TEXT,
    publication_date DATE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course_material (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    material_type TEXT,
    url TEXT,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE department_research_area (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL,
    area TEXT NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE project_funding (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,
    amount REAL CHECK (amount >= 0),
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_publication (
    project_pub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    publication_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_outcome (
    outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    description TEXT NOT NULL,
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

CREATE TABLE programme_course (
    programme_id INTEGER,
    course_id INTEGER,
    is_required INTEGER DEFAULT 1,
    PRIMARY KEY (programme_id, course_id),
    FOREIGN KEY (programme_id) REFERENCES programme(programme_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE research_project_member (
    project_id INTEGER,
    student_id INTEGER,
    PRIMARY KEY (project_id, student_id),
    FOREIGN KEY (project_id) REFERENCES research_project(project_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

-- Indexes on foreign keys to improve join performance
CREATE INDEX idx_student_programme ON student(programme_id);
CREATE INDEX idx_student_advisor ON student(advisor_id);
CREATE INDEX idx_lecturer_dept ON lecturer(dept_id);
CREATE INDEX idx_course_dept ON course(dept_id);
CREATE INDEX idx_student_grade_student ON student_grade(student_id);
CREATE INDEX idx_student_grade_course ON student_grade(course_id);
CREATE INDEX idx_publication_lecturer ON publication(lecturer_id);
CREATE INDEX idx_research_project_dept ON research_project(dept_id);
