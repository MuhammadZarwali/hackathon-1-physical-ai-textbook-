# Manual Testing Guide - Frontend-Backend Integration

**Status**: ✅ Backend running on http://localhost:8001
**Status**: ✅ Frontend running on http://localhost:3000

---

## Quick Start Testing

1. **Open Browser**: Navigate to http://localhost:3000
2. **Look for Chat Button**: Bottom-right corner (teal circular button with chat icon)
3. **Click to Open**: Chat panel should slide up from bottom

---

## Test Suite - All User Stories

### ✅ User Story 1: Ask Question and Receive Grounded Answer (MVP)

**Objective**: Verify basic query/response flow with source citations

#### Test MT001-MT006: Basic Query Flow

1. **Open Chat Widget**
   - Click the teal chat button in bottom-right corner
   - ✓ Chat panel slides up with welcome message
   - ✓ Welcome message says "Hi! I can answer questions about the Physical AI & Humanoid Robotics textbook"
   - ✓ Hint text suggests topics: ROS 2, digital twins, NVIDIA Isaac, VLA models

2. **Ask a Question**
   - Type: `What is ROS 2?`
   - Click send button (paper plane icon) or press Enter
   - ✓ Your question appears in teal bubble on right side
   - ✓ Loading indicator appears (three bouncing dots)
   - ✓ Input field is disabled during loading (grayed out)

3. **Verify Response**
   - Wait for response (may take 10-60 seconds for first query)
   - ✓ Response appears in gray bubble on left side
   - ✓ Answer includes textbook-grounded information about ROS 2
   - ✓ "Sources:" section displays below the answer
   - ✓ Multiple source citations are listed (e.g., "Chapter 1 - Introduction to ROS 2")
   - ✓ Each source shows relevance score percentage (e.g., "95%")

4. **Test Source Links**
   - Click any source link in the chat response
   - ✓ Browser navigates to the correct textbook section
   - ✓ URL changes to match the source (e.g., `/module-1-ros2/chapter-1-introduction-to-ros2`)

5. **Test Loading State**
   - Ask another question: `What is Gazebo?`
   - ✓ Previous messages remain visible
   - ✓ New question appears immediately
   - ✓ Loading indicator appears again
   - ✓ Cannot submit another question while loading

6. **Verify Chat Persists**
   - ✓ All previous messages remain visible in chronological order
   - ✓ Newest messages are at the bottom
   - ✓ Chat automatically scrolls to show latest message

**Expected Results**:
- Response time: 5-60 seconds (depending on backend performance)
- Answer is book-grounded (no hallucinated content about pizza or unrelated topics)
- Sources are clickable and navigate to correct pages
- Loading indicator provides feedback during wait

---

### ✅ User Story 2: Handle Out-of-Scope Questions Gracefully

**Objective**: Verify clear "not covered" messages for questions outside textbook scope

#### Test MT007-MT010: Out-of-Scope Handling

1. **Ask Out-of-Scope Question**
   - Type: `What is the best pizza in New York?`
   - Click send
   - Wait for response

2. **Verify "Not Covered" Response**
   - ✓ Response clearly states topic is not covered in textbook
   - ✓ Message suggests topics that ARE covered (ROS 2, Gazebo, Isaac, VLA)
   - ✓ No hallucinated pizza recommendations appear
   - ✓ Confidence badge shows "Not found" (gray badge)

3. **Test Low-Confidence Response**
   - Ask: `What is the weather like?`
   - ✓ Response indicates uncertainty or "not covered"
   - ✓ Low confidence or none badge appears

4. **Verify No Hallucination**
   - ✓ System does NOT make up fake information about unrelated topics
   - ✓ System stays within textbook domain boundaries

**Expected Results**:
- Clear messaging when topic not covered
- Confidence badges visible (gray "Not found" or red "Low confidence")
- No hallucinated content outside textbook scope

---

### ✅ User Story 3: Resume Conversation Across Page Navigation

**Objective**: Verify chat history persists when navigating between pages

#### Test MT011-MT015: Conversation Persistence

1. **Ask Question on First Page**
   - Current page: http://localhost:3000 (homepage)
   - Ask: `What is ROS 2?`
   - Wait for response
   - ✓ Response appears with sources

