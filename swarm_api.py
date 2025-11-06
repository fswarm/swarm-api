from __future__ import annotations

import os
import secrets
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Path, Query, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, constr, field_validator

# ----------------------------
# Customer API Key Configuration
# ----------------------------

# Load API keys from environment variables or use defaults
API_KEYS = {
    # Development key for testing
    "dev-key-12345": {
        "name": "Development Key",
        "permissions": ["read", "write", "admin"],
        "created_at": "2025-11-05T00:00:00"
    },
    
    # Customer API keys - provide these to your customers
    "biobot-alpha-2025-xk9f": {
        "name": "Alpha Corporation",
        "permissions": ["read", "write"],
        "created_at": "2025-11-05T00:00:00"
    },
    "biobot-beta-2025-m7p3": {
        "name": "Beta Industries",
        "permissions": ["read"],
        "created_at": "2025-11-05T00:00:00"
    },
    "biobot-gamma-2025-q4w8": {
        "name": "Gamma Solutions",
        "permissions": ["read", "write"],
        "created_at": "2025-11-05T00:00:00"
    },
    "biobot-delta-2025-r5t2": {
        "name": "Delta Research",
        "permissions": ["read", "write", "admin"],
        "created_at": "2025-11-05T00:00:00"
    },
    "biobot-echo-2025-v8n6": {
        "name": "Echo Robotics",
        "permissions": ["read"],
        "created_at": "2025-11-05T00:00:00"
    },
    "biobot-foxtrot-2025-z1y9": {
        "name": "Foxtrot Systems",
        "permissions": ["read", "write"],
        "created_at": "2025-11-05T00:00:00"
    }
}

# Load additional API keys from environment
ENV_API_KEYS = os.getenv("API_KEYS", "")
if ENV_API_KEYS:
    # Format: "key1:name1:permissions,key2:name2:permissions"
    # Example: "abc123:ProductionAPI:read|write,xyz789:AdminAPI:read|write|admin"
    for key_config in ENV_API_KEYS.split(","):
        parts = key_config.strip().split(":")
        if len(parts) >= 3:
            key, name, perms = parts[0], parts[1], parts[2]
            API_KEYS[key] = {
                "name": name,
                "permissions": perms.split("|") if "|" in perms else [perms],
                "created_at": datetime.utcnow().isoformat()
            }

# Security settings - Production Configuration  
REQUIRE_API_KEY = True  # Always require API key in production
security = HTTPBearer(auto_error=True, description="Enter your API key in the Authorization header")

# ----------------------------
# API Key Authentication
# ----------------------------

class APIKeyInfo(BaseModel):
    key: str
    name: str
    permissions: List[str]
    created_at: str

