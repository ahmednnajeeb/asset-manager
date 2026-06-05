from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Asset,
    AssetCreate,
    AssetUpdate,
    AssetList,
    AssetStatus,
    AssetCategory,
)

app = FastAPI(
    title="Asset Manager API",
    description="A simple asset management system for tracking equipment, vehicles, and other assets",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
assets_db: dict[int, Asset] = {}
next_id = 1


def get_timestamp() -> str:
    return datetime.utcnow().isoformat()


@app.get("/", response_model=dict)
async def root():
    return {
        "message": "Asset Manager API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/assets", response_model=Asset, status_code=201)
async def create_asset(asset: AssetCreate):
    global next_id
    timestamp = get_timestamp()
    new_asset = Asset(
        id=next_id,
        created_at=timestamp,
        updated_at=timestamp,
        **asset.model_dump(),
    )
    assets_db[next_id] = new_asset
    next_id += 1
    return new_asset


@app.get("/assets", response_model=AssetList)
async def list_assets(
    status: Optional[AssetStatus] = Query(None, description="Filter by status"),
    category: Optional[AssetCategory] = Query(None, description="Filter by category"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned person"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
):
    filtered_assets = list(assets_db.values())
    
    if status:
        filtered_assets = [a for a in filtered_assets if a.status == status]
    if category:
        filtered_assets = [a for a in filtered_assets if a.category == category]
    if assigned_to:
        filtered_assets = [a for a in filtered_assets if a.assigned_to == assigned_to]
    if location:
        filtered_assets = [a for a in filtered_assets if a.location == location]
    
    filtered_assets.sort(key=lambda x: x.id, reverse=True)
    total = len(filtered_assets)
    paginated = filtered_assets[skip : skip + limit]
    
    return AssetList(total=total, assets=paginated)


@app.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: int):
    if asset_id not in assets_db:
        raise HTTPException(status_code=404, detail=f"Asset with id {asset_id} not found")
    return assets_db[asset_id]


@app.put("/assets/{asset_id}", response_model=Asset)
async def update_asset(asset_id: int, asset_update: AssetUpdate):
    if asset_id not in assets_db:
        raise HTTPException(status_code=404, detail=f"Asset with id {asset_id} not found")
    
    existing = assets_db[asset_id]
    update_data = asset_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing, field, value)
    
    existing.updated_at = get_timestamp()
    assets_db[asset_id] = existing
    return existing


@app.delete("/assets/{asset_id}", status_code=204)
async def delete_asset(asset_id: int):
    if asset_id not in assets_db:
        raise HTTPException(status_code=404, detail=f"Asset with id {asset_id} not found")
    del assets_db[asset_id]


@app.get("/stats", response_model=dict)
async def get_stats():
    total = len(assets_db)
    by_status = {}
    by_category = {}
    
    for asset in assets_db.values():
        by_status[asset.status.value] = by_status.get(asset.status.value, 0) + 1
        by_category[asset.category.value] = by_category.get(asset.category.value, 0) + 1
    
    total_value = sum(
        a.purchase_price or 0 for a in assets_db.values()
    )
    
    return {
        "total_assets": total,
        "by_status": by_status,
        "by_category": by_category,
        "total_value": total_value,
    }


@app.get("/categories", response_model=list[AssetCategory])
async def list_categories():
    return list(AssetCategory)


@app.get("/statuses", response_model=list[AssetStatus])
async def list_statuses():
    return list(AssetStatus)