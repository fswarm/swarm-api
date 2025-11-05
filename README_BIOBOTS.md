# Swarm & BioBots Secure API

A comprehensive FastAPI backend for managing biobot swarms with **API key authentication**. This API provides complete CRUD operations, real-time telemetry tracking, and swarm coordination capabilities with enterprise-grade security specifically designed for biological robots.

## 🔐 Security Features

- **🔑 API Key Authentication**: Secure Bearer token authentication
- **👥 Permission-Based Access**: Read, Write, and Admin permission levels
- **🛡️ Configurable Security**: Enable/disable authentication for development
- **🔄 Key Management**: Generate, list, and revoke API keys
- **📊 Usage Tracking**: Monitor API key usage and permissions

## 🚀 Key Features

- **🦾 BioBot Management**: Complete lifecycle management of individual biobots
- **🔗 Swarm Coordination**: Group biobots into swarms for coordinated operations  
- **📡 Real-time Telemetry**: Track biobot position, battery, status, and communication
- **🔄 Dynamic Assignment**: Assign/reassign biobots between swarms on the fly
- **💾 In-Memory Storage**: Zero-configuration development environment
- **📚 Auto Documentation**: Interactive API docs with Swagger UI
- **🌐 CORS Enabled**: Ready for web-based frontends and cross-origin requests

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Authentication Setup](#-authentication-setup)
- [API Usage Examples](#-api-usage-examples)
- [Permission System](#-permission-system)
- [Security Endpoints](#-security-endpoints)
- [API Overview](#-api-overview)
- [Swarms API](#-swarms-api)
- [BioBots API](#-biobots-api)
- [Actions API](#-actions-api)
- [Data Models](#-data-models)
- [Error Handling](#-error-handling)
- [Production Deployment](#-production-deployment)

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
3. **Configure authentication** (see Authentication Setup below)
4. **Run the server**:

```bash
# Option 1: Direct execution (recommended for development)
python fastapi_swarms_backend.py

# Option 2: Using uvicorn command
uvicorn fastapi_swarms_backend:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **API Base** | http://localhost:8000 | Main API endpoint (public) |
| **Interactive Docs** | http://localhost:8000/docs | Swagger UI with auth support |
| **ReDoc** | http://localhost:8000/redoc | Alternative documentation |
| **Health Check** | http://localhost:8000/health | System status (requires auth) |
| **Auth Test** | http://localhost:8000/auth/test | Test your API key |

---

## 🔐 Authentication Setup

### Default Development Setup

The API comes with a default development key:

```bash
API Key: dev-key-12345
Permissions: read, write, admin
Usage: Authorization: Bearer dev-key-12345
```

### Environment Configuration

Create a `.env` file or set environment variables:

```bash
# Enable/disable authentication
REQUIRE_API_KEY=true

# Configure API keys (format: key:name:permissions)
API_KEYS=prod-key-abc123:Production API:read|write,admin-key-xyz789:Admin API:read|write|admin
```

### Generate Secure API Keys

Use the included generator script:

```bash
# Generate a single API key
python generate_api_key.py --name "BioBot App" --permissions "read,write"

# Generate multiple keys
python generate_api_key.py --name "BioBot Fleet" --permissions "read,write,admin" --count 3

# Generate admin key
python generate_api_key.py --name "Admin Access" --permissions "admin" --length 64
```

---

## 🔧 API Usage Examples

### Basic Authentication

All endpoints (except `/` root) require authentication:

```bash
# Test authentication
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/auth/test

# Get health status
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/health

# List biobots
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/biobots
```

### Using Different Clients

#### cURL
```bash
curl -H "Authorization: Bearer your-api-key-here" \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8000/biobots \
     -d '{"name": "New BioBot", "status": "idle"}'
```

#### Python Requests
```python
import requests

headers = {
    "Authorization": "Bearer your-api-key-here",
    "Content-Type": "application/json"
}

# Test authentication
response = requests.get("http://localhost:8000/auth/test", headers=headers)
print(response.json())

# Create a biobot
biobot_data = {
    "name": "Python BioBot",
    "status": "active",
    "position": {"x": 10, "y": 5, "z": 0},
    "battery_pct": 85
}
response = requests.post("http://localhost:8000/biobots", json=biobot_data, headers=headers)
print(response.json())
```

#### JavaScript/Fetch
```javascript
const apiKey = 'your-api-key-here';
const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
};

// Test authentication
fetch('http://localhost:8000/auth/test', { headers })
    .then(response => response.json())
    .then(data => console.log(data));

// Get biobots
fetch('http://localhost:8000/biobots', { headers })
    .then(response => response.json())
    .then(biobots => console.log(biobots));
```

---

## 📡 API Overview

All endpoints require authentication via the `Authorization` header:

```
Authorization: Bearer your-api-key-here
```

### Enhanced Health Check

#### `GET /health`

**Purpose**: Check API status with authentication info

**Response:**
```json
{
  "status": "ok",
  "swarms": 2,
  "biobots": 3,
  "authenticated_as": "Development Key",
  "api_auth_required": true
}
```

---

## 🔗 Swarms API

### Create Swarm

#### `POST /swarms`

**Required Permission**: `write`

**Request Body:**
```json
{
  "name": "Alpha BioBot Squadron",
  "description": "Primary biological operations swarm",
  "metadata": {
    "mission_type": "reconnaissance",
    "bio_type": "synthetic_organism",
    "priority": "high"
  }
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Alpha BioBot Squadron",
  "description": "Primary biological operations swarm",
  "metadata": {
    "mission_type": "reconnaissance",
    "bio_type": "synthetic_organism", 
    "priority": "high"
  },
  "created_at": "2025-11-05T10:30:00.123456"
}
```

### List Swarms

#### `GET /swarms`

**Required Permission**: `read`

### Get Swarm BioBots

#### `GET /swarms/{swarm_id}/biobots`

**Purpose**: Get all biobots currently assigned to a specific swarm

**Query Parameters:**
- `status` (optional): Filter by biobot status (`idle`, `active`, `charging`, `fault`)

**Example:**
```bash
curl -H "Authorization: Bearer dev-key-12345" \
     http://localhost:8000/swarms/1/biobots?status=active
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "BioBot-Alpha-1",
    "status": "active",
    "position": {
      "x": 10.5,
      "y": 25.3,
      "z": 0.0
    },
    "heading_deg": 45.0,
    "battery_pct": 85.5,
    "metadata": {
      "bio_type": "synthetic_organism",
      "sensors": ["bio_sensor", "chemical_detector", "gps"]
    },
    "swarm_id": 1,
    "last_seen": "2025-11-05T11:45:30.123456"
  }
]
```

---

## 🦾 BioBots API

### Create BioBot

#### `POST /biobots`

**Required Permission**: `write`

**Request Body:**
```json
{
  "name": "BioBot-Charlie-1",
  "status": "idle",
  "position": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
  },
  "heading_deg": 90.0,
  "battery_pct": 100.0,
  "metadata": {
    "bio_type": "engineered_microorganism",
    "capabilities": ["autonomous_navigation", "chemical_sensing"],
    "substrate": "nutrient_medium"
  },
  "swarm_id": 1
}
```

**Response (201):**
```json
{
  "id": 4,
  "name": "BioBot-Charlie-1",
  "status": "idle",
  "position": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
  },
  "heading_deg": 90.0,
  "battery_pct": 100.0,
  "metadata": {
    "bio_type": "engineered_microorganism",
    "capabilities": ["autonomous_navigation", "chemical_sensing"],
    "substrate": "nutrient_medium"
  },
  "swarm_id": 1,
  "last_seen": null
}
```

### List BioBots

#### `GET /biobots`

**Required Permission**: `read`

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `swarm_id` | int/null | Filter by swarm | `?swarm_id=1` |
| `status` | string | Filter by status | `?status=active` |
| `q` | string | Search by name | `?q=biobot` |
| `limit` | int | Results per page (1-500) | `?limit=20` |
| `offset` | int | Skip results | `?offset=40` |

**Example:**
```bash
curl -H "Authorization: Bearer dev-key-12345" \
     "http://localhost:8000/biobots?limit=10&status=active"
```

### Get Specific BioBot

#### `GET /biobots/{biobot_id}`

**Required Permission**: `read`

### Update BioBot

#### `POST /biobots/{biobot_id}`

**Required Permission**: `write`

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
    "bio_type": "engineered_microorganism",
    "last_feeding": "2025-11-05T10:00:00",
    "growth_phase": "exponential"
  }
}
```

### Delete BioBot

#### `DELETE /biobots/{biobot_id}`

**Required Permission**: `admin`

---

## ⚡ Actions API

### Push Telemetry

#### `POST /biobots/{biobot_id}/telemetry`

**Required Permission**: `write`

**Purpose**: Update biobot telemetry data and set last_seen timestamp

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
  "name": "BioBot-Alpha-1",
  "status": "active",
  "position": {
    "x": 20.7,
    "y": 35.4,
    "z": 1.2
  },
  "heading_deg": 275.5,
  "battery_pct": 68.3,
  "metadata": {
    "bio_type": "synthetic_organism",
    "sensors": ["bio_sensor", "chemical_detector"]
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T12:00:00.123456"
}
```

### Assign BioBot to Swarm

#### `POST /swarms/{swarm_id}/assign/{biobot_id}`

**Required Permission**: `write`

**Purpose**: Assigns a biobot to a specific swarm

### Unassign BioBot from Swarm

#### `POST /swarms/unassign/{biobot_id}`

**Required Permission**: `write`

**Purpose**: Removes a biobot from its current swarm (makes it free/unassigned)

---

## 📊 Data Models

### Core Object Schemas

#### 🔗 Swarm Object
```json
{
  "id": 1,
  "name": "Alpha BioBot Squadron",
  "description": "Primary biological operations swarm",
  "metadata": {
    "mission_type": "environmental_monitoring",
    "bio_compatibility": "aerobic_organisms",
    "temperature_range": "15-35C"
  },
  "created_at": "2025-11-05T10:30:00.123456"
}
```

#### 🦾 BioBot Object  
```json
{
  "id": 1,
  "name": "BioBot-Alpha-1",
  "status": "active",
  "position": {
    "x": 10.5,
    "y": 25.3,
    "z": 0.0
  },
  "heading_deg": 45.0,
  "battery_pct": 85.5,
  "metadata": {
    "bio_type": "engineered_microorganism",
    "substrate": "nutrient_medium",
    "generation": 3,
    "last_feeding": "2025-11-05T10:00:00"
  },
  "swarm_id": 1,
  "last_seen": "2025-11-05T11:45:30.123456"
}
```

### BioBot Status States

| Status | Meaning | Typical Use |
|--------|---------|-------------|
| `idle` | BioBot ready but not active | Default state, waiting for commands |
| `active` | BioBot performing tasks | Moving, working, executing missions |
| `charging` | BioBot charging/feeding | At feeding station, replenishing energy |
| `fault` | BioBot has error/malfunction | Needs maintenance, biological stress |

### BioBot-Specific Metadata Fields

Common metadata fields for biobots:

```json
{
  "bio_type": "engineered_microorganism",     // Type of biological system
  "substrate": "nutrient_medium",             // Energy/food source
  "generation": 3,                            // Generation number
  "growth_phase": "exponential",              // Current biological phase
  "last_feeding": "2025-11-05T10:00:00",     // Last feeding time
  "temperature": 23.5,                        // Operating temperature
  "ph_level": 7.2,                           // Environmental pH
  "oxygen_level": 95.0,                      // O2 saturation percentage
  "reproduction_cycle": "72_hours",          // Reproduction timing
  "genetic_markers": ["GFP", "antibiotic_resistance"]
}
```

---

## 🎯 Demo Data

The API starts with sample biobot data for immediate testing:

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

### Pre-loaded BioBots
```json
[
  {
    "id": 1,
    "name": "BioBot-1",
    "status": "idle",
    "position": {"x": 0, "y": 0, "z": 0},
    "heading_deg": 0,
    "battery_pct": 88,
    "swarm_id": 1,
    "last_seen": null
  },
  {
    "id": 2, 
    "name": "BioBot-2",
    "status": "active",
    "position": {"x": 5, "y": 3, "z": 0},
    "heading_deg": 45,
    "battery_pct": 73,
    "swarm_id": 1,
    "last_seen": null
  },
  {
    "id": 3,
    "name": "Scout-Bio", 
    "status": "charging",
    "position": {"x": -2, "y": 8, "z": 0},
    "heading_deg": 180,
    "battery_pct": 22,
    "swarm_id": null,
    "last_seen": null
  }
]
```

**Quick Testing:**
```bash
# View demo swarms
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/swarms

# View demo biobots
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/biobots

# View Alpha swarm's biobots  
curl -H "Authorization: Bearer dev-key-12345" http://localhost:8000/swarms/1/biobots
```

---

## 🚀 Production Deployment

### BioBot-Specific Considerations

For biological robot systems, additional considerations include:

- [ ] **Environmental Monitoring**: Temperature, pH, oxygen sensors
- [ ] **Biological Safety**: Containment protocols and fail-safes
- [ ] **Nutrient Management**: Feeding schedules and substrate monitoring
- [ ] **Reproduction Control**: Genetic stability and population limits
- [ ] **Waste Management**: Metabolic byproduct handling
- [ ] **Sterilization Protocols**: Between-mission decontamination
- [ ] **Genetic Tracking**: Lineage and mutation monitoring
- [ ] **Regulatory Compliance**: Biosafety and ethics approvals

### Security for Biological Systems

```bash
# Environment Variables for BioBot Production
REQUIRE_API_KEY=true
API_KEYS=biolab-key-xyz:BioLab Control:read|write,safety-key-abc:Safety Monitor:read|write|admin

# BioBot-specific settings
BIO_SAFETY_LEVEL=2
CONTAINMENT_PROTOCOLS=enabled
GENETIC_MONITORING=enabled
ENVIRONMENTAL_LIMITS=temperature:15-35,ph:6.5-8.0,oxygen:80-100
```

---

Your API is now fully converted to handle BioBots instead of robots! 🦾🔬

**Key Changes Made:**
- ✅ **Robot → BioBot**: All models, endpoints, and functions renamed
- ✅ **RobotStatus → BioBotStatus**: Enum class renamed
- ✅ **Updated Endpoints**: `/robots` → `/biobots`, `/robot_id` → `/biobot_id`
- ✅ **Demo Data**: Sample biobots with bio-specific naming
- ✅ **Documentation**: Complete README with BioBot-specific examples
- ✅ **Metadata Examples**: BioBot-specific metadata fields
- ✅ **Production Notes**: BioBot-specific deployment considerations

The API now provides comprehensive management for biological robot swarms with enterprise-grade security! 🤖🧬✨