"""Student domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Student(BaseModel):
    """Represents a student in the university."""

    student_id: int
    name: str
    date_of_birth: str | None = None
    contact_info: str | None = None
    programme_id: int | None = None
    year_of_study: int | None = None
    graduation_status: str | None = None
    advisor_id: int | None = None


@dataclass
class StudentGrade(BaseModel):
    """Represents a grade record for a student."""

    grade_id: int
    student_id: int
    course_id: int
    assessment_type: str | None = None
    grade: int | None = None
    date_recorded: str | None = None


@dataclass
class DisciplinaryRecord(BaseModel):
    """Represents a disciplinary record for a student."""

    record_id: int
    student_id: int
    incident_date: str | None = None
    description: str | None = None
    action_taken: str | None = None
