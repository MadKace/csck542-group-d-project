"""Student repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.orm.student import DisciplinaryRecord, Student, StudentGrade
from src.models.orm.tables import (
    lecturer_course,
    research_project_member,
    student_course,
)
from src.repositories.base_orm import BaseORMRepository


class StudentRepository(BaseORMRepository[Student]):
    """Repository for Student entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[Student]:
        return Student

    def get_by_advisor(self, lecturer_id: int) -> list[Student]:
        """Get all students advised by a lecturer."""
        stmt = (
            select(Student)
            .where(Student.advisor_id == lecturer_id)
            .order_by(Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_in_course_by_lecturer(
        self,
        course_id: int,
        lecturer_id: int,
    ) -> list[Student]:
        """Get students enrolled in a course taught by a specific lecturer."""
        stmt = (
            select(Student)
            .distinct()
            .join(student_course, Student.student_id == student_course.c.student_id)
            .join(lecturer_course, student_course.c.course_id == lecturer_course.c.course_id)
            .where(
                (student_course.c.course_id == course_id)
                & (lecturer_course.c.lecturer_id == lecturer_id)
            )
            .order_by(Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_grades(self, student_id: int) -> list[StudentGrade]:
        """Get all grades for a student."""
        stmt = (
            select(StudentGrade)
            .where(StudentGrade.student_id == student_id)
            .order_by(StudentGrade.date_recorded.desc())
        )
        return list(self._session.scalars(stmt).all())

    def get_disciplinary_records(self, student_id: int) -> list[DisciplinaryRecord]:
        """Get all disciplinary records for a student."""
        stmt = (
            select(DisciplinaryRecord)
            .where(DisciplinaryRecord.student_id == student_id)
            .order_by(DisciplinaryRecord.incident_date.desc())
        )
        return list(self._session.scalars(stmt).all())

    def get_by_programme(self, programme_id: int) -> list[Student]:
        """Get all students enrolled in a programme."""
        stmt = (
            select(Student)
            .where(Student.programme_id == programme_id)
            .order_by(Student.year_of_study, Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_course(self, course_id: int) -> list[Student]:
        """Get all students enrolled in a course."""
        stmt = (
            select(Student)
            .join(student_course, Student.student_id == student_course.c.student_id)
            .where(student_course.c.course_id == course_id)
            .order_by(Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def search(self, name: str) -> list[Student]:
        """Search students by name."""
        stmt = (
            select(Student)
            .where(func.lower(Student.name).like(func.lower(f"%{name}%")))
            .order_by(Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_research_project(self, project_id: int) -> list[Student]:
        """Get all student members of a research project."""
        stmt = (
            select(Student)
            .join(
                research_project_member,
                Student.student_id == research_project_member.c.student_id,
            )
            .where(research_project_member.c.project_id == project_id)
            .order_by(Student.name)
        )
        return list(self._session.scalars(stmt).all())

    def enrol_in_course(self, student_id: int, course_id: int) -> bool:
        """Enrol a student in a course."""
        stmt = student_course.insert().values(
            student_id=student_id, course_id=course_id
        )
        self._session.execute(stmt)
        self._session.flush()
        return True

    def unenrol_from_course(self, student_id: int, course_id: int) -> bool:
        """Remove a student from a course."""
        stmt = student_course.delete().where(
            (student_course.c.student_id == student_id)
            & (student_course.c.course_id == course_id)
        )
        result = self._session.execute(stmt)
        self._session.flush()
        return result.rowcount > 0

    def add_grade(
        self,
        student_id: int,
        course_id: int,
        assessment_type: str | None = None,
        grade: int | None = None,
        date_recorded: str | None = None,
    ) -> StudentGrade:
        """Add a grade record for a student."""
        student_grade = StudentGrade(
            student_id=student_id,
            course_id=course_id,
            assessment_type=assessment_type,
            grade=grade,
            date_recorded=date_recorded,
        )
        self._session.add(student_grade)
        self._session.flush()
        self._session.refresh(student_grade)
        return student_grade

    def add_disciplinary_record(
        self,
        student_id: int,
        incident_date: str | None = None,
        description: str | None = None,
        action_taken: str | None = None,
    ) -> DisciplinaryRecord:
        """Add a disciplinary record for a student."""
        record = DisciplinaryRecord(
            student_id=student_id,
            incident_date=incident_date,
            description=description,
            action_taken=action_taken,
        )
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record
