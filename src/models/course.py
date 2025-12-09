"""Course domain models."""

from dataclasses import dataclass

from src.models.base import BaseModel


@dataclass
class Course(BaseModel):
    """Represents a course in the university."""

    course_id: int
    course_code: str
    name: str
    description: str | None = None
    dept_id: int | None = None
    level: str | None = None
    credits: int | None = None
    schedule: str | None = None


@dataclass
class CourseMaterial(BaseModel):
    """Represents a material associated with a course."""

    material_id: int
    course_id: int
    title: str
    material_type: str | None = None
    url: str | None = None
