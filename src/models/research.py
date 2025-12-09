"""Research project domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class ResearchProject(BaseModel):
    """Represents a research project."""

    project_id: int
    title: str
    head_lecturer_id: int
    dept_id: int | None = None
    start_date: str | None = None
    end_date: str | None = None


@dataclass
class ProjectFunding(BaseModel):
    """Represents a funding source for a research project."""

    funding_id: int
    project_id: int
    source_name: str
    amount: float | None = None


@dataclass
class ProjectOutcome(BaseModel):
    """Represents an outcome from a research project."""

    outcome_id: int
    project_id: int
    description: str
    outcome_date: str | None = None
