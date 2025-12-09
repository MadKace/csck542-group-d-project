"""Non-academic staff domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class NonAcademicStaff(BaseModel):
    """Represents a non-academic staff member."""

    staff_id: int
    name: str
    job_title: str | None = None
    dept_id: int | None = None
    employment_type: str | None = None
    contract_details: str | None = None
    salary: float | None = None
    emergency_contact: str | None = None