2. **Navigate to Different Page**
   - Click any link in the navbar or sidebar
   - Navigate to: Module 1 → Chapter 1 (or any other page)
   - ✓ URL changes to new page
   - ✓ Chat panel remains open (if it was open)

3. **Verify History Preserved**
   - Look at chat panel
   - ✓ Previous question and answer still visible
   - ✓ All source citations preserved
   - ✓ Message order maintained

4. **Close and Reopen Chat**
   - Click X button to close chat panel
   - Navigate to another page
   - Click chat button to reopen
   - ✓ All previous messages restored from sessionStorage
   - ✓ Chat state matches before closing

5. **Ask Follow-Up Question**
   - Ask: `What about Gazebo?`
   - ✓ New question appears after previous conversation
   - ✓ Context maintained (backend may use conversation history)

6. **Test Clear History Button**
   - Look for trash icon button in chat header (next to persona dropdown)
   - Click the "Clear History" button
   - ✓ All messages disappear
   - ✓ Welcome message reappears
   - ✓ Clean slate for new conversation

7. **Verify History Clears on Tab Close**
   - Close the browser tab completely
   - Open new tab to http://localhost:3000
   - Open chat widget
   - ✓ Chat history is empty (sessionStorage cleared)

**Expected Results**:
- Conversation persists across page navigation within same session
- Chat panel state (open/closed) preserved
- Clear History button removes all messages
- History clears when browser tab/window closes

---

### ✅ User Story 4: Receive Persona-Adapted Responses

**Objective**: Verify responses adapt to selected expertise level

#### Test MT016-MT020: Persona Adaptation

1. **Test Default Persona (All Audiences)**
   - Ensure persona dropdown shows "All audiences"
   - Ask: `What is a neural network?`
   - Note the response style (balanced technical detail)

2. **Test Beginner Persona**
   - Click persona dropdown in chat header
   - Select: "Beginner"
   - ✓ Dropdown updates to show "Beginner"
   - Ask: `What is a neural network?`
   - Wait for response
   - ✓ Response uses simple language, analogies, minimal jargon
   - ✓ Explanations are more detailed and introductory

3. **Test AI Researcher Persona**
   - Change persona dropdown to: "AI Researcher"
   - Ask the same question: `What is a neural network?`
   - ✓ Response is more technical and concise
   - ✓ Uses advanced terminology and mathematical concepts
   - ✓ Assumes prior knowledge

4. **Test Software Engineer Persona**
   - Select: "Software Engineer"
   - Ask: `How do I use ROS 2 in Python?`
   - ✓ Response focuses on practical implementation details
   - ✓ Includes code examples and API references

5. **Test Robotics Student Persona**
   - Select: "Robotics Student"
   - Ask: `What is inverse kinematics?`
   - ✓ Response balances theory and practice
   - ✓ Educational tone with academic context

6. **Verify Persona Persistence**
   - Keep persona set to "Beginner"
   - Navigate to different page
   - Return and check chat
   - ✓ Persona dropdown still shows "Beginner"
   - ✓ Persona selection persists across navigation

7. **Test Persona in Request**
   - Open browser DevTools (F12) → Network tab
   - Ask a question with persona selected
   - Look at the POST request to `/query`
   - ✓ Request body includes `"persona": "beginner"` (or selected persona)

**Expected Results**:
- Persona dropdown visible in chat header
- Response style adapts to selected persona
- Persona selection persists across page navigation
- Persona included in API request payload

---

### ✅ Error Handling & Edge Cases

**Objective**: Verify robust error handling for network failures, timeouts, and invalid inputs

#### Test MT021-MT025: Error Handling

1. **Test Network Failure**
   - Stop the backend server:
     - Find the terminal running `python main_cohere.py`
     - Press `Ctrl+C` to stop it
   - In browser, ask: `What is ROS 2?`
   - ✓ Error message appears: "Connection failed: Unable to connect to the chatbot server..."
   - ✓ Error message is user-friendly (not technical stack trace)
   - ✓ No console errors crash the app
   - **Restart backend** before continuing: `cd physical-ai-textbook/rag-backend && python main_cohere.py`

