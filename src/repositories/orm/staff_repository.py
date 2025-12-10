"""Staff repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.orm.staff import NonAcademicStaff
from src.repositories.base_orm import BaseORMRepository


class StaffRepository(BaseORMRepository[NonAcademicStaff]):
    """Repository for NonAcademicStaff entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[NonAcademicStaff]:
        return NonAcademicStaff

    def get_by_department(self, dept_id: int) -> list[NonAcademicStaff]:
        """Get all staff members in a department."""
        stmt = (
            select(NonAcademicStaff)
            .where(NonAcademicStaff.dept_id == dept_id)
            .order_by(NonAcademicStaff.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_job_title(self, job_title: str) -> list[NonAcademicStaff]:
        """Get all staff members with a specific job title."""
        stmt = (
            select(NonAcademicStaff)
            .where(
                func.lower(NonAcademicStaff.job_title).like(
                    func.lower(f"%{job_title}%")
                )
            )
            .order_by(NonAcademicStaff.name)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_employment_type(
        self,
        employment_type: str,
    ) -> list[NonAcademicStaff]:
        """Get all staff members with a specific employment type."""
        stmt = (
            select(NonAcademicStaff)
            .where(NonAcademicStaff.employment_type == employment_type)
            .order_by(NonAcademicStaff.name)
        )
        return list(self._session.scalars(stmt).all())

    def search(self, name: str) -> list[NonAcademicStaff]:
        """Search staff by name."""
        stmt = (
            select(NonAcademicStaff)
            .where(func.lower(NonAcademicStaff.name).like(func.lower(f"%{name}%")))
            .order_by(NonAcademicStaff.name)
        )
        return list(self._session.scalars(stmt).all())
