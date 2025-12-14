# API Reference

## Quick Start

```python
from src.services import APIService

api = APIService()  # Singleton, always returns same instance

# Access repositories via properties
students = api.student_repo.get_all()
lecturer = api.lecturer_repo.get_by_id(1)
courses = api.course_repo.get_by_department(dept_id=2)

# Transaction control
api.commit()    # Commit changes
api.rollback()  # Rollback changes
api.close()     # Close session and reset singleton
```

---

## APIService

Single entry point for all data access. Uses SQLAlchemy ORM with session-based
transaction management.

| Method | Description |
|--------|-------------|
| `commit()` | Commit the current transaction. |
| `rollback()` | Rollback the current transaction. |
| `close()` | Close the session and reset the singleton. |

| Property | Repository Type |
|----------|-----------------|
| `student_repo` | `StudentRepository` |
| `lecturer_repo` | `LecturerRepository` |
| `course_repo` | `CourseRepository` |
| `department_repo` | `DepartmentRepository` |
| `programme_repo` | `ProgrammeRepository` |
| `staff_repo` | `StaffRepository` |
| `research_project_repo` | `ResearchProjectRepository` |

---

## Base Repository Methods

All repositories inherit these methods:

### Read

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_id(id: int)` | `T` | Get entity by primary key. Raises `EntityNotFoundError` if not found. |
| `get_all()` | `list[T]` | Get all entities. |
| `exists(id: int)` | `bool` | Check if entity exists. |
| `count()` | `int` | Count total entities. |

### Create / Update / Delete

| Method | Return Type | Description |
|--------|-------------|-------------|
| `create(**kwargs)` | `T` | Create new entity. Returns the created entity with generated ID. |
| `update(id: int, **kwargs)` | `T` | Update entity fields. Returns updated entity. Raises `EntityNotFoundError` if not found. |
| `delete(id: int)` | `bool` | Delete entity. Returns `True` if deleted, `False` if not found. |

**Example:**
```python
# Create
student = api.student_repo.create(name="John Doe", year_of_study=1)
api.commit()

# Update
student = api.student_repo.update(student.student_id, year_of_study=2)
api.commit()

# Delete
deleted = api.student_repo.delete(student.student_id)
api.commit()
```

---

## StudentRepository

**Entity:** `Student`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_advisor(lecturer_id: int)` | `list[Student]` | Students advised by a lecturer. |
| `get_by_programme(programme_id: int)` | `list[Student]` | Students in a programme. |
| `get_by_course(course_id: int)` | `list[Student]` | Students enrolled in a course. |
| `get_by_research_project(project_id: int)` | `list[Student]` | Student members of a research project. |
| `get_in_course_by_lecturer(course_id: int, lecturer_id: int)` | `list[Student]` | Students in a course taught by a specific lecturer. |
| `get_grades(student_id: int)` | `list[StudentGrade]` | All grades for a student. |
| `get_disciplinary_records(student_id: int)` | `list[DisciplinaryRecord]` | Disciplinary records for a student. |
| `search(name: str)` | `list[Student]` | Search by name (case-insensitive, partial match). |
| `enrol_in_course(student_id, course_id)` | `bool` | Enrol student in a course. Returns `True` on success. |
| `unenrol_from_course(student_id, course_id)` | `bool` | Remove student from a course. Returns `False` if not enrolled. |
| `add_grade(student_id, course_id, ...)` | `StudentGrade` | Add a grade record. Returns the created record. |
| `add_disciplinary_record(student_id, ...)` | `DisciplinaryRecord` | Add a disciplinary record. Returns the created record. |

---

## LecturerRepository

