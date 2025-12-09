"""Lecturer domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Lecturer(BaseModel):
    """Represents a lecturer in the university."""

    lecturer_id: int
    name: str
    dept_id: int | None = None
    course_load: int | None = None


@dataclass
class LecturerQualification(BaseModel):
    """Represents an academic qualification of a lecturer."""

    qualification_id: int
    lecturer_id: int
    qualification_name: str
    institution: str | None = None
    year_awarded: int | None = None


@dataclass
class LecturerExpertise(BaseModel):
    """Represents an area of expertise for a lecturer."""

    expertise_id: int
    lecturer_id: int
    area: str


@dataclass
class Publication(BaseModel):
    """Represents a publication by a lecturer."""

    publication_id: int
    lecturer_id: int
    title: str
    journal: str | None = None
    publication_date: str | None = None
