"""Programme repository using SQLAlchemy ORM."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.orm.programme import Programme
from src.repositories.base_orm import BaseORMRepository


class ProgrammeRepository(BaseORMRepository[Programme]):
    """Repository for Programme entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[Programme]:
        return Programme

    def get_by_name(self, name: str) -> Programme | None:
        """Get a programme by its name."""
        stmt = select(Programme).where(Programme.name == name)
        return self._session.scalar(stmt)

    def get_by_degree(self, degree_awarded: str) -> list[Programme]:
        """Get all programmes awarding a specific degree."""
        stmt = (
            select(Programme)
            .where(Programme.degree_awarded == degree_awarded)
            .order_by(Programme.name)
        )
        return list(self._session.scalars(stmt).all())