**Entity:** `Lecturer`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_department(dept_id: int)` | `list[Lecturer]` | Lecturers in a department. |
| `get_by_expertise(area: str)` | `list[Lecturer]` | Lecturers with matching expertise (partial match). |
| `get_qualifications(lecturer_id: int)` | `list[LecturerQualification]` | Qualifications for a lecturer. |
| `get_expertise(lecturer_id: int)` | `list[LecturerExpertise]` | Expertise areas for a lecturer. |
| `get_publications(lecturer_id: int)` | `list[Publication]` | Publications by a lecturer. |
| `get_research_interests(lecturer_id: int)` | `list[LecturerResearchInterest]` | Research interests for a lecturer. |
| `search(name: str)` | `list[Lecturer]` | Search by name (case-insensitive, partial match). |
| `assign_to_course(lecturer_id, course_id)` | `bool` | Assign lecturer to teach a course. Returns `True` on success. |
| `unassign_from_course(lecturer_id, course_id)` | `bool` | Remove lecturer from a course. Returns `False` if not assigned. |
| `add_qualification(lecturer_id, qualification_name, ...)` | `LecturerQualification` | Add a qualification. Returns the created record. |
| `add_expertise(lecturer_id, area)` | `LecturerExpertise` | Add an expertise area. Returns the created record. |
| `add_publication(lecturer_id, title, ...)` | `Publication` | Add a publication. Returns the created record. |
| `add_research_interest(lecturer_id, interest)` | `LecturerResearchInterest` | Add a research interest. Returns the created record. |

---

## CourseRepository

**Entity:** `Course`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_department(dept_id: int)` | `list[Course]` | Courses offered by a department. |
| `get_by_department_lecturers(dept_id: int)` | `list[Course]` | Courses taught by lecturers in a department. |
| `get_by_lecturer(lecturer_id: int)` | `list[Course]` | Courses taught by a lecturer. |
| `get_by_student(student_id: int)` | `list[Course]` | Courses a student is enrolled in. |
| `get_by_programme(programme_id: int, required_only: bool = False)` | `list[Course]` | Courses in a programme. Set `required_only=True` for required courses only. |
| `get_by_level(level: str)` | `list[Course]` | Courses at a specific level. |
| `get_by_code(course_code: str)` | `Course \| None` | Get course by its code. |
| `get_prerequisites(course_id: int)` | `list[Course]` | Prerequisite courses. |
| `get_materials(course_id: int)` | `list[CourseMaterial]` | Materials for a course. |
| `search(term: str)` | `list[Course]` | Search by name or code (case-insensitive, partial match). |
| `add_prerequisite(course_id, prerequisite_id)` | `bool` | Add a prerequisite to a course. Returns `True` on success. |
| `remove_prerequisite(course_id, prerequisite_id)` | `bool` | Remove a prerequisite from a course. Returns `False` if not found. |
| `add_to_programme(course_id, programme_id, is_required=False)` | `bool` | Add course to a programme. Returns `True` on success. |
| `remove_from_programme(course_id, programme_id)` | `bool` | Remove course from a programme. Returns `False` if not found. |
| `add_material(course_id, title, ...)` | `CourseMaterial` | Add a material to a course. Returns the created record. |

---

## DepartmentRepository

**Entity:** `Department`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_name(name: str)` | `Department \| None` | Get department by exact name. |
| `get_by_faculty(faculty: str)` | `list[Department]` | Departments in a faculty. |
| `get_research_areas(dept_id: int)` | `list[ResearchArea]` | Research areas for a department. |
| `get_departments_with_research_area(area: str)` | `list[Department]` | Departments with matching research area (partial match). |
| `search(name: str)` | `list[Department]` | Search by name (case-insensitive, partial match). |
| `add_research_area(dept_id, area)` | `ResearchArea` | Add a research area to a department. Returns the created record. |

---

## ProgrammeRepository

**Entity:** `Programme`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_name(name: str)` | `Programme \| None` | Get programme by exact name. |
| `get_by_degree(degree_awarded: str)` | `list[Programme]` | Programmes awarding a specific degree. |

---

## StaffRepository

**Entity:** `NonAcademicStaff`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_department(dept_id: int)` | `list[NonAcademicStaff]` | Staff in a department. |
| `get_by_job_title(job_title: str)` | `list[NonAcademicStaff]` | Staff with matching job title (partial match). |
| `get_by_employment_type(employment_type: str)` | `list[NonAcademicStaff]` | Staff by employment type (exact match). |
| `search(name: str)` | `list[NonAcademicStaff]` | Search by name (case-insensitive, partial match). |

---

## ResearchProjectRepository

**Entity:** `ResearchProject`

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_by_department(dept_id: int)` | `list[ResearchProject]` | Projects in a department. |
| `get_by_head_lecturer(lecturer_id: int)` | `ResearchProject \| None` | Project headed by a lecturer. |
| `get_funding(project_id: int)` | `list[ProjectFunding]` | Funding sources for a project. |
| `get_outcomes(project_id: int)` | `list[ProjectOutcome]` | Outcomes for a project. |
| `search(title: str)` | `list[ResearchProject]` | Search by title (case-insensitive, partial match). |
| `add_member(project_id, student_id)` | `bool` | Add a student member to a project. Returns `True` on success. |
| `remove_member(project_id, student_id)` | `bool` | Remove a student member from a project. Returns `False` if not found. |
| `add_funding(project_id, source_name, ...)` | `ProjectFunding` | Add a funding source. Returns the created record. |
| `add_outcome(project_id, description, ...)` | `ProjectOutcome` | Add an outcome. Returns the created record. |

