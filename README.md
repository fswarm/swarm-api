# Swarm & Robots API Documentation

A comprehensive FastAPI backend for managing robot swarms and individual robots. This API provides complete CRUD operations, real-time telemetry tracking, and swarm coordination capabilities. Built with FastAPI for high performance and automatic API documentation.

## 🚀 Key Features

- **🤖 Robot Management**: Complete lifecycle management of individual robots
- **🔗 Swarm Coordination**: Group robots into swarms for coordinated operations  
- **📡 Real-time Telemetry**: Track robot position, battery, status, and communication
- **🔄 Dynamic Assignment**: Assign/reassign robots between swarms on the fly
- **💾 In-Memory Storage**: Zero-configuration development environment
- **📚 Auto Documentation**: Interactive API docs with Swagger UI
- **🌐 CORS Enabled**: Ready for web-based frontends and cross-origin requests

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [API Overview](#-api-overview)
- [Authentication](#-authentication)
- [Health Check](#-health-check)
- [Swarms API](#-swarms-api)
- [Robots API](#-robots-api)
- [Actions API](#-actions-api)
- [Data Models](#-data-models)
- [Error Handling](#-error-handling)
- [Demo Data](#-demo-data)
- [Development Notes](#-development-notes)

## 🏃 Quick Start

### Prerequisites

```bash
# Python 3.8+ required
python --version

# Install required dependencies
pip install fastapi uvicorn pydantic
```

### Installation & Setup

1. **Clone or download the project**
2. **Install dependencies** (see above)
3. **Run the server**:

```bash
# Option 1: Direct execution (recommended for development)
python fastapi_swarms_backend.py

# Option 2: Using uvicorn command
uvicorn fastapi_swarms_backend:app --reload --host 0.0.0.0 --port 8000

# Option 3: Production mode (no auto-reload)
uvicorn fastapi_swarms_backend:app --host 0.0.0.0 --port 8000
```

### 🌐 Access Points

Once running, the API provides these endpoints:

| Service | URL | Description |
|---------|-----|-------------|
| **API Base** | http://localhost:8000 | Main API endpoint |
| **Interactive Docs** | http://localhost:8000/docs | Swagger UI - Test API directly in browser |
| **ReDoc** | http://localhost:8000/redoc | Alternative documentation format |
| **OpenAPI Schema** | http://localhost:8000/openapi.json | Machine-readable API specification |

> 💡 **Tip**: Use the Interactive Docs (Swagger UI) to explore and test all endpoints directly in your browser!

## 🔍 API Overview

This API follows RESTful principles with JSON request/response bodies. All endpoints return consistent data structures and use standard HTTP status codes.

### 🔐 Authentication

**Current Status**: No authentication required (development mode)

> ⚠️ **Security Note**: This is a development API with no authentication. In production, implement proper authentication (JWT, OAuth2, API keys) before deploying.

### 📊 Base URL Structure

```
Base URL: http://localhost:8000
Pattern:  /{resource}/{id?}/{action?}
```

**Examples:**
- `GET /robots` - List all robots
- `GET /robots/1` - Get specific robot
- `POST /robots/1/telemetry` - Update robot telemetry
- `POST /swarms/1/assign/2` - Assign robot 2 to swarm 1

### 📡 Health Check

#### `GET /health`

**Purpose**: Check API status and get system statistics

**Response Format:**
```json
{
  "status": "ok",           // Always "ok" if API is running
  "swarms": 2,             // Total number of swarms in system
  "robots": 3              // Total number of robots in system
}
```

**Use Cases:**
- Health monitoring and uptime checks
- Quick system statistics without fetching full data
- Load balancer health checks

---

## 🔗 Swarms API

Swarms are groups of robots that work together. Each swarm has metadata and can contain multiple robots.

### Create New Swarm

#### `POST /swarms`

**Purpose**: Create a new robot swarm

**Request Body:** (All fields except `name` are optional)
```json
{
  "name": "Alpha Squadron",                    // Required: 1-80 characters
  "description": "Primary operations swarm",   // Optional: Free text description  
  "metadata": {                               // Optional: Custom JSON data
    "mission_type": "reconnaissance",
    "priority": "high",
    "max_robots": 10,
    "operational_area": "sector_7"
  }
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,                                    // Auto-generated unique ID
  "name": "Alpha Squadron",
  "description": "Primary operations swarm",
  "metadata": {
    "mission_type": "reconnaissance", 
    "priority": "high",
    "max_robots": 10,
    "operational_area": "sector_7"
  },
  "created_at": "2025-11-05T10:30:00.123456"  // ISO 8601 UTC timestamp
}
```

**Notes:**
- `id` is auto-generated and unique
- `created_at` is automatically set to current UTC time
- `metadata` can store any JSON structure for custom properties
- Swarm names are trimmed of whitespace but preserved as entered

### List All Swarms

#### `GET /swarms`

**Purpose**: Retrieve list of all swarms with optional filtering and pagination

**Query Parameters:** (All optional)
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | none | Filter swarms by name (case-insensitive substring) |
| `limit` | integer | 50 | Maximum results to return (1-500) |
| `offset` | integer | 0 | Number of results to skip (for pagination) |

**Example Requests:**
```bash
# Get all swarms
GET /swarms

# Search for swarms with "alpha" in name
GET /swarms?q=alpha

# Get 10 swarms starting from result 20 (pagination)
GET /swarms?limit=10&offset=20

# Combined: search + pagination
GET /swarms?q=patrol&limit=5&offset=0
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Alpha Squadron", 
    "description": "Primary operations swarm",
    "metadata": {
      "mission_type": "reconnaissance",
      "priority": "high"
    },
    "created_at": "2025-11-05T10:30:00.123456"
  },
  {
    "id": 2,
    "name": "Bravo Team",
    "description": "Exploration swarm", 
    "metadata": {
      "mission_type": "exploration",
      "priority": "medium"
    },
    "created_at": "2025-11-05T10:35:00.789012"
  }
]
```

**Notes:**
- Returns empty array `[]` if no swarms match criteria
- Results are not guaranteed to be in any particular order
- Use `limit` and `offset` for pagination in large datasets

### Get Specific Swarm

#### `GET /swarms/{swarm_id}`

**Purpose**: Retrieve detailed information about a specific swarm

**Path Parameters:**
- `swarm_id` (integer, required): The unique ID of the swarm (must be ≥ 1)

**Example Request:**
```bash
GET /swarms/1
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Alpha Squadron",
  "description": "Primary operations swarm", 
  "metadata": {
    "mission_type": "reconnaissance",
    "priority": "high",
    "max_robots": 10,
    "operational_area": "sector_7"
  },
  "created_at": "2025-11-05T10:30:00.123456"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Swarm not found"
}
```

### Update Existing Swarm

#### `POST /swarms/{swarm_id}`

**Purpose**: Update an existing swarm (supports partial updates)

**Path Parameters:**
- `swarm_id` (integer, required): The unique ID of the swarm to update

**Request Body:** (All fields are optional - only include fields you want to change)
```json
{
  "name": "Alpha Squadron - Updated",           // Optional: New name
  "description": "Updated operations swarm",    // Optional: New description
  "metadata": {                                // Optional: Completely replaces existing metadata
    "mission_type": "surveillance",
    "priority": "critical", 
    "last_updated": "2025-11-05",
    "status": "active"
  }
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Alpha Squadron - Updated",          // Updated field
  "description": "Updated operations swarm",   // Updated field  
  "metadata": {                               // Completely replaced
    "mission_type": "surveillance",
    "priority": "critical",
    "last_updated": "2025-11-05", 
    "status": "active"
  },
  "created_at": "2025-11-05T10:30:00.123456"  // Unchanged
}
```

**Important Notes:**
- ⚠️ **Metadata Replacement**: The entire `metadata` object is replaced, not merged
- ✅ **Partial Updates**: Only send fields you want to change
- ✅ **Validation**: Name must be 1-80 characters if provided
- ❌ **Immutable Fields**: `id` and `created_at` cannot be changed

**Error Responses:**
```json
// 404 Not Found
{
  "detail": "Swarm not found"
}

// 422 Validation Error  
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Delete Swarm

#### `DELETE /swarms/{swarm_id}`

**Purpose**: Permanently delete a swarm and automatically detach all robots from it

**Path Parameters:**
- `swarm_id` (integer, required): The unique ID of the swarm to delete

**Example Request:**
```bash
DELETE /swarms/1
```

**Success Response (204 No Content):**
- No response body
- HTTP status code 204 indicates successful deletion

**Side Effects:**
- 🤖 **Robot Auto-Detachment**: All robots assigned to this swarm become unassigned (`swarm_id` becomes `null`)
- 💾 **Permanent Deletion**: Swarm data is permanently removed (cannot be undone)

**Error Response (404 Not Found):**
```json
{
  "detail": "Swarm not found"
}
```

**Example Workflow:**
```bash
# Before deletion: Robot 1 is in swarm 1
GET /robots/1
# Response: {"id": 1, "swarm_id": 1, ...}

# Delete the swarm
DELETE /swarms/1
# Response: 204 No Content

# After deletion: Robot 1 is now unassigned
GET /robots/1  
# Response: {"id": 1, "swarm_id": null, ...}
```

### List Robots in Swarm

#### `GET /swarms/{swarm_id}/robots`

**Purpose**: Get all robots currently assigned to a specific swarm

**Path Parameters:**
- `swarm_id` (integer, required): The unique ID of the swarm

**Query Parameters:**
| Parameter | Type | Options | Description |
|-----------|------|---------|-------------|
| `status` | string | `idle`, `active`, `charging`, `fault` | Filter robots by their current status |

**Example Requests:**
```bash
# Get all robots in swarm 1
GET /swarms/1/robots

# Get only active robots in swarm 1  
GET /swarms/1/robots?status=active

# Get only charging robots in swarm 2
GET /swarms/2/robots?status=charging
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Rover-Alpha-1",
    "status": "active",
    "position": {
      "x": 10.5,
      "y": 25.3, 
      "z": 0.0
    },
    "heading_deg": 45.0,
    "battery_pct": 85.5,
    "metadata": {
      "model": "RX-7",
      "sensors": ["lidar", "camera", "gps"]
    },
    "swarm_id": 1,                              // Always matches the requested swarm_id
    "last_seen": "2025-11-05T11:45:30.123456"
  }
]
```

**Notes:**
- Returns empty array `[]` if swarm has no robots or no robots match filter
- All returned robots will have `swarm_id` matching the requested swarm
- Robots with `swarm_id: null` (unassigned) will never appear in these results

---

## 🤖 Robots API

Individual robots with position tracking, battery monitoring, and status management.

### Create New Robot

#### `POST /robots`

**Purpose**: Create a new robot with optional swarm assignment

**Request Body:**
```json
{
  "name": "Rover-Charlie-1",                    // Required: 1-80 characters
  "status": "idle",                            // Optional: Default "idle"
  "position": {                                // Optional: Default (0,0,0)
    "x": 0.0,                                 // X coordinate in meters
    "y": 0.0,                                 // Y coordinate in meters  
    "z": 0.0                                  // Z coordinate in meters (altitude)
  },
  "heading_deg": 90.0,                         // Optional: 0-359.9 degrees, default 0
  "battery_pct": 100.0,                        // Optional: 0-100%, default 100
  "metadata": {                                // Optional: Custom JSON data
    "model": "RX-9",
    "capabilities": ["autonomous_navigation", "object_detection"],
    "max_speed_ms": 2.5,
    "weight_kg": 15.2
  },
  "swarm_id": 1                               // Optional: null = unassigned, number = assign to swarm
}
```

**Field Details:**
| Field | Type | Required | Validation | Default |
|-------|------|----------|------------|---------|
| `name` | string | ✅ Yes | 1-80 chars, whitespace trimmed | - |
| `status` | enum | ❌ No | `idle`, `active`, `charging`, `fault` | `idle` |
| `position` | object | ❌ No | Valid Position object | `{x:0, y:0, z:0}` |
| `heading_deg` | number | ❌ No | 0.0 ≤ value < 360.0 | `0.0` |
| `battery_pct` | number | ❌ No | 0.0 ≤ value ≤ 100.0 | `100.0` |
| `metadata` | object | ❌ No | Any valid JSON | `{}` |
| `swarm_id` | integer/null | ❌ No | Must be valid swarm ID or null | `null` |

**Success Response (201 Created):**
```json
{
  "id": 4,                                    // Auto-generated unique ID
  "name": "Rover-Charlie-1",
  "status": "idle",
  "position": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
  },
  "heading_deg": 90.0,                        // Automatically normalized to 0-359.9
  "battery_pct": 100.0,
  "metadata": {
    "model": "RX-9",
    "capabilities": ["autonomous_navigation", "object_detection"],
    "max_speed_ms": 2.5,
    "weight_kg": 15.2
  },
  "swarm_id": 1,
  "last_seen": null                           // null until first telemetry update
}
```

**Error Responses:**
```json
// 404 Not Found (invalid swarm_id)
{
  "detail": "Swarm not found" 
}

// 422 Validation Error (invalid heading)
{
  "detail": [
    {
      "loc": ["body", "heading_deg"],
      "msg": "ensure this value is less than 360",
      "type": "value_error.number.not_lt"
    }
  ]
}
```

### List All Robots

#### `GET /robots`

**Purpose**: Retrieve list of all robots with advanced filtering and pagination

**Query Parameters:** (All optional)
| Parameter | Type | Options/Range | Description |
|-----------|------|---------------|-------------|
| `swarm_id` | integer/null | Any valid swarm ID or literal `null` | Filter by swarm assignment |
| `status` | string | `idle`, `active`, `charging`, `fault` | Filter by robot status |
| `q` | string | Any text | Filter by name (case-insensitive substring) |
| `limit` | integer | 1-500 | Maximum results to return (default: 50) |
| `offset` | integer | 0+ | Number of results to skip (default: 0) |

**Example Requests:**
```bash
# Get all robots
GET /robots

# Get only unassigned robots (free agents)
GET /robots?swarm_id=null

# Get robots in swarm 1
GET /robots?swarm_id=1

# Get all active robots regardless of swarm
GET /robots?status=active

# Search for robots with "rover" in name
GET /robots?q=rover

# Get charging robots in swarm 1, limit to 5 results
GET /robots?swarm_id=1&status=charging&limit=5

# Pagination: Get robots 11-20
GET /robots?limit=10&offset=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Rover-Alpha-1", 
    "status": "active",
    "position": {
      "x": 10.5,
      "y": 25.3,
      "z": 0.0
    },
    "heading_deg": 45.0,
    "battery_pct": 85.5,
    "metadata": {
      "model": "RX-7", 
      "sensors": ["lidar", "camera", "gps"]
    },
    "swarm_id": 1,                              // Assigned to swarm 1
    "last_seen": "2025-11-05T11:45:30.123456"   // Last telemetry update
  },
  {
    "id": 2,
    "name": "Scout-Bravo-1",
    "status": "charging", 
    "position": {
      "x": -5.0,
      "y": 12.8,
      "z": 0.0
    },
    "heading_deg": 180.0,
    "battery_pct": 22.0,
    "metadata": {
      "model": "SC-3",
      "type": "reconnaissance"
    },
    "swarm_id": null,                           // Unassigned robot
    "last_seen": "2025-11-05T10:20:15.987654"
  }
]
```

**Filter Combinations:**
- ✅ Multiple filters work together (AND logic)
- ✅ `swarm_id=null` finds unassigned robots
- ✅ Empty results return `[]` (not an error)

### Get Specific Robot

#### GET /robots/{robot_id}
Retrieves a specific robot by ID.

**Response:**
```json
{
  "id": 1,
  "name": "Rover-Alpha-1",
  "status": "active",
  "position": {
    "x": 10.5,
    "y": 25.3,
    "z": 0.0
  },
  "heading_deg": 45.0,
  "battery_pct": 85.5,
  "metadata": {
    "model": "RX-7",
    "sensors": ["lidar", "camera", "gps"]
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T11:45:30.123456"
}
```

### Update Robot

#### POST /robots/{robot_id}
Updates an existing robot (partial updates supported).

**Request Body:**
```json
{
  "status": "charging",
  "position": {
    "x": 15.2,
    "y": 30.1,
    "z": 0.0
  },
  "battery_pct": 75.0,
  "metadata": {
    "model": "RX-7",
    "sensors": ["lidar", "camera", "gps"],
    "last_maintenance": "2025-11-01"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Rover-Alpha-1",
  "status": "charging",
  "position": {
    "x": 15.2,
    "y": 30.1,
    "z": 0.0
  },
  "heading_deg": 45.0,
  "battery_pct": 75.0,
  "metadata": {
    "model": "RX-7",
    "sensors": ["lidar", "camera", "gps"],
    "last_maintenance": "2025-11-01"
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T11:45:30.123456"
}
```

### Delete Robot

#### DELETE /robots/{robot_id}
Deletes a robot permanently.

**Response:** 204 No Content

---

## Actions API

### Push Telemetry

#### POST /robots/{robot_id}/telemetry
Updates robot telemetry data and sets last_seen timestamp.

**Request Body:**
```json
{
  "position": {
    "x": 20.7,
    "y": 35.4,
    "z": 1.2
  },
  "heading_deg": 275.5,
  "battery_pct": 68.3,
  "status": "active"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Rover-Alpha-1",
  "status": "active",
  "position": {
    "x": 20.7,
    "y": 35.4,
    "z": 1.2
  },
  "heading_deg": 275.5,
  "battery_pct": 68.3,
  "metadata": {
    "model": "RX-7",
    "sensors": ["lidar", "camera", "gps"]
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T12:00:00.123456"
}
```

### Assign Robot to Swarm

#### POST /swarms/{swarm_id}/assign/{robot_id}
Assigns a robot to a specific swarm.

**Response:**
```json
{
  "id": 2,
  "name": "Scout-Bravo-1",
  "status": "charging",
  "position": {
    "x": -5.0,
    "y": 12.8,
    "z": 0.0
  },
  "heading_deg": 180.0,
  "battery_pct": 22.0,
  "metadata": {
    "model": "SC-3",
    "type": "reconnaissance"
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T10:20:15.987654"
}
```

### Unassign Robot from Swarm

#### POST /swarms/unassign/{robot_id}
Removes a robot from its current swarm (makes it free/unassigned).

**Response:**
```json
{
  "id": 2,
  "name": "Scout-Bravo-1",
  "status": "charging",
  "position": {
    "x": -5.0,
    "y": 12.8,
    "z": 0.0
  },
  "heading_deg": 180.0,
  "battery_pct": 22.0,
  "metadata": {
    "model": "SC-3",
    "type": "reconnaissance"
  },
  "swarm_id": null,
  "last_seen": "2025-11-05T10:20:15.987654"
}
```

---

## Data Models

### Robot Status Enum
- `idle`: Robot is inactive and available
- `active`: Robot is currently performing tasks
- `charging`: Robot is charging its battery
- `fault`: Robot has encountered an error

### Position Object
```json
{
  "x": 0.0,    // X coordinate in meters
  "y": 0.0,    // Y coordinate in meters  
  "z": 0.0     // Z coordinate in meters (altitude)
}
```

### Swarm Object
```json
{
  "id": 1,
  "name": "Swarm Name",
  "description": "Optional description",
  "metadata": {},  // Free-form JSON object
  "created_at": "2025-11-05T10:30:00.123456"
}
```

### Robot Object
```json
{
  "id": 1,
  "name": "Robot Name",
  "status": "idle",           // Robot status enum
  "position": {},             // Position object
  "heading_deg": 0.0,         // Heading in degrees (0-359.9)
  "battery_pct": 100.0,       // Battery percentage (0-100)
  "metadata": {},             // Free-form JSON object
  "swarm_id": 1,              // ID of assigned swarm (null if unassigned)
  "last_seen": "2025-11-05T10:30:00.123456"  // Last telemetry update
}
```

---

## Demo Data

The API starts with demo data:

**Swarms:**
- Alpha (ID: 1) - Primary ops swarm
- Bravo (ID: 2) - Exploration swarm

**Robots:**
- Rover-1 (ID: 1) - Assigned to Alpha swarm, idle, 88% battery
- Rover-2 (ID: 2) - Assigned to Alpha swarm, active, 73% battery  
- Scout-1 (ID: 3) - Unassigned, charging, 22% battery

## 🚨 Error Handling

This API uses standard HTTP status codes and provides detailed error messages in JSON format.

### HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| **200** | OK | Successful GET/POST request |
| **201** | Created | Successful resource creation |
| **204** | No Content | Successful DELETE request |
| **404** | Not Found | Resource doesn't exist |
| **422** | Validation Error | Invalid request data |
| **500** | Server Error | Unexpected server problem |

### Error Response Format

All errors return JSON with a `detail` field:

#### 404 Not Found Errors
```json
{
  "detail": "Swarm not found"
}
```
```json
{
  "detail": "Robot not found" 
}
```

**Common Causes:**
- Requesting non-existent ID
- ID was deleted
- Typo in URL path

#### 422 Validation Errors

**Single Field Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "battery_pct"],                    // Location of error
      "msg": "ensure this value is less than or equal to 100",  // Human-readable message  
      "type": "value_error.number.not_le",               // Error type code
      "ctx": {"limit_value": 100}                        // Additional context
    }
  ]
}
```

**Multiple Field Errors:**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length" 
    },
    {
      "loc": ["body", "heading_deg"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

**Common Validation Issues:**
- **Name**: Empty string or > 80 characters
- **Battery**: < 0% or > 100%  
- **Heading**: < 0° or ≥ 360°
- **Swarm ID**: References non-existent swarm
- **Status**: Invalid enum value
- **Required Fields**: Missing required fields

### Debugging Tips

1. **Check the `loc` field** to identify which field caused the error
2. **Read the `msg` field** for human-readable explanation  
3. **Use Interactive Docs** at `/docs` to test requests
4. **Validate JSON syntax** before sending requests
5. **Check data types** (string vs number vs boolean)

---

## 📊 Data Models

### Core Object Schemas

#### 🔗 Swarm Object
```json
{
  "id": 1,                                    // Auto-generated, immutable
  "name": "Alpha Squadron",                   // 1-80 characters, required
  "description": "Mission description",       // Optional text
  "metadata": {                               // Optional JSON object
    "mission_type": "reconnaissance",
    "priority": "high",
    "custom_field": "any_value"
  },
  "created_at": "2025-11-05T10:30:00.123456" // ISO 8601 UTC, auto-generated
}
```

#### 🤖 Robot Object  
```json
{
  "id": 1,                                    // Auto-generated, immutable
  "name": "Rover-Alpha-1",                    // 1-80 characters, required
  "status": "active",                         // Enum: idle|active|charging|fault
  "position": {                               // 3D coordinates in meters
    "x": 10.5,                               // X-axis position  
    "y": 25.3,                               // Y-axis position
    "z": 0.0                                 // Z-axis position (altitude)
  },
  "heading_deg": 45.0,                        // 0-359.9 degrees (auto-normalized)
  "battery_pct": 85.5,                        // 0-100% battery level
  "metadata": {                               // Optional JSON object
    "model": "RX-7",
    "sensors": ["lidar", "camera"],
    "custom_data": "anything"
  },
  "swarm_id": 1,                             // null = unassigned, number = swarm ID  
  "last_seen": "2025-11-05T11:45:30.123456"  // Last telemetry update (ISO 8601 UTC)
}
```

### Enum Values

#### Robot Status States
| Status | Meaning | Typical Use |
|--------|---------|-------------|
| `idle` | Robot ready but not active | Default state, waiting for commands |
| `active` | Robot performing tasks | Moving, working, executing missions |
| `charging` | Robot charging battery | At charging station, temporarily unavailable |
| `fault` | Robot has error/malfunction | Needs maintenance, emergency state |

### Field Validation Rules

#### 📝 Text Fields
- **Names**: 1-80 characters, whitespace trimmed but preserved
- **Descriptions**: No length limit, optional
- **Metadata**: Any valid JSON structure

#### 🔢 Numeric Fields  
- **IDs**: Positive integers ≥ 1, auto-generated
- **Battery**: 0.0 ≤ value ≤ 100.0 (percentage)
- **Heading**: 0.0 ≤ value < 360.0 (degrees, auto-normalized)
- **Coordinates**: Any float value (positive/negative/zero)

#### 📅 DateTime Fields
- **Format**: ISO 8601 with microseconds (`YYYY-MM-DDTHH:MM:SS.ffffff`)
- **Timezone**: Always UTC
- **Auto-generated**: `created_at`, `last_seen` (when updated)

#### 🔗 Relationships
- **Swarm ↔ Robots**: One-to-many (swarm can have multiple robots)
- **Robot → Swarm**: Many-to-one or null (robot can be unassigned)
- **Deletion**: Deleting swarm auto-detaches all robots

---

## 🎯 Demo Data

The API starts with sample data for immediate testing:

### Pre-loaded Swarms
```json
[
  {
    "id": 1,
    "name": "Alpha", 
    "description": "Primary ops swarm",
    "metadata": {},
    "created_at": "2025-11-05T..."
  },
  {
    "id": 2,
    "name": "Bravo",
    "description": "Exploration swarm", 
    "metadata": {},
    "created_at": "2025-11-05T..."
  }
]
```

### Pre-loaded Robots
```json
[
  {
    "id": 1,
    "name": "Rover-1",
    "status": "idle",
    "position": {"x": 0, "y": 0, "z": 0},
    "heading_deg": 0,
    "battery_pct": 88,
    "swarm_id": 1,        // Assigned to Alpha swarm
    "last_seen": null
  },
  {
    "id": 2, 
    "name": "Rover-2",
    "status": "active",
    "position": {"x": 5, "y": 3, "z": 0},
    "heading_deg": 45,
    "battery_pct": 73,
    "swarm_id": 1,        // Assigned to Alpha swarm  
    "last_seen": null
  },
  {
    "id": 3,
    "name": "Scout-1", 
    "status": "charging",
    "position": {"x": -2, "y": 8, "z": 0},
    "heading_deg": 180,
    "battery_pct": 22,
    "swarm_id": null,     // Unassigned robot
    "last_seen": null
  }
]
```

**Quick Testing:**
```bash
# View demo swarms
curl http://localhost:8000/swarms

# View demo robots
curl http://localhost:8000/robots

# View Alpha swarm's robots  
curl http://localhost:8000/swarms/1/robots
```

---

## 💻 Development Notes

### 🔧 Technical Implementation

- **Framework**: FastAPI with automatic OpenAPI docs
- **Storage**: In-memory Python dictionaries (resets on restart)
- **Validation**: Pydantic models with automatic type checking
- **CORS**: Enabled for all origins (development mode)
- **Auto-docs**: Swagger UI at `/docs`, ReDoc at `/redoc`

### ⚠️ Development Limitations

- **Data Persistence**: All data lost on server restart
- **Concurrency**: No locking mechanism for concurrent updates
- **Authentication**: No security (anyone can access all endpoints)
- **Rate Limiting**: No request rate limiting
- **Database**: No persistent storage or transactions

### 🚀 Production Readiness Checklist

Before deploying to production, consider implementing:

- [ ] **Database Integration**: PostgreSQL, MongoDB, or SQLite
- [ ] **Authentication**: JWT tokens, OAuth2, or API keys  
- [ ] **Authorization**: Role-based access control
- [ ] **Rate Limiting**: Prevent API abuse
- [ ] **Logging**: Request/response logging and monitoring
- [ ] **Input Sanitization**: Additional security validation
- [ ] **HTTPS**: SSL/TLS encryption
- [ ] **Environment Config**: Separate dev/staging/prod settings
- [ ] **Error Monitoring**: Sentry, Rollbar, or similar
- [ ] **Load Balancing**: Multiple server instances
- [ ] **Backup Strategy**: Data backup and recovery
- [ ] **API Versioning**: Backwards compatibility strategy

### 🔮 Suggested Next Features

- **WebSocket Support**: Real-time robot position streaming
- **Command Queue**: Send commands to robots and track execution
- **Path Planning**: Calculate optimal routes for robots
- **Collision Detection**: Prevent robots from colliding
- **Mission Management**: Complex multi-robot missions
- **Historical Data**: Track robot movement and battery history
- **Alerts & Notifications**: Battery low, robot offline, etc.
- **Map Integration**: 2D/3D visualization of robot positions
- **Swarm Algorithms**: Coordinated swarm behaviors
- **Robot Simulation**: Virtual robot testing environment

### 📚 Useful Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Validation**: https://pydantic-docs.helpmanual.io/
- **OpenAPI Specification**: https://swagger.io/specification/
- **Python datetime**: https://docs.python.org/3/library/datetime.html