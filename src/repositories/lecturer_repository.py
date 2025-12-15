"""Lecturer repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.lecturer import (
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    LecturerResearchInterest,
    Publication,
)
from src.models.research import ResearchProject
from src.models.tables import lecturer_course
from src.repositories.base import BaseRepository


class LecturerRepository(BaseRepository[Lecturer]):
    """Repository for Lecturer entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[Lecturer]:
        return Lecturer

    def get_by_expertise(self, area: str) -> list[Lecturer]:
        """Get lecturers with expertise in a specific area."""
        stmt = (
            select(Lecturer)
            .distinct()
            .join(LecturerExpertise)
            .where(func.lower(LecturerExpertise.area).like(func.lower(f"%{area}%")))
            .order_by(Lecturer.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_department(self, dept_id: int) -> list[Lecturer]:
        """Get all lecturers in a department."""
        stmt = (
            select(Lecturer)
            .where(Lecturer.dept_id == dept_id)
            .order_by(Lecturer.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_available_head_lecturers(
        self, exclude_lecturer_id: int | None = None
    ) -> list[Lecturer]:
        """Get lecturers not already heading a research project.

        Args:
            exclude_lecturer_id: Optionally exclude this lecturer from the filter
                (useful when editing a project - the current head should still be available)

        Returns:
            List of lecturers who can be assigned as head of a research project.
        """
        # Subquery to get all lecturer IDs that are already head lecturers
        head_lecturer_ids = select(ResearchProject.head_lecturer_id)
        if exclude_lecturer_id is not None:
            head_lecturer_ids = head_lecturer_ids.where(
                ResearchProject.head_lecturer_id != exclude_lecturer_id
            )

        stmt = (
            select(Lecturer)
            .where(Lecturer.lecturer_id.not_in(head_lecturer_ids))
            .order_by(Lecturer.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_qualifications(self, lecturer_id: int) -> list[LecturerQualification]:
        """Get all qualifications for a lecturer."""
        stmt = (
            select(LecturerQualification)
            .where(LecturerQualification.lecturer_id == lecturer_id)
            .order_by(LecturerQualification.year_awarded.desc())
        )
        return list(self._session.scalars(stmt).all())

    def get_expertise(self, lecturer_id: int) -> list[LecturerExpertise]:
        """Get all expertise areas for a lecturer."""
        stmt = (
            select(LecturerExpertise)
            .where(LecturerExpertise.lecturer_id == lecturer_id)
            .order_by(LecturerExpertise.area)
        )
        return list(self._session.scalars(stmt).all())

    def get_publications(self, lecturer_id: int) -> list[Publication]:
        """Get all publications by a lecturer."""
        stmt = (
            select(Publication)
            .where(Publication.lecturer_id == lecturer_id)
            .order_by(Publication.publication_date.desc())
        )
        return list(self._session.scalars(stmt).all())

    def get_research_interests(
        self,
        lecturer_id: int,
    ) -> list[LecturerResearchInterest]:
        """Get all research interests for a lecturer."""
        stmt = (
            select(LecturerResearchInterest)
            .where(LecturerResearchInterest.lecturer_id == lecturer_id)
            .order_by(LecturerResearchInterest.interest)
        )
        return list(self._session.scalars(stmt).all())

    def search(self, name: str) -> list[Lecturer]:
        """Search lecturers by name."""
        stmt = (
            select(Lecturer)
            .where(func.lower(Lecturer.name).like(func.lower(f"%{name}%")))
            .order_by(Lecturer.name)
        )
        return list(self._session.scalars(stmt).all())

    def assign_to_course(self, lecturer_id: int, course_id: int) -> bool:
        """Assign a lecturer to teach a course."""
        stmt = lecturer_course.insert().values(
            lecturer_id=lecturer_id, course_id=course_id
        )
        self._session.execute(stmt)
        self._session.flush()
        return True

    def unassign_from_course(self, lecturer_id: int, course_id: int) -> bool:
        """Remove a lecturer from a course."""
        stmt = lecturer_course.delete().where(
            (lecturer_course.c.lecturer_id == lecturer_id)
            & (lecturer_course.c.course_id == course_id)
        )
        result = self._session.execute(stmt)
        self._session.flush()
        return result.rowcount > 0

    def add_qualification(
        self,
        lecturer_id: int,
        qualification_name: str,
        institution: str | None = None,
        year_awarded: int | None = None,
    ) -> LecturerQualification:
        """Add a qualification for a lecturer."""
        qualification = LecturerQualification(
            lecturer_id=lecturer_id,
            qualification_name=qualification_name,
            institution=institution,
            year_awarded=year_awarded,
        )
        self._session.add(qualification)
        self._session.flush()
        self._session.refresh(qualification)
        return qualification

    def add_expertise(self, lecturer_id: int, area: str) -> LecturerExpertise:
        """Add an expertise area for a lecturer."""
        expertise = LecturerExpertise(lecturer_id=lecturer_id, area=area)
        self._session.add(expertise)
        self._session.flush()
        self._session.refresh(expertise)
        return expertise

    def add_publication(
        self,
        lecturer_id: int,
        title: str,
        journal: str | None = None,
        publication_date: str | None = None,
    ) -> Publication:
        """Add a publication for a lecturer."""
        publication = Publication(
            lecturer_id=lecturer_id,
            title=title,
            journal=journal,
            publication_date=publication_date,
        )
        self._session.add(publication)
        self._session.flush()
        self._session.refresh(publication)
        return publication

    def add_research_interest(
        self,
        lecturer_id: int,
        interest: str,
    ) -> LecturerResearchInterest:
        """Add a research interest for a lecturer."""
        research_interest = LecturerResearchInterest(
            lecturer_id=lecturer_id, interest=interest
        )
        self._session.add(research_interest)
        self._session.flush()
        self._session.refresh(research_interest)
        return research_interest