---

## Models

All models are SQLAlchemy ORM entities using `Mapped[]` type hints.

### Common Property

All models have an `as_dict` property that returns the model's attributes as a dictionary:

```python
student = api.student_repo.get_by_id(1)
print(student.as_dict)
# {'student_id': 1, 'name': 'John Doe', 'date_of_birth': '2000-01-01', ...}
```

### Student
| Field | Type |
|-------|------|
| student_id | int |
| name | str |
| date_of_birth | str \| None |
| contact_info | str \| None |
| programme_id | int \| None |
| year_of_study | int \| None |
| graduation_status | str \| None |
| advisor_id | int \| None |

### StudentGrade
| Field | Type |
|-------|------|
| grade_id | int |
| student_id | int |
| course_id | int |
| assessment_type | str \| None |
| grade | int \| None |
| date_recorded | str \| None |

### DisciplinaryRecord
| Field | Type |
|-------|------|
| record_id | int |
| student_id | int |
| incident_date | str \| None |
| description | str \| None |
| action_taken | str \| None |

### Lecturer
| Field | Type |
|-------|------|
| lecturer_id | int |
| name | str |
| dept_id | int \| None |
| course_load | int \| None |

### LecturerQualification
| Field | Type |
|-------|------|
| qualification_id | int |
| lecturer_id | int |
| qualification_name | str |
| institution | str \| None |
| year_awarded | int \| None |

### LecturerExpertise
| Field | Type |
|-------|------|
| expertise_id | int |
| lecturer_id | int |
| area | str |

### LecturerResearchInterest
| Field | Type |
|-------|------|
| interest_id | int |
| lecturer_id | int |
| interest | str |

### Publication
| Field | Type |
|-------|------|
| publication_id | int |
| lecturer_id | int |
| title | str |
| journal | str \| None |
| publication_date | str \| None |

### Course
| Field | Type |
|-------|------|
| course_id | int |
| course_code | str |
| name | str |
| description | str \| None |
| dept_id | int \| None |
| level | str \| None |
| credits | int \| None |
| schedule | str \| None |

### CourseMaterial
| Field | Type |
|-------|------|
| material_id | int |
| course_id | int |
| title | str |
| material_type | str \| None |
| url | str \| None |

### Department
| Field | Type |
|-------|------|
| dept_id | int |
| name | str |
| faculty | str \| None |

### ResearchArea
| Field | Type |
|-------|------|
| area_id | int |
| dept_id | int |
| area | str |

### Programme
| Field | Type |
|-------|------|
| programme_id | int |
| name | str |
| degree_awarded | str \| None |
| duration_years | int \| None |
| enrolment_details | str \| None |

### NonAcademicStaff
| Field | Type |
|-------|------|
| staff_id | int |
| name | str |
| job_title | str \| None |
| dept_id | int \| None |
| employment_type | str \| None |
| contract_details | str \| None |
| salary | float \| None |
| emergency_contact | str \| None |

### ResearchProject
| Field | Type |
|-------|------|
| project_id | int |
| title | str |
| head_lecturer_id | int |
| dept_id | int \| None |
| start_date | str \| None |
| end_date | str \| None |

### ProjectFunding
| Field | Type |
|-------|------|
| funding_id | int |
| project_id | int |
| source_name | str |
| amount | float \| None |

### ProjectOutcome
| Field | Type |
|-------|------|
| outcome_id | int |
| project_id | int |
| description | str |
| outcome_date | str \| None |

---

## Exceptions

| Exception | When Raised |
|-----------|-------------|
| `EntityNotFoundError` | `get_by_id()` or `update()` called with non-existent ID. |
| `DatabaseError` | Database connection or query execution fails. |
| `IntegrityError` | Database integrity constraint violated (e.g., foreign key, unique). |
| `ValidationError` | Data validation fails (e.g., missing required fields in `create()`). |
| `ConfigurationError` | Configuration-related errors. |

All exceptions inherit from `UniversityDBError`:

```python
from src.exceptions import UniversityDBError

try:
    student = api.student_repo.get_by_id(999)
except UniversityDBError as e:
    print(f"Error: {e.message}")
```
