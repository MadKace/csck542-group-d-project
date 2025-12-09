"""Programme domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Programme(BaseModel):
    """Represents an academic programme."""

    programme_id: int
    name: str
    degree_awarded: str | None = None
    duration_years: int | None = None
    enrolment_details: str | None = None
