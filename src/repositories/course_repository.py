"""Course repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.course import Course, CourseMaterial
from src.models.lecturer import Lecturer
from src.models.tables import (
    course_prerequisite,
    lecturer_course,
    programme_course,
    student_course,
)
from src.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Repository for Course entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[Course]:
        return Course

    def get_by_department(self, dept_id: int) -> list[Course]:
        """Get all courses offered by a department."""
        stmt = (
            select(Course)
            .where(Course.dept_id == dept_id)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_department_lecturers(self, dept_id: int) -> list[Course]:
        """Get courses taught by lecturers in a department."""
        stmt = (
            select(Course)
            .distinct()
            .join(lecturer_course, Course.course_id == lecturer_course.c.course_id)
            .join(Lecturer, lecturer_course.c.lecturer_id == Lecturer.lecturer_id)
            .where(Lecturer.dept_id == dept_id)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_lecturer(self, lecturer_id: int) -> list[Course]:
        """Get all courses taught by a lecturer."""
        stmt = (
            select(Course)
            .join(lecturer_course, Course.course_id == lecturer_course.c.course_id)
            .where(lecturer_course.c.lecturer_id == lecturer_id)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_student(self, student_id: int) -> list[Course]:
        """Get all courses a student is enrolled in."""
        stmt = (
            select(Course)
            .join(student_course, Course.course_id == student_course.c.course_id)
            .where(student_course.c.student_id == student_id)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_programme(
        self,
        programme_id: int,
        required_only: bool = False,
    ) -> list[Course]:
        """Get all courses in a programme."""
        stmt = (
            select(Course)
            .join(programme_course, Course.course_id == programme_course.c.course_id)
            .where(programme_course.c.programme_id == programme_id)
        )
        if required_only:
            stmt = stmt.where(programme_course.c.is_required == 1)
        stmt = stmt.order_by(Course.course_code)
        return list(self._session.scalars(stmt).all())

    def get_materials(self, course_id: int) -> list[CourseMaterial]:
        """Get all materials for a course."""
        stmt = (
            select(CourseMaterial)
            .where(CourseMaterial.course_id == course_id)
            .order_by(CourseMaterial.title)
        )
        return list(self._session.scalars(stmt).all())

    def get_prerequisites(self, course_id: int) -> list[Course]:
        """Get all prerequisite courses for a course."""
        stmt = (
            select(Course)
            .join(
                course_prerequisite,
                Course.course_id == course_prerequisite.c.prerequisite_id,
            )
            .where(course_prerequisite.c.course_id == course_id)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_level(self, level: str) -> list[Course]:
        """Get all courses at a specific level."""
        stmt = (
            select(Course)
            .where(Course.level == level)
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_code(self, course_code: str) -> Course | None:
        """Get a course by its course code."""
        stmt = select(Course).where(Course.course_code == course_code)
        return self._session.scalar(stmt)

    def search(self, term: str) -> list[Course]:
        """Search courses by name or code."""
        pattern = f"%{term}%"
        stmt = (
            select(Course)
            .where(
                func.lower(Course.name).like(func.lower(pattern))
                | func.lower(Course.course_code).like(func.lower(pattern))
            )
            .order_by(Course.course_code)
        )
        return list(self._session.scalars(stmt).all())

    def add_prerequisite(self, course_id: int, prerequisite_id: int) -> bool:
        """Add a prerequisite to a course."""
        stmt = course_prerequisite.insert().values(
            course_id=course_id, prerequisite_id=prerequisite_id
        )
        self._session.execute(stmt)
        self._session.flush()
        return True

    def remove_prerequisite(self, course_id: int, prerequisite_id: int) -> bool:
        """Remove a prerequisite from a course."""
        stmt = course_prerequisite.delete().where(
            (course_prerequisite.c.course_id == course_id)
            & (course_prerequisite.c.prerequisite_id == prerequisite_id)
        )
        result = self._session.execute(stmt)
        self._session.flush()
        return result.rowcount > 0

    def add_to_programme(
        self,
        course_id: int,
        programme_id: int,
        is_required: bool = False,
    ) -> bool:
        """Add a course to a programme."""
        stmt = programme_course.insert().values(
            programme_id=programme_id,
            course_id=course_id,
            is_required=1 if is_required else 0,
        )
        self._session.execute(stmt)
        self._session.flush()
        return True

    def remove_from_programme(self, course_id: int, programme_id: int) -> bool:
        """Remove a course from a programme."""
        stmt = programme_course.delete().where(
            (programme_course.c.programme_id == programme_id)
            & (programme_course.c.course_id == course_id)
        )
        result = self._session.execute(stmt)
        self._session.flush()
        return result.rowcount > 0

    def add_material(
        self,
        course_id: int,
        title: str,
        material_type: str | None = None,
        url: str | None = None,
    ) -> CourseMaterial:
        """Add a material to a course."""
        material = CourseMaterial(
            course_id=course_id,
            title=title,
            material_type=material_type,
            url=url,
        )
        self._session.add(material)
        self._session.flush()
        self._session.refresh(material)
        return material