2. **Test Empty Query Prevention**
   - Click in the input field
   - Try to submit without typing anything (just click send)
   - ✓ Send button is disabled (grayed out)
   - Try typing only spaces: `     `
   - ✓ Send button remains disabled
   - ✓ No network request made

3. **Test Long Query Limit**
   - Copy-paste a very long question (>1000 characters)
   - Click send
   - ✓ Error message appears: "Your question is too long (maximum 1000 characters)..."
   - ✓ No network request made

4. **Test Rapid-Fire Queries**
   - Quickly type and submit 5 questions in rapid succession:
     - `What is ROS 2?` (send)
     - `What is Gazebo?` (send)
     - `What is Isaac Sim?` (send)
     - `What is VLA?` (send)
     - `What is DDS?` (send)
   - ✓ Input field disables after first submission
   - ✓ Subsequent attempts are ignored until first query completes
   - ✓ Only one request processes at a time
   - ✓ No race conditions or duplicate responses

5. **Test Timeout Handling** (if backend is very slow)
   - If a query takes longer than 10 seconds:
   - ✓ Error message appears: "Timeout: The server is taking too long to respond..."
   - ✓ Request is cancelled using AbortController
   - ✓ User can submit new query after timeout

6. **Test Component Unmount Cleanup**
   - Submit a query
   - While loading, quickly navigate to different page
   - ✓ No memory leaks occur
   - ✓ In-flight request is cancelled (AbortController cleanup)

**Expected Results**:
- User-friendly error messages for all error types
- Empty queries prevented at UI level
- Long queries rejected with clear message
- Only one query processes at a time
- Timeout after 10 seconds with retry logic
- Clean unmount with no memory leaks

---

## Mobile Responsiveness Testing

**Objective**: Verify chat widget works on mobile devices (375px+ width)

#### Test MT026: Mobile Layout

1. **Open DevTools Responsive Mode**
   - Press `F12` to open DevTools
   - Click "Toggle device toolbar" icon (or `Ctrl+Shift+M`)
   - Select device: "iPhone SE" (375px width) or "iPhone 12 Pro" (390px)

2. **Verify Mobile Layout**
   - ✓ Chat button visible in bottom-right (smaller positioning)
   - ✓ Chat button not too close to screen edges (10px margin)
   - Click chat button
   - ✓ Chat panel expands to `calc(100vw - 20px)` width (full width minus margins)
   - ✓ Chat panel height is `calc(100vh - 100px)` (full height minus space for button)
   - ✓ Messages are readable (text not cut off)
   - ✓ Input field and send button properly sized
   - ✓ Persona dropdown fits in header

3. **Test Touch Interactions**
   - ✓ Buttons are touch-friendly (minimum 44px touch targets)
   - ✓ Scrolling works smoothly in message area
   - ✓ No horizontal scroll on page

**Expected Results**:
- Chat widget fully responsive at 375px and above
- All elements visible and usable on mobile
- No layout breaking or content overflow

---

## Dark Mode Testing

**Objective**: Verify chat widget properly supports dark theme

#### Test MT027: Dark Mode

1. **Enable Dark Mode**
   - Click the theme toggle in the navbar (sun/moon icon)
   - Select "Dark" mode
   - ✓ Page background changes to dark

2. **Verify Chat Widget Dark Mode**
   - Open chat widget
   - ✓ Chat panel background is dark (`#1e293b`)
   - ✓ Chat header has dark gradient (`#0f172a` to `#020617`)
   - ✓ Message bubbles are dark-themed:
     - User messages: Same teal gradient (good contrast)
     - Assistant messages: Dark gray background (`#334155`) with light text
   - ✓ Sources section has dark background (`#0f172a`)
   - ✓ Source links are teal (`#5eead4`) with good contrast
   - ✓ Input field is dark (`#0f172a`) with light text
   - ✓ All text is readable with sufficient contrast

3. **Test Mode Indicator in Dark Mode**
   - Select some text on the page
   - ✓ Mode indicator background is dark teal (`#134e4a`)
   - ✓ Text color is light teal (`#5eead4`)

**Expected Results**:
- All chat widget elements properly themed for dark mode
- Good contrast ratios for accessibility
- No white flashes or unthemed elements

---

## Browser Compatibility Testing

**Objective**: Verify chat widget works on all target browsers

#### Test MT028: Cross-Browser Compatibility

