from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class AssetStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"
    DISPOSED = "disposed"


class AssetCategory(str, Enum):
    EQUIPMENT = "equipment"
    VEHICLE = "vehicle"
    ELECTRONICS = "electronics"
    FURNITURE = "furniture"
    TOOLS = "tools"
    OTHER = "other"


class AssetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Asset name")
    description: Optional[str] = Field(None, max_length=500, description="Asset description")
    category: AssetCategory = Field(..., description="Asset category")
    status: AssetStatus = Field(default=AssetStatus.ACTIVE, description="Asset status")
    serial_number: Optional[str] = Field(None, max_length=50, description="Serial number")
    purchase_date: Optional[date] = Field(None, description="Purchase date")
    purchase_price: Optional[float] = Field(None, ge=0, description="Purchase price")
    location: Optional[str] = Field(None, max_length=100, description="Asset location")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Person assigned to")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[AssetCategory] = None
    status: Optional[AssetStatus] = None
    serial_number: Optional[str] = Field(None, max_length=50)
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=100)
    assigned_to: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)


class Asset(AssetBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AssetList(BaseModel):
    total: int
    assets: list[Asset]