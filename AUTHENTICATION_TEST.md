# 🔑 Quick Authentication Test Guide

## ✅ Fixed: Security Scheme Mismatch

**Issue:** The Swagger UI was using `BearerAuth` but the API expected `HTTPBearer`  
**Solution:** Updated the security scheme to match the API expectations

## 🧪 Test Steps:

### 1. Open the Documentation
```bash
# Option 1: Direct file
Open biobot_swagger_offline.html in browser

# Option 2: Local server (recommended)
python serve_docs.py
```

### 2. Authenticate
1. **Click** the "Authorize" button (🔒 icon in top-right)
2. **Enter** your API key: `biobot-alpha-2025-xk9f`
   - Enter JUST the key (no "Bearer" prefix)
   - Example: `biobot-alpha-2025-xk9f`
3. **Click** "Authorize"
4. **Click** "Close"

### 3. Test Authentication
1. **Try** the `/auth/info` endpoint:
   - Click on "security" section
   - Click on "GET /auth/info"
   - Click "Try it out"
   - Click "Execute"
   - **Expected:** ✅ 200 response with your API key info

### 4. Test API Functionality
1. **Try** the `/swarms` endpoint:
   - Click on "swarms" section  
   - Click on "GET /swarms"
   - Click "Try it out"
   - Click "Execute"
   - **Expected:** ✅ 200 response with swarm data

## 🔑 Valid API Keys:
- `biobot-alpha-2025-xk9f` (Read/Write)
- `biobot-beta-2025-m7p3` (Read Only)
- `biobot-gamma-2025-q4w8` (Read/Write)

## ⚠️ If Still Getting 403:
1. **Double-check** you entered the key correctly
2. **Make sure** you clicked "Authorize" after entering the key
3. **Try** a different browser or incognito mode
4. **Verify** the live API: https://swarm-api-smzv.onrender.com/

The authentication should now work correctly! 🎉