**Target Browsers**: Chrome, Firefox, Safari, Edge (last 2 versions)

1. **Test in Chrome/Edge** (already done if using Chrome)
   - ✓ All features work
   - ✓ No console errors

2. **Test in Firefox**
   - Open http://localhost:3000 in Firefox
   - Run through basic tests (MT001-MT006)
   - ✓ Chat widget loads and functions
   - ✓ Fetch API works
   - ✓ AbortController works (timeout handling)
   - ✓ SessionStorage works (conversation persistence)

3. **Test in Safari** (if on macOS)
   - Open http://localhost:3000 in Safari
   - Run through basic tests
   - ✓ All features work
   - ✓ Modern JavaScript syntax supported

**Expected Results**:
- Feature parity across all target browsers
- No browser-specific bugs
- Polyfills not needed (modern browsers only)

---

## Performance Testing

**Objective**: Verify frontend bundle size and page load time within requirements

#### Test MT029: Performance Metrics

1. **Measure Bundle Size**
   - Build production bundle:
     ```bash
     cd physical-ai-textbook/docs
     npm run build
     ```
   - Check build output for bundle sizes
   - Look for `main.[hash].js` size
   - ✓ ChatWidget code adds less than 100KB to bundle (compressed)

2. **Measure Page Load Time**
   - Open DevTools → Performance tab
   - Record page load
   - Check "First Contentful Paint" and "Time to Interactive"
   - ✓ ChatWidget impact is less than 500ms on page load
   - ✓ Chat button renders quickly (part of initial bundle)
   - ✓ No blocking JavaScript execution

3. **Measure Query Response Time**
   - Open DevTools → Network tab
   - Submit query: `What is ROS 2?`
   - Find POST request to `/query`
   - ✓ 95% of queries complete within 5 seconds (backend performance)
   - ✓ Frontend handles timeout after 10 seconds

**Expected Results**:
- Bundle size increase < 100KB
- Page load impact < 500ms
- Query response time < 5s for 95% of queries

---

## Security Testing

**Objective**: Verify no API keys or sensitive data exposed to browser

#### Test MT030: Security Verification

1. **Check Network Tab**
   - Open DevTools → Network tab
   - Submit a query
   - Click on the `/query` request → Headers tab
   - ✓ No API keys in request headers
   - ✓ Only `Content-Type: application/json` header sent
   - ✓ Request body only contains: question, mode, selected_text, persona

2. **Check Response Body**
   - Click on the `/query` request → Response tab
   - ✓ Response only contains: answer, sources, confidence, mode_used, chunks_retrieved
   - ✓ No API keys, database credentials, or internal URLs exposed

3. **Check Environment Variables**
   - Open DevTools → Console
   - Type: `window.process` or `import.meta.env`
   - ✓ Only `API_URL` is exposed via customFields
   - ✓ No backend API keys visible

4. **Verify HTTPS** (in production)
   - When deployed to production:
   - ✓ Site uses HTTPS (not HTTP)
   - ✓ No mixed content warnings
   - ✓ API calls use HTTPS

**Expected Results**:
- No sensitive data exposed to browser
- Only public API URL visible
- Secure HTTPS communication in production

---

## CORS Testing

**Objective**: Verify CORS configuration allows frontend-backend communication

#### Test MT031: CORS Verification

1. **Check CORS Headers**
   - Open DevTools → Network tab
   - Submit a query
   - Click on `/query` request → Headers tab → Response Headers
   - ✓ `Access-Control-Allow-Origin` includes `http://localhost:3000`
   - ✓ `Access-Control-Allow-Methods` includes `POST`
   - ✓ `Access-Control-Allow-Headers` includes `Content-Type`

2. **Verify No CORS Errors**
   - Open DevTools → Console
   - Submit multiple queries
   - ✓ No red CORS error messages in console
   - ✓ Queries succeed without preflight errors

3. **Test Preflight Request** (if applicable)
   - Look for OPTIONS request before POST request
   - ✓ OPTIONS request succeeds with 200 OK
   - ✓ POST request follows and succeeds

**Expected Results**:
- CORS properly configured on backend
- No CORS errors in browser console
- All frontend origins whitelisted in backend `.env`

---

## Production Deployment Testing

