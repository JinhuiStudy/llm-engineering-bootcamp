"""Day 4: Pydantic 스키마."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class Skill(BaseModel):
    name: str
    level: Literal["beginner", "intermediate", "expert"]
    years: float | None = Field(default=None, ge=0, le=60)


class Achievement(BaseModel):
    description: str
    impact: str | None = None


class Experience(BaseModel):
    company: str
    role: str
    start_year: int = Field(ge=1970, le=2030)
    end_year: int | None = Field(default=None, ge=1970, le=2030)
    achievements: list[Achievement] = Field(default_factory=list)


class ResumeSummary(BaseModel):
    name: str
    email: EmailStr | None = None
    years_of_experience: int = Field(ge=0, le=60)
    headline: str = Field(description="한 줄 자기소개")
    skills: list[Skill]
    experiences: list[Experience]
