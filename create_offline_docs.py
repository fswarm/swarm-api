"""
Script to generate offline Swagger documentation for BioBot Swarm API
This creates a standalone HTML file that customers can open in their browser
and test against the live API endpoint.
"""

import json
import sys
import os

# Add the current directory to Python path to import swarm_api
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from swarm_api import app
    from fastapi.openapi.utils import get_openapi
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this script from the same directory as swarm_api.py")
    exit(1)

def create_offline_swagger():
    """Generate offline Swagger documentation"""
    
    print("🚀 Generating offline Swagger documentation...")
    
    # Generate OpenAPI specification
    openapi_schema = get_openapi(
        title="BioBot Swarm Management API",
        version="1.0.0",
        description="Production-ready API for managing autonomous biobot swarms with real-time telemetry and geographic positioning",
        routes=app.routes,
    )
    
    # Add server information for live API
    openapi_schema["servers"] = [
        {
            "url": "https://swarm-api-smzv.onrender.com",
            "description": "Production API Server"
        }
    ]
    
    # Add security scheme information
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "API Key",
            "description": "Enter your API key in the Authorization header"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"HTTPBearer": []}]
    
    # Save OpenAPI JSON for reference
    with open("biobot_api_spec.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    # Create standalone HTML with embedded Swagger UI
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BioBot Swarm API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5.9.0/favicon-32x32.png" sizes="32x32" />
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        
        .simple-header {{
            background: #f8f9fa;
            padding: 10px 20px;
            text-align: center;
            border-bottom: 1px solid #dee2e6;
            font-size: 14px;
            color: #6c757d;
        }}
        
        .swagger-ui .topbar {{
            display: none;
        }}
    </style>
</head>
<body>
    <div class="simple-header">
        API Documentation - Enter your API key using the "Authorize" button
    </div>
    
    <div id="swagger-ui"></div>
    
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            // OpenAPI specification embedded directly
            const spec = {json.dumps(openapi_schema, indent=2)};
            
            // Initialize Swagger UI
            const ui = SwaggerUIBundle({{
                spec: spec,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                docExpansion: "list",
                operationsSorter: "method",
                tryItOutEnabled: true
            }});
            
            window.ui = ui;
        }};
    </script>
</body>
</html>"""
    
    # Write the HTML file
    with open("biobot_swagger_offline.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Offline Swagger documentation created successfully!")
    print("\n📁 Generated files:")
    print("  📄 biobot_swagger_offline.html - Interactive documentation (open in browser)")
    print("  📄 biobot_api_spec.json - OpenAPI specification (for reference)")
    print("\n🚀 Usage Options:")
    print("  📋 Option 1 - Direct File Access:")
    print("    1. Open 'biobot_swagger_offline.html' directly in browser")
    print("    2. Click 'Authorize' and enter API key")
    print("    3. Test endpoints against live API")
    print("  ")
    print("  🌐 Option 2 - Local Server (Recommended for CORS issues):")
    print("    1. Run: python serve_docs.py")
    print("    2. Opens automatically at http://localhost:8888")
    print("    3. No CORS issues, full functionality")
    print("\n⚠️  If you see CORS errors with Option 1, use Option 2!")
    print("\n🔑 Sample API keys to share with customers:")
    print("  - biobot-alpha-2025-xk9f (Read/Write)")
    print("  - biobot-beta-2025-m7p3 (Read Only)")
    print("  - biobot-gamma-2025-q4w8 (Read/Write)")

if __name__ == "__main__":
    create_offline_swagger()