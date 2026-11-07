"""Persistent models used by the content management system."""

from datetime import datetime
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class CMSRecord(BaseModel):
    """One content item, keeping the editable draft separate from live data."""

    __tablename__ = 'cms_records'
    __table_args__ = (UniqueConstraint('kind', 'slug'),)

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    kind: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    draft_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    published_data: Mapped[dict | None] = mapped_column(JSON)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    draft_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    published_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class MediaAsset(BaseModel):
    __tablename__ = 'cms_media_assets'

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)
    alt_text: Mapped[str] = mapped_column(Text, nullable=False, default='')
    decorative: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )


class AdminAuthState(BaseModel):
    """Shared persistent lockout window for the single administrator."""

    __tablename__ = 'cms_admin_auth_state'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    failures: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    window_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