async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> APIKeyInfo:
    """
    Validate API key from Authorization header
    Expected format: Authorization: Bearer your-api-key-here
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="API key required. Please provide Authorization header with Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    api_key = credentials.credentials
    key_info = API_KEYS.get(api_key)
    
    if not key_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Please contact support for a valid API key.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return APIKeyInfo(
        key=api_key,
        name=key_info["name"],
        permissions=key_info["permissions"],
        created_at=key_info["created_at"]
    )

def require_permission(permission: str):
    """
    Dependency factory to require specific permissions
    """
    async def check_permission(api_key_info: APIKeyInfo = Depends(get_api_key)):
        if permission not in api_key_info.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient permissions. Required: {permission}. Available: {api_key_info.permissions}"
            )
        return api_key_info
    return check_permission

# Permission dependencies
require_read = require_permission("read")
require_write = require_permission("write")
require_admin = require_permission("admin")

# ----------------------------
# FastAPI App Setup
# ----------------------------

app = FastAPI(
    title="BioBot Swarm Management API",
    version="1.0.0",
    description=(
        " **Professional BioBot Swarm Management API**\n\n"
        "A secure, production-ready API for managing autonomous biobot swarms and individual biobots. "
        
        "**Authentication Required:** All endpoints require a valid API key in the Authorization header.\n"
        "Contact support to obtain your API key."
    ),
    contact={
        "name": "BioBot API Support",
       
    },
    license_info={
        
    },
    # Disable automatic documentation endpoints for production
    docs_url=None,      # Disables /docs
    redoc_url=None      # Disables /redoc (optional)
)

# Custom OpenAPI schema to remove example from security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Customize the security scheme to remove the example
    if "components" in openapi_schema and "securitySchemes" in openapi_schema["components"]:
        for scheme_name, scheme in openapi_schema["components"]["securitySchemes"].items():
            if scheme.get("type") == "http" and scheme.get("scheme") == "bearer":
                # Remove any example and update description
                scheme["bearerFormat"] = "API Key"
                scheme["description"] = "Enter your API key in the Authorization header"
                # Remove any example keys
                if "example" in scheme:
                    del scheme["example"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- Production CORS settings ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",  # Replace with your actual domain
        "https://app.yourdomain.com",  # Your web application domain
        "http://localhost:3000",  # For local development
        "http://localhost:8080",  # Alternative local port
        "null",  # Allow local file:// protocol (for offline Swagger docs)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# ----------------------------
# Models
# ----------------------------
class BioBotStatus(str, Enum):
    idle = "idle"
    active = "active"
    charging = "charging"
    fault = "fault"


class Position(BaseModel):
    latitude: float = Field(0.0, ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(0.0, ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    altitude: float = Field(0.0, description="Altitude in meters above sea level")


class SwarmBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=80)
    description: Optional[str] = Field(
        None, description="Short description of the swarm"
    )
    metadata: Optional[dict] = Field(
        default_factory=dict, description="Free-form JSON metadata"
    )


class SwarmCreate(SwarmBase):
    pass


class SwarmUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=80)] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


class Swarm(SwarmBase):
    id: int
    created_at: datetime
    biobots: List["BioBot"] = Field(default_factory=list, description="Biobots assigned to this swarm")


class BioBotBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=80)
    status: BioBotStatus = BioBotStatus.idle
    position: Position = Field(default_factory=Position)
    heading_deg: float = Field(0, ge=0.0, lt=360.0, description="Heading in degrees")
    battery_pct: float = Field(100, ge=0.0, le=100.0)
    metadata: Optional[dict] = Field(default_factory=dict)

    @field_validator("heading_deg")
    @classmethod
    def normalize_heading(cls, v: float) -> float:
        return float(v % 360)


class BioBotCreate(BioBotBase):
    swarm_id: Optional[int] = Field(
        None, description="Optional parent swarm id. BioBot can be free (None)."
    )


class BioBotUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=80)] = None
    status: Optional[BioBotStatus] = None
    position: Optional[Position] = None
    heading_deg: Optional[float] = Field(None, ge=0.0, lt=360.0)
    battery_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    metadata: Optional[dict] = None
    swarm_id: Optional[int] = Field(
        None, description="Set to an id to assign, or to null to detach"
    )


class TelemetryUpdate(BaseModel):
    position: Optional[Position] = None
    heading_deg: Optional[float] = Field(None, ge=0.0, lt=360.0)
    battery_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    status: Optional[BioBotStatus] = None


class BioBot(BioBotBase):
    id: int
    swarm_id: Optional[int] = None
    last_seen: Optional[datetime] = None


# ----------------------------
# Event Models
# ----------------------------
class EventSeverity(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class EventBase(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=50, strip_whitespace=True)
    description: str = Field(..., min_length=1, max_length=500)
    data: Optional[dict] = Field(default_factory=dict, description="Additional event data")
    severity: EventSeverity = EventSeverity.info


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    biobot_id: int
    timestamp: datetime


# ----------------------------
# In-memory stores (swap with DB later)
# ----------------------------
_swarm_store: Dict[int, Swarm] = {}
_biobot_store: Dict[int, BioBot] = {}
_event_store: Dict[int, Event] = {}

_next_swarm_id = 1
_next_biobot_id = 1
_next_event_id = 1


# ----------------------------
# Helpers
# ----------------------------

def _require_swarm(swarm_id: int) -> Swarm:
    swarm = _swarm_store.get(swarm_id)
    if not swarm:
        raise HTTPException(status_code=404, detail="Swarm not found")
    return swarm


def _require_biobot(biobot_id: int) -> BioBot:
    biobot = _biobot_store.get(biobot_id)
    if not biobot:
        raise HTTPException(status_code=404, detail="BioBot not found")
    return biobot


def _populate_swarm_biobots(swarm: Swarm) -> Swarm:
    """Populate a swarm with its assigned biobots"""
    swarm_biobots = [
        biobot for biobot in _biobot_store.values() 
        if biobot.swarm_id == swarm.id
    ]
    # Create a new swarm instance with biobots populated
    return Swarm(
        id=swarm.id,
        name=swarm.name,
        description=swarm.description,
        metadata=swarm.metadata,
        created_at=swarm.created_at,
        biobots=swarm_biobots
    )


# ----------------------------
# Security & Auth Endpoints
# ----------------------------

@app.get("/auth/info", tags=["security"])
async def auth_info(api_key_info: APIKeyInfo = Depends(get_api_key)):
    """Get information about the current API key"""
    return {
        "authenticated": True,
        "api_key_name": api_key_info.name,
        "permissions": api_key_info.permissions,
        "created_at": api_key_info.created_at
    }

@app.get("/auth/test", tags=["security"])
async def auth_test(api_key_info: APIKeyInfo = Depends(get_api_key)):
    """Test API key authentication"""
    return {
        "message": "Authentication successful!",
        "api_key_name": api_key_info.name,
        "permissions": api_key_info.permissions
    }

@app.post("/auth/generate-key", tags=["security"])
async def generate_api_key(
    name: str = "Generated Key",
    permissions: List[str] = ["read"],
    api_key_info: APIKeyInfo = Depends(require_admin)
):
    """Generate a new API key (admin only)"""
    new_key = secrets.token_urlsafe(32)
    API_KEYS[new_key] = {
        "name": name,
        "permissions": permissions,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "api_key": new_key,
        "name": name,
        "permissions": permissions,
        "message": "Store this key securely! It won't be shown again."
    }

@app.get("/auth/keys", tags=["security"])
async def list_api_keys(api_key_info: APIKeyInfo = Depends(require_admin)):
    """List all API keys (admin only) - keys are masked for security"""
    return [
        {
            "key_preview": f"{key[:8]}...{key[-4:]}",
            "name": info["name"],
            "permissions": info["permissions"],
            "created_at": info["created_at"]
        }
        for key, info in API_KEYS.items()
    ]

@app.delete("/auth/keys/{key_preview}", tags=["security"])
async def revoke_api_key(
    key_preview: str,
    api_key_info: APIKeyInfo = Depends(require_admin)
):
    """Revoke an API key (admin only)"""
    # Find key by preview
    key_to_delete = None
    for key in API_KEYS.keys():
        if f"{key[:8]}...{key[-4:]}" == key_preview:
            key_to_delete = key
            break
    
    if not key_to_delete:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Don't allow deleting your own key
    if key_to_delete == api_key_info.key:
        raise HTTPException(status_code=400, detail="Cannot revoke your own API key")
    
    del API_KEYS[key_to_delete]
    return {"message": f"API key {key_preview} has been revoked"}

# ----------------------------
# Health & Utility
# ----------------------------

@app.get("/", tags=["system"])
async def root():
    """Public endpoint - no authentication required"""
    return {
        "message": "Swarm & BioBots Secure API",
        "version": "1.0.0",
        "authentication": "required" if REQUIRE_API_KEY else "optional",
        "docs": "/docs",
        "health": "/health"
    }

# ----------------------------
# Health & Utility
# ----------------------------
@app.get("/health", tags=["system"])
async def health(api_key_info: APIKeyInfo = Depends(get_api_key)):
    """Health check - requires authentication"""
    return {
        "status": "ok", 
        "swarms": len(_swarm_store), 
        "biobots": len(_biobot_store),
        "authenticated_as": api_key_info.name,
        "api_auth_required": REQUIRE_API_KEY
    }


# ----------------------------
# Swarms CRUD
# ----------------------------
@app.post("/swarms", response_model=Swarm, status_code=201, tags=["swarms"])
async def create_swarm(
    payload: SwarmCreate,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    global _next_swarm_id
    swarm = Swarm(
        id=_next_swarm_id,
        name=payload.name,
        description=payload.description,
        metadata=payload.metadata or {},
        created_at=datetime.utcnow(),
    )
    _swarm_store[_next_swarm_id] = swarm
    _next_swarm_id += 1
    return _populate_swarm_biobots(swarm)


@app.get("/swarms", response_model=List[Swarm], tags=["swarms"])
async def list_swarms(
    q: Optional[str] = Query(None, description="Filter by name substring"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    swarms = list(_swarm_store.values())
    if q:
        swarms = [s for s in swarms if q.lower() in s.name.lower()]
    # Populate each swarm with its biobots
    populated_swarms = [_populate_swarm_biobots(swarm) for swarm in swarms[offset : offset + limit]]
    return populated_swarms


@app.get("/swarms/{swarm_id}", response_model=Swarm, tags=["swarms"])
async def get_swarm(
    swarm_id: int = Path(..., ge=1),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    swarm = _require_swarm(swarm_id)
    return _populate_swarm_biobots(swarm)


@app.put("/swarms/{swarm_id}", response_model=Swarm, tags=["swarms"])
async def update_swarm(
    swarm_id: int = Path(..., ge=1),
    updated_swarm: SwarmUpdate = ...,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    swarm = _require_swarm(swarm_id)
    data = swarm.dict()
    for field in ("name", "description", "metadata"):
        value = getattr(updated_swarm, field)
        if value is not None:
            data[field] = value
    updated = Swarm(**data)
    _swarm_store[swarm_id] = updated
    return _populate_swarm_biobots(updated)


@app.delete("/swarms/{swarm_id}", status_code=204, tags=["swarms"])
async def delete_swarm(
    swarm_id: int,
    api_key_info: APIKeyInfo = Depends(require_admin)
):
    _require_swarm(swarm_id)
    # Detach any biobots in this swarm
    for b in _biobot_store.values():
        if b.swarm_id == swarm_id:
            b.swarm_id = None
    del _swarm_store[swarm_id]
    return None


@app.get("/swarms/{swarm_id}/biobots", response_model=List[BioBot], tags=["swarms"])
async def list_swarm_biobots(
    swarm_id: int,
    status: Optional[BioBotStatus] = Query(None, description="Filter by status"),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    _require_swarm(swarm_id)
    biobots = [b for b in _biobot_store.values() if b.swarm_id == swarm_id]
    if status:
        biobots = [b for b in biobots if b.status == status]
    return biobots


# ----------------------------
# BioBots CRUD
# ----------------------------
@app.post("/biobots", response_model=BioBot, status_code=201, tags=["biobots"])
async def create_biobot(
    payload: BioBotCreate,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    global _next_biobot_id
    if payload.swarm_id is not None:
        _require_swarm(payload.swarm_id)
    biobot = BioBot(
        id=_next_biobot_id,
        name=payload.name,
        status=payload.status,
        position=payload.position,
        heading_deg=payload.heading_deg,
        battery_pct=payload.battery_pct,
        metadata=payload.metadata or {},
        swarm_id=payload.swarm_id,
        last_seen=None,
    )
    _biobot_store[_next_biobot_id] = biobot
    _next_biobot_id += 1
    return biobot


@app.get("/biobots", response_model=List[BioBot], tags=["biobots"])
async def list_biobots(
    swarm_id: Optional[int] = Query(
        None, description="Only biobots in this swarm id (or null for free biobots)"
    ),
    status: Optional[BioBotStatus] = Query(None, description="Filter by status"),
    q: Optional[str] = Query(None, description="Filter by name substring"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    biobots = list(_biobot_store.values())
    if swarm_id is not None:
        biobots = [b for b in biobots if b.swarm_id == swarm_id]
    if status is not None:
        biobots = [b for b in biobots if b.status == status]
    if q:
        biobots = [b for b in biobots if q.lower() in b.name.lower()]
    return biobots[offset : offset + limit]


@app.get("/biobots/{biobot_id}", response_model=BioBot, tags=["biobots"])
async def get_biobot(
    biobot_id: int = Path(..., ge=1),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    return _require_biobot(biobot_id)


@app.post("/biobots/{biobot_id}", response_model=BioBot, tags=["biobots"])
async def update_biobot(
    biobot_id: int,
    payload: BioBotUpdate,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    biobot = _require_biobot(biobot_id)
    data = biobot.dict()
    for field in ("name", "status", "position", "heading_deg", "battery_pct", "metadata"):
        value = getattr(payload, field)
        if value is not None:
            data[field] = value
    if payload.swarm_id is not None:
        # payload.swarm_id set to an int -> (re)assign
        _require_swarm(payload.swarm_id)
        data["swarm_id"] = payload.swarm_id
    elif payload.swarm_id is None and "swarm_id" in payload.__fields_set__:
        # explicitly null -> detach
        data["swarm_id"] = None

    updated = BioBot(**data)
    _biobot_store[biobot_id] = updated
    return updated


@app.delete("/biobots/{biobot_id}", status_code=204, tags=["biobots"])
async def delete_biobot(
    biobot_id: int,
    api_key_info: APIKeyInfo = Depends(require_admin)
):
    _require_biobot(biobot_id)
    del _biobot_store[biobot_id]
    return None


# ----------------------------
# Actions
# ----------------------------
@app.post("/biobots/{biobot_id}/telemetry", response_model=BioBot, tags=["actions"])
async def push_telemetry(
    biobot_id: int,
    payload: TelemetryUpdate,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    biobot = _require_biobot(biobot_id)
    if payload.position is not None:
        biobot.position = payload.position
    if payload.heading_deg is not None:
        biobot.heading_deg = float(payload.heading_deg % 360)
    if payload.battery_pct is not None:
        biobot.battery_pct = payload.battery_pct
    if payload.status is not None:
        biobot.status = payload.status
    biobot.last_seen = datetime.utcnow()
    _biobot_store[biobot_id] = biobot
    return biobot


@app.post("/swarms/{swarm_id}/assign/{biobot_id}", response_model=BioBot, tags=["actions"])
async def assign_biobot_to_swarm(
    swarm_id: int,
    biobot_id: int,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    _require_swarm(swarm_id)
    biobot = _require_biobot(biobot_id)
    biobot.swarm_id = swarm_id
    _biobot_store[biobot_id] = biobot
    return biobot


@app.post("/swarms/unassign/{biobot_id}", response_model=BioBot, tags=["actions"])
async def unassign_biobot(
    biobot_id: int,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    biobot = _require_biobot(biobot_id)
    biobot.swarm_id = None
    _biobot_store[biobot_id] = biobot
    return biobot


# ----------------------------
# Event API Endpoints
# ----------------------------
@app.get("/events", response_model=List[Event], tags=["events"])
async def list_events(
    biobot_id: Optional[int] = Query(None, description="Filter events by biobot ID"),
    event_type: Optional[str] = Query(None, description="Filter events by type"),
    severity: Optional[EventSeverity] = Query(None, description="Filter events by severity"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of events"),
    offset: int = Query(0, ge=0, description="Number of events to skip"),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    """Get list of events with optional filtering."""
    events = list(_event_store.values())
    
    # Apply filters
    if biobot_id is not None:
        events = [e for e in events if e.biobot_id == biobot_id]
    if event_type:
        events = [e for e in events if event_type.lower() in e.event_type.lower()]
    if severity:
        events = [e for e in events if e.severity == severity]
    
    # Sort by timestamp (newest first)
    events.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Apply pagination
    return events[offset:offset + limit]


@app.get("/biobots/{biobot_id}/events", response_model=List[Event], tags=["events"])
async def get_biobot_events(
    biobot_id: int,
    event_type: Optional[str] = Query(None, description="Filter events by type"),
    severity: Optional[EventSeverity] = Query(None, description="Filter events by severity"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of events"),
    offset: int = Query(0, ge=0, description="Number of events to skip"),
    api_key_info: APIKeyInfo = Depends(require_read)
):
    """Get events for a specific biobot."""
    _require_biobot(biobot_id)  # Ensure biobot exists
    
    events = [e for e in _event_store.values() if e.biobot_id == biobot_id]
    
    # Apply filters
    if event_type:
        events = [e for e in events if event_type.lower() in e.event_type.lower()]
    if severity:
        events = [e for e in events if e.severity == severity]
    
    # Sort by timestamp (newest first)
    events.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Apply pagination
    return events[offset:offset + limit]


@app.post("/biobots/{biobot_id}/events", response_model=Event, tags=["events"], status_code=201)
async def create_biobot_event(
    biobot_id: int,
    event_data: EventCreate,
    api_key_info: APIKeyInfo = Depends(require_write)
):
    """Create a new event for a specific biobot."""
    global _next_event_id
    
    _require_biobot(biobot_id)  # Ensure biobot exists
    
    event = Event(
        id=_next_event_id,
        biobot_id=biobot_id,
        event_type=event_data.event_type,
        description=event_data.description,
        data=event_data.data,
        severity=event_data.severity,
        timestamp=datetime.utcnow()
    )
    
    _event_store[_next_event_id] = event
    _next_event_id += 1
    
    return event


@app.get("/events/{event_id}", response_model=Event, tags=["events"])
async def get_event(
    event_id: int,
    api_key_info: APIKeyInfo = Depends(require_read)
):
    """Get a specific event by ID."""
    if event_id not in _event_store:
        raise HTTPException(status_code=404, detail="Event not found")
    return _event_store[event_id]


@app.delete("/events/{event_id}", status_code=204, tags=["events"])
async def delete_event(
    event_id: int,
    api_key_info: APIKeyInfo = Depends(require_admin)
):
    """Delete a specific event (admin only)."""
    if event_id not in _event_store:
        raise HTTPException(status_code=404, detail="Event not found")
    
    del _event_store[event_id]


# ----------------------------
# Demo seed data and startup
# ----------------------------
@app.on_event("startup")
async def _seed_demo():
    global _next_swarm_id, _next_biobot_id, _next_event_id
    
    # Show production startup status
    total_api_keys = len(API_KEYS)
    print("� BioBot Swarm Management API - Starting...")
    print(f"🔐 Security: ENABLED (Production Mode)")
    print(f"🔑 API Keys: {total_api_keys} customer keys configured")
    print(f"📡 CORS: Configured for production domains")
    print(f"🌍 Geography: Using lat/lng coordinates")
    print("✅ Ready for customer connections")
    
    if not _swarm_store and not _biobot_store:
        print("📊 Loading demo data for testing...")
        # Create three swarms with rich metadata
        s1 = Swarm(
            id=_next_swarm_id, 
            name="Alpha Squad", 
            description="Primary operations swarm for urban reconnaissance", 
            metadata={
                "mission_type": "reconnaissance",
                "deployment_zone": "urban",
                "priority": "high",
                "commander": "Agent Smith",
                "formation": "diamond",
                "max_range_km": 5.0
            }, 
            created_at=datetime.utcnow()
        )
        _swarm_store[_next_swarm_id] = s1
        _next_swarm_id += 1

        s2 = Swarm(
            id=_next_swarm_id, 
            name="Bravo Explorer", 
            description="Long-range exploration and mapping swarm", 
            metadata={
                "mission_type": "exploration",
                "deployment_zone": "wilderness",
                "priority": "medium",
                "commander": "Dr. Wilson",
                "formation": "line",
                "max_range_km": 15.0
            }, 
            created_at=datetime.utcnow()
        )
        _swarm_store[_next_swarm_id] = s2
        _next_swarm_id += 1

        s3 = Swarm(
            id=_next_swarm_id, 
            name="Charlie Rescue", 
            description="Emergency response and rescue operations", 
            metadata={
                "mission_type": "rescue",
                "deployment_zone": "disaster_area",
                "priority": "critical",
                "commander": "Captain Jones",
                "formation": "spread",
                "max_range_km": 8.0
            }, 
            created_at=datetime.utcnow()
        )
        _swarm_store[_next_swarm_id] = s3
        _next_swarm_id += 1

        # Create multiple biobots with rich metadata in each swarm
        
        # Alpha Squad biobots (3 units) - Operating in New York City area
        b1 = BioBot(
            id=_next_biobot_id, 
            name="Alpha-Leader", 
            status=BioBotStatus.active, 
            position=Position(latitude=40.7589, longitude=-73.9851, altitude=15.2), 
            heading_deg=45, 
            battery_pct=92, 
            metadata={
                "role": "squad_leader",
                "capabilities": ["surveillance", "communication", "navigation"],
                "last_maintenance": "2025-11-04",
                "sensor_suite": "advanced_optics",
                "payload_kg": 1.2
            }, 
            swarm_id=1, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b1
        _next_biobot_id += 1

        b2 = BioBot(
            id=_next_biobot_id, 
            name="Alpha-Scout", 
            status=BioBotStatus.active, 
            position=Position(latitude=40.7614, longitude=-73.9776, altitude=22.8), 
            heading_deg=30, 
            battery_pct=78, 
            metadata={
                "role": "reconnaissance",
                "capabilities": ["stealth", "long_range_sensors", "data_collection"],
                "last_maintenance": "2025-11-03",
                "sensor_suite": "thermal_imaging",
                "payload_kg": 0.8
            }, 
            swarm_id=1, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b2
        _next_biobot_id += 1

        b3 = BioBot(
            id=_next_biobot_id, 
            name="Alpha-Support", 
            status=BioBotStatus.idle, 
            position=Position(latitude=40.7505, longitude=-73.9934, altitude=8.5), 
            heading_deg=60, 
            battery_pct=85, 
            metadata={
                "role": "support",
                "capabilities": ["repair", "supply_drop", "medical_aid"],
                "last_maintenance": "2025-11-05",
                "sensor_suite": "medical_scanner",
                "payload_kg": 2.5
            }, 
            swarm_id=1, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b3
        _next_biobot_id += 1

        # Bravo Explorer biobots (4 units) - Operating in Colorado wilderness
        b4 = BioBot(
            id=_next_biobot_id, 
            name="Bravo-Navigator", 
            status=BioBotStatus.active, 
            position=Position(latitude=39.7392, longitude=-104.9903, altitude=1655.3), 
            heading_deg=180, 
            battery_pct=67, 
            metadata={
                "role": "navigation",
                "capabilities": ["mapping", "gps", "terrain_analysis"],
                "last_maintenance": "2025-11-02",
                "sensor_suite": "lidar_mapping",
                "payload_kg": 1.8
            }, 
            swarm_id=2, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b4
        _next_biobot_id += 1

        b5 = BioBot(
            id=_next_biobot_id, 
            name="Bravo-Sampler", 
            status=BioBotStatus.active, 
            position=Position(latitude=39.7285, longitude=-105.0178, altitude=1689.7), 
            heading_deg=195, 
            battery_pct=73, 
            metadata={
                "role": "sampling",
                "capabilities": ["soil_analysis", "water_testing", "air_quality"],
                "last_maintenance": "2025-11-01",
                "sensor_suite": "chemical_analyzer",
                "payload_kg": 3.1
            }, 
            swarm_id=2, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b5
        _next_biobot_id += 1

        b6 = BioBot(
            id=_next_biobot_id, 
            name="Bravo-Comm", 
            status=BioBotStatus.charging, 
            position=Position(latitude=39.7817, longitude=-104.9478, altitude=1612.1), 
            heading_deg=165, 
            battery_pct=34, 
            metadata={
                "role": "communication",
                "capabilities": ["long_range_radio", "data_relay", "satellite_uplink"],
                "last_maintenance": "2025-10-30",
                "sensor_suite": "radio_array",
                "payload_kg": 0.9
            }, 
            swarm_id=2, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b6
        _next_biobot_id += 1

        b7 = BioBot(
            id=_next_biobot_id, 
            name="Bravo-Guard", 
            status=BioBotStatus.active, 
            position=Position(latitude=39.7041, longitude=-105.0817, altitude=1743.9), 
            heading_deg=210, 
            battery_pct=89, 
            metadata={
                "role": "security",
                "capabilities": ["perimeter_watch", "threat_detection", "defense"],
                "last_maintenance": "2025-11-04",
                "sensor_suite": "motion_detection",
                "payload_kg": 1.5
            }, 
            swarm_id=2, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b7
        _next_biobot_id += 1

        # Charlie Rescue biobots (3 units) - Operating in California disaster area
        b8 = BioBot(
            id=_next_biobot_id, 
            name="Charlie-Medic", 
            status=BioBotStatus.active, 
            position=Position(latitude=34.0522, longitude=-118.2437, altitude=71.3), 
            heading_deg=270, 
            battery_pct=96, 
            metadata={
                "role": "medical",
                "capabilities": ["first_aid", "patient_monitoring", "drug_delivery"],
                "last_maintenance": "2025-11-05",
                "sensor_suite": "vital_signs_monitor",
                "payload_kg": 4.2
            }, 
            swarm_id=3, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b8
        _next_biobot_id += 1

        b9 = BioBot(
            id=_next_biobot_id, 
            name="Charlie-Rescue", 
            status=BioBotStatus.active, 
            position=Position(latitude=34.0407, longitude=-118.2468, altitude=89.6), 
            heading_deg=285, 
            battery_pct=81, 
            metadata={
                "role": "rescue",
                "capabilities": ["victim_extraction", "debris_clearing", "heavy_lifting"],
                "last_maintenance": "2025-11-03",
                "sensor_suite": "structural_scanner",
                "payload_kg": 6.8
            }, 
            swarm_id=3, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b9
        _next_biobot_id += 1

        b10 = BioBot(
            id=_next_biobot_id, 
            name="Charlie-Search", 
            status=BioBotStatus.fault, 
            position=Position(latitude=34.0619, longitude=-118.2357, altitude=103.7), 
            heading_deg=255, 
            battery_pct=12, 
            metadata={
                "role": "search",
                "capabilities": ["victim_detection", "voice_analysis", "thermal_search"],
                "last_maintenance": "2025-10-28",
                "sensor_suite": "thermal_camera",
                "payload_kg": 1.1,
                "fault_code": "SENSOR_MALFUNCTION"
            }, 
            swarm_id=3, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b10
        _next_biobot_id += 1

        # Two unassigned biobots (available for deployment) - Base location in Washington DC
        b11 = BioBot(
            id=_next_biobot_id, 
            name="Reserve-Delta", 
            status=BioBotStatus.idle, 
            position=Position(latitude=38.8951, longitude=-77.0364, altitude=125.0), 
            heading_deg=0, 
            battery_pct=100, 
            metadata={
                "role": "reserve",
                "capabilities": ["multi_purpose", "rapid_deployment", "adaptable"],
                "last_maintenance": "2025-11-05",
                "sensor_suite": "standard_package",
                "payload_kg": 0.0,
                "deployment_ready": True
            }, 
            swarm_id=None, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b11
        _next_biobot_id += 1

        b12 = BioBot(
            id=_next_biobot_id, 
            name="Reserve-Echo", 
            status=BioBotStatus.charging, 
            position=Position(latitude=38.8977, longitude=-77.0365, altitude=128.3), 
            heading_deg=90, 
            battery_pct=45, 
            metadata={
                "role": "reserve",
                "capabilities": ["multi_purpose", "rapid_deployment", "adaptable"],
                "last_maintenance": "2025-11-04",
                "sensor_suite": "standard_package",
                "payload_kg": 0.0,
                "deployment_ready": False
            }, 
            swarm_id=None, 
            last_seen=None
        )
        _biobot_store[_next_biobot_id] = b12
        _next_biobot_id += 1

        # Create demo events for biobots
        global _next_event_id
        
        # Events for Alpha Leader (b1)
        e1 = Event(
            id=_next_event_id,
            biobot_id=1,
            event_type="mission_start",
            description="Started reconnaissance mission in Central Park",
            data={"mission_id": "recon_001", "location": "Central Park, NYC"},
            severity=EventSeverity.info,
            timestamp=datetime.utcnow().replace(hour=9, minute=30)
        )
        _event_store[_next_event_id] = e1
        _next_event_id += 1

        e2 = Event(
            id=_next_event_id,
            biobot_id=1,
            event_type="battery_low",
            description="Battery level dropped below 20%",
            data={"battery_level": 15.5, "estimated_runtime": "45 minutes"},
            severity=EventSeverity.warning,
            timestamp=datetime.utcnow().replace(hour=14, minute=15)
        )
        _event_store[_next_event_id] = e2
        _next_event_id += 1

        # Events for Alpha Scout (b2)
        e3 = Event(
            id=_next_event_id,
            biobot_id=2,
            event_type="target_detected",
            description="Motion detected in sector 7",
            data={"sector": 7, "confidence": 0.87, "object_type": "human"},
            severity=EventSeverity.info,
            timestamp=datetime.utcnow().replace(hour=11, minute=45)
        )
        _event_store[_next_event_id] = e3
        _next_event_id += 1

        # Events for Reserve Echo (b12)
        e4 = Event(
            id=_next_event_id,
            biobot_id=12,
            event_type="charging_complete",
            description="Battery charging completed successfully",
            data={"charge_duration": "2.5 hours", "battery_level": 100},
            severity=EventSeverity.info,
            timestamp=datetime.utcnow().replace(hour=8, minute=0)
        )
        _event_store[_next_event_id] = e4
        _next_event_id += 1

        e5 = Event(
            id=_next_event_id,
            biobot_id=5,
            event_type="sensor_malfunction",
            description="LiDAR sensor showing intermittent readings",
            data={"sensor": "lidar", "error_rate": 0.23, "recommended_action": "maintenance"},
            severity=EventSeverity.error,
            timestamp=datetime.utcnow().replace(hour=13, minute=20)
        )
        _event_store[_next_event_id] = e5
        _next_event_id += 1

        print(f"📊 Demo data loaded: {len(_swarm_store)} swarms, {len(_biobot_store)} biobots, {len(_event_store)} events")


# ----------------------------
# Run (optional): `uvicorn fastapi_swarms_backend:app --reload`
# ----------------------------
if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run("fastapi_swarms_backend:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("uvicorn not installed. Install with: pip install uvicorn")
        print("Or run with: uvicorn fastapi_swarms_backend:app --reload")
