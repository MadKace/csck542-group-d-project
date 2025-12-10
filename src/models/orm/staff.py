"""Non-academic staff ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.orm.base import Base

if TYPE_CHECKING:
    from src.models.orm.department import Department


class NonAcademicStaff(Base):
    """Represents a non-academic staff member."""

    __tablename__ = "non_academic_staff"

    staff_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    job_title: Mapped[str | None] = mapped_column(String(100))
    dept_id: Mapped[int | None] = mapped_column(ForeignKey("department.dept_id"))
    employment_type: Mapped[str | None] = mapped_column(String(20))
    contract_details: Mapped[str | None] = mapped_column(String(500))
    salary: Mapped[float | None] = mapped_column(Numeric(10, 2))
    emergency_contact: Mapped[str | None] = mapped_column(String(200))

    # Relationships
    department: Mapped["Department | None"] = relationship(back_populates="staff")
