"""Department repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.department import Department, ResearchArea
from src.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    """Repository for Department entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[Department]:
        return Department

    def get_by_name(self, name: str) -> Department | None:
        """Get a department by its name."""
        stmt = select(Department).where(Department.name == name)
        return self._session.scalar(stmt)

    def get_by_faculty(self, faculty: str) -> list[Department]:
        """Get all departments in a faculty."""
        stmt = (
            select(Department)
            .where(Department.faculty == faculty)
            .order_by(Department.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_research_areas(self, dept_id: int) -> list[ResearchArea]:
        """Get all research areas for a department."""
        stmt = (
            select(ResearchArea)
            .where(ResearchArea.dept_id == dept_id)
            .order_by(ResearchArea.area)
        )
        return list(self._session.scalars(stmt).all())

    def get_departments_with_research_area(self, area: str) -> list[Department]:
        """Get departments with a matching research area."""
        stmt = (
            select(Department)
            .distinct()
            .join(ResearchArea)
            .where(func.lower(ResearchArea.area).like(func.lower(f"%{area}%")))
            .order_by(Department.name)
        )
        return list(self._session.scalars(stmt).all())

    def search(self, name: str) -> list[Department]:
        """Search departments by name."""
        stmt = (
            select(Department)
            .where(func.lower(Department.name).like(func.lower(f"%{name}%")))
            .order_by(Department.name)
        )
        return list(self._session.scalars(stmt).all())

    def add_research_area(self, dept_id: int, area: str) -> ResearchArea:
        """Add a research area to a department."""
        research_area = ResearchArea(dept_id=dept_id, area=area)
        self._session.add(research_area)
        self._session.flush()
        self._session.refresh(research_area)
        return research_area