**Note**: These tests are for when backend/frontend are deployed to Railway/Vercel

#### Test MT032-MT033: Production Integration

1. **Update Production URLs**
   - Deploy backend to Railway (get URL like `https://your-backend.railway.app`)
   - Update `physical-ai-textbook/docs/.env.production` with Railway URL
   - Update Railway `CORS_ORIGINS` environment variable with Vercel URL
   - Deploy frontend to Vercel

2. **Test Production Site**
   - Open production URL: `https://your-project.vercel.app`
   - Run through all manual tests (MT001-MT031) on production site
   - ✓ All features work identically to local development
   - ✓ API calls succeed to Railway backend
   - ✓ CORS properly configured with production URLs
   - ✓ HTTPS enforced on both frontend and backend

---

## Summary Checklist

**Phase 1-7**: ✅ All implementation tasks complete (50/54 tasks)

**User Story 1 (MVP)**:
- [ ] MT001: Chat button visible
- [ ] MT002: Chat panel opens with welcome
- [ ] MT003: Query "What is ROS 2?" succeeds
- [ ] MT004: Source citations display
- [ ] MT005: Source links navigate
- [ ] MT006: Loading indicator works

**User Story 2 (Out-of-Scope)**:
- [ ] MT007: Out-of-scope question handled gracefully
- [ ] MT008: "Not covered" message clear
- [ ] MT009: No hallucinations
- [ ] MT010: Low confidence indicator works

**User Story 3 (Persistence)**:
- [ ] MT011: History persists across navigation
- [ ] MT012: Chat state preserved
- [ ] MT013: Follow-up questions work
- [ ] MT014: Clear History button works
- [ ] MT015: History clears on tab close

**User Story 4 (Persona)**:
- [ ] MT016: Persona dropdown works
- [ ] MT017: Beginner persona uses simple language
- [ ] MT018: AI Researcher persona is technical
- [ ] MT019: Persona persists across navigation
- [ ] MT020: Persona included in API request

**Error Handling**:
- [ ] MT021: Network failure error message
- [ ] MT022: Empty query prevented
- [ ] MT023: Long query rejected
- [ ] MT024: Rapid-fire queries handled
- [ ] MT025: Component cleanup works

**Polish & Production**:
- [ ] MT026: Mobile responsive (375px+)
- [ ] MT027: Dark mode works
- [ ] MT028: Cross-browser compatible
- [ ] MT029: Performance within limits
- [ ] MT030: No security issues
- [ ] MT031: CORS configured correctly
- [ ] MT032: Production site works
- [ ] MT033: All features work in production

---

## Troubleshooting Common Issues

**Issue**: Chat button not visible
- **Fix**: Check that `ChatWidget` is imported in Docusaurus layout

**Issue**: "Failed to fetch" error
- **Fix**: Verify backend is running on port 8001 (`curl http://localhost:8001/health`)
- **Fix**: Check `API_URL` in Docusaurus config matches backend URL

**Issue**: CORS errors in console
- **Fix**: Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`
- **Fix**: Restart backend after changing CORS settings

**Issue**: Empty responses or 500 errors
- **Fix**: Check backend terminal for error logs
- **Fix**: Verify all API keys (COHERE_API_KEY, QDRANT_API_KEY) are set correctly
- **Fix**: Ensure Qdrant collection exists and has data (106 chunks expected)

**Issue**: Conversation not persisting
- **Fix**: Check browser console for sessionStorage errors
- **Fix**: Verify browser supports sessionStorage (not in incognito mode with restricted storage)

**Issue**: Persona not affecting responses
- **Fix**: Check Network tab to confirm persona is included in request body
- **Fix**: Verify backend processes persona field correctly

---

## Next Steps After Testing

1. **Mark all manual tests complete** in `specs/006-frontend-backend-integration/tasks.md`
2. **Document any issues found** during testing
3. **Fix bugs** if any are discovered
4. **Proceed with deployment** (Tasks T049-T052) to Railway and Vercel
5. **Run production tests** to verify end-to-end integration

---

**Testing Status**: Ready for manual verification
**Local Servers**: Backend (8001) ✅ | Frontend (3000) ✅
**Estimated Testing Time**: 30-45 minutes for complete test suite
