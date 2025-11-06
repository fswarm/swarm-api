# BioBot Swarm API - Data Architecture Documentation

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BioBot Swarm Management API                  │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Client Apps  →  🔑 Auth Layer  →  ⚡ FastAPI  →  💾 Storage │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ Data Entity Structure

### 1. 🏢 **SWARM** (Container Entity)
```
╔══════════════════════════════════════╗
║ Swarm                                ║
╠══════════════════════════════════════╣
║ • id: int (Primary Key)              ║
║ • name: string (1-80 chars)          ║
║ • description: string (optional)     ║
║ • metadata: dict (flexible JSON)     ║
║ • created_at: datetime (UTC)         ║
║ • biobots: list[BioBot] (children)   ║
╚══════════════════════════════════════╝
```

### 2. 🤖 **BIOBOT** (Individual Unit)
```
╔══════════════════════════════════════╗
║ BioBot                               ║
╠══════════════════════════════════════╣
║ • id: int (Primary Key)              ║
║ • name: string (1-80 chars)          ║
║ • status: enum (idle/active/         ║
║           charging/fault)            ║
║ • position: Position (embedded)      ║
║ • heading_deg: float (0-359.9°)      ║
║ • battery_pct: float (0-100%)        ║
║ • metadata: dict (flexible JSON)     ║
║ • swarm_id: int (Foreign Key, null)  ║
║ • last_seen: datetime (nullable)     ║
╚══════════════════════════════════════╝
```

### 3. 📍 **POSITION** (Geographic Location)
```
╔══════════════════════════════════════╗
║ Position                             ║
╠══════════════════════════════════════╣
║ • latitude: float (-90° to +90°)     ║
║ • longitude: float (-180° to +180°)  ║
║ • altitude: float (meters ASL)       ║
╚══════════════════════════════════════╝
```

### 4. 🔑 **API_KEY** (Authentication)
```
╔══════════════════════════════════════╗
║ API Key                              ║
╠══════════════════════════════════════╣
║ • key: string (Primary Key)          ║
║ • name: string (customer name)       ║
║ • permissions: list[string]          ║
║   └─ "read", "write", "admin"        ║
║ • created_at: datetime (UTC)         ║
╚══════════════════════════════════════╝
```

## 🔗 Entity Relationships

```
    SWARM (1) ←──────→ (0..n) BIOBOT
       │                       │
       │                       │
   [contains]              [belongs to]
       │                       │
       └─── One-to-Many ───────┘

    BIOBOT (1) ←──────→ (1) POSITION
       │                    │
   [has location]      [belongs to]
       │                    │
       └─── One-to-One ─────┘

    API_KEY (1) ←──────→ (0..n) REQUEST
       │                        │
  [authenticates]          [uses key]
       │                        │
       └─── One-to-Many ────────┘
```

## 📋 Business Rules & Constraints

### **Swarm Rules:**
- ✅ Can contain multiple BioBots (0..n relationship)
- ✅ Can exist without BioBots (empty swarm)
- ✅ Deletion auto-detaches all BioBots (sets swarm_id = null)
- ✅ Name must be unique and 1-80 characters

### **BioBot Rules:**
- ✅ Can exist without Swarm assignment (swarm_id = null)
- ✅ Can only belong to one Swarm at a time
- ✅ Position coordinates must be valid Earth coordinates
- ✅ Heading automatically normalized to 0-359.9°
- ✅ Battery percentage clamped to 0-100%

### **Position Rules:**
- ✅ Latitude: -90° (South Pole) to +90° (North Pole)
- ✅ Longitude: -180° (West) to +180° (East)
- ✅ Altitude: Any float value (negative = below sea level)

### **API Key Rules:**
- ✅ Each key has specific permissions (read/write/admin)
- ✅ All endpoints require valid authentication
- ✅ Permissions are checked per operation

## 🎯 Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│  Security   │───▶│  Endpoint   │
│ Application │    │ Validation  │    │  Handler    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  API Keys   │    │ In-Memory   │
                   │ Dictionary  │    │ Data Store  │
                   └─────────────┘    └─────────────┘
                                             │
                          ┌──────────────────┼──────────────────┐
                          ▼                  ▼                  ▼
                   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
                   │   swarms    │  │  biobots    │  │  next_ids   │
                   │ {id: swarm} │  │ {id: bot}   │  │ {counters}  │
                   └─────────────┘  └─────────────┘  └─────────────┘
```

## 🚀 Current Implementation Details

### **Storage Technology:**
- **Type:** In-memory Python dictionaries
- **Persistence:** None (data resets on restart)
- **Performance:** High-speed operations
- **Scalability:** Single-instance only

### **Data Structure:**
```python
# Global data stores
swarms: Dict[int, Swarm] = {}
biobots: Dict[int, BioBot] = {}
next_swarm_id: int = 1
next_biobot_id: int = 1

# API authentication
API_KEYS: Dict[str, dict] = {
    "biobot-alpha-2025-xk9f": {
        "name": "Alpha Corporation",
        "permissions": ["read", "write"]
    }
    # ... more keys
}
```

### **ID Generation:**
- **Type:** Auto-incrementing integers
- **Thread Safety:** Single-threaded (no concurrent access)
- **Uniqueness:** Guaranteed within session

### **Timestamp Format:**
- **Standard:** ISO 8601 UTC format
- **Example:** `2025-11-06T10:30:45.123456`
- **Timezone:** Always UTC (no local time)

## 📊 Current Data Examples

### **Sample Swarm:**
```json
{
  "id": 1,
  "name": "Alpha Squad",
  "description": "Primary operations swarm",
  "metadata": {
    "mission_type": "reconnaissance",
    "priority": "high"
  },
  "created_at": "2025-11-06T10:00:00.000000",
  "biobots": [...]
}
```

### **Sample BioBot:**
```json
{
  "id": 1,
  "name": "Scout-Alpha-1",
  "status": "active",
  "position": {
    "latitude": 40.7589,
    "longitude": -73.9851,
    "altitude": 15.2
  },
  "heading_deg": 45.0,
  "battery_pct": 85.5,
  "metadata": {
    "model": "RX-7",
    "sensors": ["lidar", "camera", "gps"]
  },
  "swarm_id": 1,
  "last_seen": "2025-11-06T10:30:00.000000"
}
```

## 🔧 Future Considerations

### **Scalability Improvements:**
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Caching layer (Redis)
- [ ] Horizontal scaling support
- [ ] Real-time sync mechanisms

### **Data Enhancements:**
- [ ] Historical position tracking
- [ ] Mission/task assignments
- [ ] Performance metrics
- [ ] Alert/notification system
- [ ] Batch operations support

---

**API Endpoint:** https://swarm-api-smzv.onrender.com/  
**Documentation:** https://swarm-api-smzv.onrender.com/docs  
**Repository:** Private (fswarm/swarm-api)