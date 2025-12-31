# Fix: Connection Failed Error

## Problem
The frontend shows: **"Connection failed: Unable to connect to the chatbot server. Please check your internet connection."**

## Root Cause
Docusaurus wasn't loading the `.env.development` file, so environment variables weren't being read properly.

## Solution Applied
1. ✅ Installed `dotenv` package
2. ✅ Updated `docusaurus.config.ts` to load `.env.development` file
3. ⏳ **Frontend dev server needs to be restarted** to pick up changes

---

## Steps to Fix

### 1. Stop the Frontend Dev Server
Find the terminal running `npm start` and press **Ctrl+C** to stop it.

### 2. Restart the Frontend
```bash
cd physical-ai-textbook/docs
npm start
```

Wait for the message: `[SUCCESS] Docusaurus website is running at: http://localhost:3000/`

### 3. Test the Connection
1. Open browser to http://localhost:3000
2. Click the chat button (bottom-right corner)
3. Ask: "What is ROS 2?"
4. You should now get a response without connection errors

---

## Verification

After restarting, the frontend will:
- ✅ Load `API_URL` from `.env.development` file
- ✅ Use `http://localhost:8001` as the backend URL
- ✅ Successfully connect to the backend
- ✅ Display responses with source citations

---

## What Was Changed

**File**: `physical-ai-textbook/docs/docusaurus.config.ts`

**Before**:
```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)
```

**After**:
```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import * as dotenv from 'dotenv';

// Load environment variables from .env.development or .env.production
dotenv.config({ path: process.env.NODE_ENV === 'production' ? '.env.production' : '.env.development' });

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)
```

**Packages Installed**:
```bash
npm install dotenv --save-dev
```

---

## Troubleshooting

### If Error Persists After Restart:

**1. Verify Backend is Running**
```bash
curl http://localhost:8001/health
```
Expected output: `{"status":"healthy","service":"rag-chatbot",...}`

**2. Check Frontend Console (F12)**
- Open browser DevTools (F12)
- Go to Console tab
- Look for any error messages
- Check Network tab for failed requests

**3. Verify Environment Variable Loaded**
After restart, add this to browser console:
```javascript
window.docusaurus.siteConfig.customFields.API_URL
```
Should output: `"http://localhost:8001"`

**4. Check CORS Configuration**
In backend `.env` file, verify:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://hackathon-1-physical-ai-textbook-phi.vercel.app
```

**5. Clear Browser Cache**
- Press `Ctrl+Shift+Delete`
- Clear cached images and files
- Reload page

---

## Alternative: Use Fallback URL

If environment variables still don't load, the fallback URL should work:

**In `docusaurus.config.ts` line 38**:
```typescript
API_URL: process.env.API_URL || 'http://localhost:8001',
```

The fallback `'http://localhost:8001'` should be used if `process.env.API_URL` is undefined.

However, with dotenv now configured, the `.env.development` file should be loaded correctly.

---

## Summary

✅ **Fixed**: Added dotenv configuration to load environment variables
⏳ **Action Required**: Restart frontend dev server (`npm start`)
🎯 **Expected Result**: Chat widget connects successfully to backend

**Next**: After restarting, test the connection and continue with manual testing from `MANUAL_TESTING_GUIDE.md`
