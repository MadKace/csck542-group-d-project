CREATE TABLE department (
    dept_id INT PRIMARY KEY,
    name VARCHAR(100),
    faculty VARCHAR(100)
);

CREATE TABLE program (
    program_id INT PRIMARY KEY,
    name VARCHAR(100),
    degree_awarded VARCHAR(50),
    duration_years INT,
    enrolment_details VARCHAR
);

CREATE TABLE lecturer (
    lecturer_id INT PRIMARY KEY,
    dept_id INT,
    name VARCHAR(100),
    course_load INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE student (
    student_id INT PRIMARY KEY,
    program_id INT,
    advisor_id INT,
    name VARCHAR(100),
    date_of_birth DATE,
    contact_info VARCHAR(200),
    year_of_study INT,
    graduation_status VARCHAR,
    FOREIGN KEY (program_id) REFERENCES program(program_id),
    FOREIGN KEY (advisor_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course (
    course_id INT PRIMARY KEY,
    dept_id INT,
    course_code VARCHAR(20),
    name VARCHAR(100),
    description VARCHAR(500),
    level VARCHAR(50),
    credits INT,
    schedule VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE non_academic_staff (
    staff_id INT PRIMARY KEY,
    dept_id INT,
    name VARCHAR(100),
    job_title VARCHAR(100),
    employment_type VARCHAR(50),
    contract_details VARCHAR,
    salary DECIMAL(10,2),
    emergency_contact VARCHAR,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE research_project (
    project_id INT PRIMARY KEY,
    head_lecturer_id INT,
    dept_id INT,
    title VARCHAR(200),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (head_lecturer_id) REFERENCES lecturer(lecturer_id),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE disciplinary_record (
    record_id INT PRIMARY KEY,
    student_id INT,
    incident_date DATE,
    description VARCHAR(500),
    action_taken VARCHAR(200),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE student_grade (
    grade_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    assessment_type VARCHAR(50),
    grade INT,
    date_recorded DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE lecturer_qualification (
    qualification_id INT PRIMARY KEY,
    lecturer_id INT,
    qualification_name VARCHAR,
    institution VARCHAR(100),
    year_awarded INT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_expertise (
    expertise_id INT PRIMARY KEY,
    lecturer_id INT,
    area VARCHAR(100),
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE lecturer_research_interest (
    interest_id INT PRIMARY KEY,
    lecturer_id INT,
    interest VARCHAR(100),
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE publication (
    publication_id INT PRIMARY KEY,
    lecturer_id INT,
    title VARCHAR(300),
    journal VARCHAR(200),
    publication_date DATE,
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id)
);

CREATE TABLE course_material (
    material_id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(200),
    material_type VARCHAR(50),
    url VARCHAR(500),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE department_research_area (
    area_id INT PRIMARY KEY,
    dept_id INT,
    area VARCHAR(100),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

CREATE TABLE project_funding (
    funding_id INT PRIMARY KEY,
    project_id INT,
    source_name VARCHAR(100),
    amount DECIMAL(12,2),
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_publication (
    project_pub_id INT PRIMARY KEY,
    project_id INT,
    title VARCHAR(300),
    publication_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE project_outcome (
    outcome_id INT PRIMARY KEY,
    project_id INT,
    description VARCHAR(500),
    outcome_date DATE,
    FOREIGN KEY (project_id) REFERENCES research_project(project_id)
);

CREATE TABLE student_course (
    student_id INT,
    course_id INT,
    semester VARCHAR(20),
    enrolment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE lecturer_course (
    lecturer_id INT,
    course_id INT,
    PRIMARY KEY (lecturer_id, course_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(lecturer_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE course_prerequisite (
    course_id INT,
    prerequisite_id INT,
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (prerequisite_id) REFERENCES course(course_id)
);

CREATE TABLE program_course (
    program_id INT,
    course_id INT,
    is_required BOOLEAN,
    PRIMARY KEY (program_id, course_id),
    FOREIGN KEY (program_id) REFERENCES program(program_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE research_project_member (
    group_id INT,
    student_id INT,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES research_project(project_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE project_member (
    project_id INT,
    student_id INT,
    PRIMARY KEY (project_id, student_id),
    FOREIGN KEY (project_id) REFERENCES research_project(project_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);
