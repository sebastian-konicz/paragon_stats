"""Email waitlist models."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class WaitlistEntry(BaseModel):
    """Model for waitlist signup request."""

    email: EmailStr
    source: str = Field(default="dashboard", description="Źródło zapisu: dashboard, wrapped, landing")


class WaitlistDB(BaseModel):
    """Waitlist entry model for database storage."""

    email: str
    source: str
    created_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None


class WaitlistResponse(BaseModel):
    """Response model for waitlist signup."""

    success: bool
    message: str


class WaitlistStats(BaseModel):
    """Statistics about waitlist entries."""

    total_entries: int
    entries_by_source: dict[str, int]
