"""Department domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Department(BaseModel):
    """Represents a department in the university."""

    dept_id: int
    name: str
    faculty: str | None = None


@dataclass
class ResearchArea(BaseModel):
    """Represents a research area within a department."""

    area_id: int
    dept_id: int
    area: str
