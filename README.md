# Asset Manager

A simple asset management system built with FastAPI for tracking equipment, vehicles, electronics, and other organizational assets.

## Features

- **CRUD Operations**: Create, read, update, and delete assets
- **Filtering**: Filter assets by status, category, location, or assignee
- **Categories**: Equipment, Vehicles, Electronics, Furniture, Tools, Other
- **Status Tracking**: Active, Maintenance, Retired, Disposed
- **Statistics**: View asset counts and total values

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/assets` | Create a new asset |
| GET | `/assets` | List all assets (with filters) |
| GET | `/assets/{id}` | Get a specific asset |
| PUT | `/assets/{id}` | Update an asset |
| DELETE | `/assets/{id}` | Delete an asset |
| GET | `/stats` | Get asset statistics |
| GET | `/categories` | List all categories |
| GET | `/statuses` | List all statuses |

## Usage Examples

### Create an Asset

```bash
curl -X POST "http://localhost:8000/assets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro 16\"",
    "description": "Company laptop for development",
    "category": "electronics",
    "serial_number": "C02XG8GTJGH5",
    "purchase_date": "2024-01-15",
    "purchase_price": 2499.00,
    "location": "Office A",
    "assigned_to": "John Doe"
  }'
```

### List Assets with Filters

```bash
# All active assets
curl "http://localhost:8000/assets?status=active"

# Electronics only
curl "http://localhost:8000/assets?category=electronics"

# Assets at Office A
curl "http://localhost:8000/assets?location=Office%20A"
```

### Update an Asset

```bash
curl -X PUT "http://localhost:8000/assets/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "maintenance",
    "notes": "Sent for repair"
  }'
```

### Delete an Asset

```bash
curl -X DELETE "http://localhost:8000/assets/1"
```

## Data Model

### Asset Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | auto | Unique identifier |
| name | string | yes | Asset name |
| description | string | no | Detailed description |
| category | enum | yes | Asset category |
| status | enum | no | Asset status (default: active) |
| serial_number | string | no | Serial/model number |
| purchase_date | date | no | Date of purchase |
| purchase_price | float | no | Purchase cost |
| location | string | no | Physical location |
| assigned_to | string | no | Person assigned |
| notes | string | no | Additional notes |
| created_at | string | auto | Creation timestamp |
| updated_at | string | auto | Last update timestamp |

## Categories

- `equipment` - General equipment
- `vehicle` - Vehicles
- `electronics` - Electronic devices
- `furniture` - Furniture items
- `tools` - Tools and instruments
- `other` - Miscellaneous items

## Statuses

- `active` - Currently in use
- `maintenance` - Under repair or maintenance
- `retired` - No longer in active use
- `disposed` - Sold, donated, or discarded