# 🤖 BioBot Swarm API - Offline Documentation

This package contains offline documentation for the BioBot Swarm Management API that you can use to test and explore the API endpoints.

## 📁 Files Included

- **`biobot_swagger_offline.html`** - Interactive Swagger documentation
- **`serve_docs.py`** - Local server to avoid CORS issues
- **`biobot_api_spec.json`** - Raw OpenAPI specification (optional)

## 🚀 Usage Options

### Option 1: Direct File Access
1. **Open** `biobot_swagger_offline.html` directly in your web browser
2. **Click** the "Authorize" button in the top-right
3. **Enter** your API key in the format: `your-api-key-here`
4. **Test** any endpoint by clicking "Try it out"

### Option 2: Local Server (Recommended)
If you encounter CORS errors with Option 1, use this method:

1. **Install Python** (if not already installed): https://python.org
2. **Run the server**:
   ```bash
   python serve_docs.py
   ```
3. **Open browser** - The documentation will open automatically at `http://localhost:8888`
4. **Authorize** with your API key and test endpoints

## 🔑 API Key Authentication

All endpoints require authentication. Use your provided API key in the "Authorize" dialog.

**Format:** Enter just the key (without "Bearer" prefix)
```
your-api-key-here
```

## 🌐 Live API Endpoint

The documentation tests against the live API at:
```
https://swarm-api-smzv.onrender.com
```

## 📋 Common Endpoints to Try

1. **`GET /auth/info`** - Test your API key and see permissions
2. **`GET /swarms`** - List all swarms
3. **`GET /biobots`** - List all biobots
4. **`GET /events`** - List recent events

## ⚠️ Troubleshooting

### CORS Errors
If you see errors like "URL scheme must be http or https for CORS request":
- **Solution:** Use Option 2 (Local Server) instead of opening the HTML file directly

### Network Failures
- **Check** that you have internet connection
- **Verify** the API endpoint is accessible: https://swarm-api-smzv.onrender.com
- **Confirm** your API key is valid using the `/auth/info` endpoint

### Authorization Issues
- **Ensure** you're using the correct API key
- **Check** that your key has the required permissions for the endpoint
- **Contact** support if your key appears to be invalid

## 🔒 Security Notes

- **Keep your API key secure** - don't share it publicly
- **Each key has specific permissions** (read, write, admin)
- **Contact support** if you suspect your key has been compromised

## 📞 Support

If you encounter any issues or need additional API keys, please contact support with:
- Your organization name
- Description of the issue
- Screenshots if applicable

---

*Generated on: November 6, 2025*  
*API Version: 1.0.0*