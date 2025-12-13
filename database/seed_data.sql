-- Seed data generated using Faker library

INSERT INTO department (name, faculty) VALUES ('Computer Science', 'Science and Engineering');
INSERT INTO department (name, faculty) VALUES ('Mathematics', 'Science and Engineering');
INSERT INTO department (name, faculty) VALUES ('Physics', 'Science and Engineering');
INSERT INTO department (name, faculty) VALUES ('English', 'Arts and Humanities');
INSERT INTO department (name, faculty) VALUES ('Business', 'Business School');

INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('BSc Computer Science', 'BSc', 3);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('MSc Computer Science', 'MSc', 1);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('MSc Data Science', 'MSc', 1);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('BA English Literature', 'BA', 3);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('MBA Business Administration', 'MBA', 2);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('BSc Mathematics', 'BSc', 3);
INSERT INTO programme (name, degree_awarded, duration_years) VALUES ('PhD Computer Science', 'PhD', 4);

-- Lecturers
INSERT INTO lecturer (dept_id, name, course_load) VALUES (1, 'Dr Alexandre Traore', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (2, 'Dr Udant Dewan', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (3, 'Dr Yves Traore', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (4, 'Dr Piersanti Balbi', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (5, 'Dr Gillian Barnes', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (1, 'Dr Gaetano Verdone', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (2, 'Dr Jacobo del Agudo', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (3, 'Dr Gina Moore', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (4, 'Dr George Rai', 3);
INSERT INTO lecturer (dept_id, name, course_load) VALUES (5, 'Dr Miss Sylvia Pritchard', 3);

-- Students
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (1, 1, 'Bernard Wilkinson-Simpson', '2000-08-13', 'renata95@example.net', 1, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (2, 2, 'Amber Perez', '2000-08-16', 'jamesshawn@example.com', 2, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (3, 3, 'Daniel Adams', '2005-06-17', 'eleanorbriggs@example.org', 3, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (4, 4, 'Elba Gimenez Morata', '2001-11-23', 'joanne41@example.org', 4, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (5, 5, 'Sig.ra Eva Tarchetti', '2007-06-22', 'qmeunier@example.org', 1, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (6, 6, 'Kimberly Burgess', '2007-08-02', 'oorengo@example.org', 2, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (7, 7, 'Beatrice Bellini', '2001-03-31', 'sophiebazin@example.com', 3, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (1, 8, 'Orlando Paruta', '2003-12-06', 'angelica01@example.net', 4, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (2, 9, 'Massimiliano Caracciolo-Magrassi', '2001-04-17', 'lagoangelita@example.org', 1, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (3, 10, 'Lazzaro Tomaselli', '2001-08-21', 'kathryn88@example.org', 2, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (4, 1, 'Sig. Aldo Cardano', '2007-06-04', 'dalbirkhosla@example.net', 3, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (5, 2, 'June Sharp', '2006-06-18', 'donnaarroyo@example.org', 4, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (6, 3, 'Siddharth Zacharia', '2005-10-25', 'raymond57@example.net', 1, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (7, 4, 'Duilio Gomila Baró', '2000-02-16', 'biancagaluppi@example.org', 2, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (1, 5, 'Guy Howard-Townsend', '2007-04-05', 'varkeywazir@example.com', 3, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (2, 6, 'Frédérique Gimenez', '2006-02-06', 'ygolino@example.com', 4, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (3, 7, 'Asdrubal Caballero', '2003-08-13', 'droy@example.net', 1, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (4, 8, 'Toby Robinson', '2000-06-18', 'nereida13@example.org', 2, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (5, 9, 'Brenda White', '2002-01-27', 'jmann@example.org', 3, 'enrolled');
INSERT INTO student (programme_id, advisor_id, name, date_of_birth, contact_info, year_of_study, graduation_status) VALUES (6, 10, 'Mathew Lee', '2007-10-30', 'richardolson@example.com', 4, 'enrolled');

INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (1, 'CS101', 'Introduction to Programming', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (1, 'CS201', 'Data Structures', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (1, 'CS301', 'Databases and Information Systems', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (1, 'CS401', 'Machine Learning', 'Postgraduate', 20);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (2, 'MA101', 'Calculus', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (2, 'MA201', 'Linear Algebra', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (3, 'PH101', 'Classical Mechanics', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (4, 'EN101', 'Introduction to Literature', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (5, 'BA101', 'Principles of Management', 'Undergraduate', 15);
INSERT INTO course (dept_id, course_code, name, level, credits) VALUES (5, 'BA201', 'Financial Accounting', 'Undergraduate', 15);

-- Non-academic staff
INSERT INTO non_academic_staff (dept_id, name, job_title, employment_type, salary) VALUES (1, 'Janice Metcalfe', 'Admin Assistant', 'full-time', 35000);
INSERT INTO non_academic_staff (dept_id, name, job_title, employment_type, salary) VALUES (2, 'Ruben Sanz-Machado', 'Lab Technician', 'full-time', 35000);
INSERT INTO non_academic_staff (dept_id, name, job_title, employment_type, salary) VALUES (3, 'Nadia del Cortina', 'IT Support', 'full-time', 35000);
INSERT INTO non_academic_staff (dept_id, name, job_title, employment_type, salary) VALUES (4, 'Wayne Riley', 'HR Officer', 'full-time', 35000);
INSERT INTO non_academic_staff (dept_id, name, job_title, employment_type, salary) VALUES (5, 'Luca Bettoni', 'Finance', 'full-time', 35000);

-- Research projects
INSERT INTO research_project (head_lecturer_id, dept_id, title, start_date, end_date) VALUES (1, 1, 'Neural Network Architectures', '2024-01-01', '2025-12-31');
INSERT INTO research_project (head_lecturer_id, dept_id, title, start_date, end_date) VALUES (2, 1, 'Sustainable Computing', '2024-01-01', '2025-12-31');
INSERT INTO research_project (head_lecturer_id, dept_id, title, start_date, end_date) VALUES (3, 2, 'Applied Statistics', '2024-01-01', '2025-12-31');

-- Lecturer qualifications
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (1, 'PhD', 'University of Liverpool', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (2, 'PhD', 'University of Oxford', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (3, 'PhD', 'UCL', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (4, 'PhD', 'Imperial', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (5, 'PhD', 'Cambridge', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (6, 'PhD', 'Edinburgh', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (7, 'PhD', 'Manchester', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (8, 'PhD', 'Bristol', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (9, 'PhD', 'Warwick', 2015);
INSERT INTO lecturer_qualification (lecturer_id, qualification_name, institution, year_awarded) VALUES (10, 'PhD', 'Glasgow', 2015);

-- Lecturer expertise
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (1, 'Machine Learning');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (2, 'Databases');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (3, 'Networks');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (4, 'Security');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (5, 'AI');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (6, 'Algebra');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (7, 'Statistics');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (8, 'Quantum');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (9, 'Literature');
INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (10, 'Finance');

-- Student enrolments
INSERT INTO student_course (student_id, course_id, semester) VALUES (1, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (1, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (1, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (2, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (2, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (2, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (3, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (3, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (3, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (4, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (4, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (4, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (5, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (5, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (5, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (6, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (6, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (6, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (7, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (7, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (7, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (8, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (8, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (8, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (9, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (9, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (9, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (10, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (10, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (10, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (11, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (11, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (11, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (12, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (12, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (12, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (13, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (13, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (13, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (14, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (14, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (14, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (15, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (15, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (15, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (16, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (16, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (16, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (17, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (17, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (17, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (18, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (18, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (18, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (19, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (19, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (19, 3, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (20, 1, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (20, 2, 'Autumn 2024');
INSERT INTO student_course (student_id, course_id, semester) VALUES (20, 3, 'Autumn 2024');

-- Lecturer assignments
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (1, 1);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (2, 2);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (3, 3);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (4, 4);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (5, 5);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (6, 6);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (7, 7);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (8, 8);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (9, 9);
INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (10, 10);

-- Student grades
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (1, 1, 'exam', 52, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (1, 2, 'exam', 52, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (1, 3, 'exam', 52, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (2, 1, 'exam', 54, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (2, 2, 'exam', 54, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (2, 3, 'exam', 54, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (3, 1, 'exam', 56, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (3, 2, 'exam', 56, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (3, 3, 'exam', 56, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (4, 1, 'exam', 58, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (4, 2, 'exam', 58, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (4, 3, 'exam', 58, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (5, 1, 'exam', 60, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (5, 2, 'exam', 60, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (5, 3, 'exam', 60, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (6, 1, 'exam', 62, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (6, 2, 'exam', 62, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (6, 3, 'exam', 62, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (7, 1, 'exam', 64, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (7, 2, 'exam', 64, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (7, 3, 'exam', 64, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (8, 1, 'exam', 66, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (8, 2, 'exam', 66, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (8, 3, 'exam', 66, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (9, 1, 'exam', 68, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (9, 2, 'exam', 68, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (9, 3, 'exam', 68, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (10, 1, 'exam', 70, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (10, 2, 'exam', 70, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (10, 3, 'exam', 70, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (11, 1, 'exam', 72, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (11, 2, 'exam', 72, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (11, 3, 'exam', 72, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (12, 1, 'exam', 74, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (12, 2, 'exam', 74, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (12, 3, 'exam', 74, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (13, 1, 'exam', 76, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (13, 2, 'exam', 76, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (13, 3, 'exam', 76, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (14, 1, 'exam', 78, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (14, 2, 'exam', 78, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (14, 3, 'exam', 78, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (15, 1, 'exam', 80, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (15, 2, 'exam', 80, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (15, 3, 'exam', 80, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (16, 1, 'exam', 82, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (16, 2, 'exam', 82, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (16, 3, 'exam', 82, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (17, 1, 'exam', 84, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (17, 2, 'exam', 84, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (17, 3, 'exam', 84, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (18, 1, 'exam', 86, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (18, 2, 'exam', 86, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (18, 3, 'exam', 86, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (19, 1, 'exam', 88, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (19, 2, 'exam', 88, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (19, 3, 'exam', 88, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (20, 1, 'exam', 50, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (20, 2, 'exam', 50, '2024-12-01');
INSERT INTO student_grade (student_id, course_id, assessment_type, grade, date_recorded) VALUES (20, 3, 'exam', 50, '2024-12-01');

-- Programme courses
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (1, 1, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (1, 2, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (1, 3, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (2, 3, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (2, 4, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (6, 5, 1);
INSERT INTO programme_course (programme_id, course_id, is_required) VALUES (6, 6, 1);
