"""Image generation models."""

from enum import Enum

from pydantic import BaseModel, Field


class ImageType(str, Enum):
    """Available image types for social media sharing."""

    TOP_PRODUCTS = "top_products"
    CALENDAR = "calendar"
    SAVINGS = "savings"
    FAVORITE_TIME = "favorite_time"


class ImageRequest(BaseModel):
    """Request model for image generation."""

    image_type: ImageType
    period: str = Field(description="Okres: '2024' lub '2024-01'")
    limit: int = Field(default=10, ge=1, le=20, description="Limit dla top products")


class ImageConfig(BaseModel):
    """Configuration for image generation."""

    width: int = 1080
    height: int = 1080
    background_color: str = "#FFFFFF"
    primary_color: str = "#E30613"  # Biedronka red
    secondary_color: str = "#FFD700"  # Biedronka yellow
    text_color: str = "#333333"
    font_size_title: int = 72
    font_size_body: int = 48
    font_size_small: int = 36


class ImageResponse(BaseModel):
    """Response model for generated image."""

    filename: str
    content_type: str = "image/png"
    width: int
    height: int


class ImageMetadata(BaseModel):
    """Metadata about generated image."""

    image_type: ImageType
    period: str
    generated_at: str
    data_summary: dict
