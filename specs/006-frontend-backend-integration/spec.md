# Feature Specification: Frontend-Backend Integration for RAG Chatbot

**Feature Branch**: `006-frontend-backend-integration`
**Created**: 2025-12-30
**Status**: Draft
**Input**: Connect Docusaurus frontend to FastAPI RAG backend via secure HTTP API for book-grounded chatbot responses

## User Scenarios & Testing

### User Story 1 - Ask Question and Receive Grounded Answer (Priority: P1)

A reader visits the Physical AI textbook website and has a question about a concept. They click the chat widget, type their question, and receive an accurate answer grounded in the textbook content with source citations.

**Why this priority**: This is the core value proposition - enabling readers to get instant answers without manually searching through chapters.

**Independent Test**: Open the textbook site, click the chat button, ask "What is ROS 2?", verify the response includes textbook-grounded content with clickable source links.

**Acceptance Scenarios**:

1. **Given** reader is on any textbook page, **When** they click the floating chat button, **Then** chat panel opens with welcome message
2. **Given** chat panel is open, **When** reader types "What is ROS 2?" and submits, **Then** system displays answer with source citations
3. **Given** response is displayed, **When** reader clicks a source link, **Then** browser navigates to that chapter/section
4. **Given** reader submits a query, **When** backend processes the request, **Then** response appears within 5 seconds

---

### User Story 2 - Handle Out-of-Scope Questions Gracefully (Priority: P1)

A reader asks a question that is not covered in the textbook. The chatbot clearly communicates that the information is not available rather than providing incorrect or hallucinated information.

**Why this priority**: Maintaining trust requires honest communication about coverage limits. Hallucinated answers destroy credibility.

**Independent Test**: Ask "What is the best pizza in New York?" and verify the chatbot declines with a clear message about textbook scope.

**Acceptance Scenarios**:

1. **Given** reader asks about non-robotics topic, **When** backend searches for content, **Then** system returns clear "not covered" message with suggestions
2. **Given** reader asks partially covered topic, **When** retrieval confidence is low, **Then** response includes uncertainty indicator

---

### User Story 3 - Resume Conversation Across Page Navigation (Priority: P2)

A reader starts a conversation on one page, navigates to another chapter, and continues the conversation without losing context.

**Why this priority**: Readers browse multiple chapters - conversation continuity enhances the learning experience.

**Independent Test**: Ask a question on Chapter 1, navigate to Chapter 3, ask follow-up question, verify chat history is preserved.

**Acceptance Scenarios**:

1. **Given** reader has active chat conversation, **When** they navigate to different page, **Then** chat history persists
2. **Given** reader closes chat panel, **When** they reopen it within same session, **Then** conversation history is restored

---

### User Story 4 - Receive Persona-Adapted Responses (Priority: P3)

A reader selects their expertise level (beginner, software engineer, robotics student, AI researcher) and receives explanations tailored to their background.

**Why this priority**: Enhances user experience but not critical for core functionality.

**Independent Test**: Select "Beginner" persona, ask "What is ROS 2?", verify response uses simple analogies without jargon.

**Acceptance Scenarios**:

1. **Given** reader selects "Beginner" persona, **When** they ask a question, **Then** response uses first-principles explanations
2. **Given** reader selects "AI Researcher" persona, **When** they ask same question, **Then** response assumes deep ML knowledge

---

### Edge Cases

- What happens when backend API is unreachable (network failure, server down)?
- How does system handle very long user questions (>1000 characters)?
- What occurs when user submits empty query?
- How does chat widget behave on mobile devices with small screens?
- What happens when user selects text and asks unrelated question?
- How does system handle rapid-fire queries (user sends 5 questions in 10 seconds)?
- What occurs when backend returns malformed JSON response?

## Requirements

### Functional Requirements

- **FR-001**: Chat widget MUST be accessible from all textbook pages without disrupting reading experience
- **FR-002**: System MUST display floating chat button in bottom-right corner that opens/closes chat panel
- **FR-003**: Frontend MUST send user queries to backend API via HTTP POST request
- **FR-004**: Backend MUST return responses within 5 seconds for 95% of queries
- **FR-005**: System MUST display source citations with clickable links to textbook sections
- **FR-006**: Frontend MUST indicate when responses are book-grounded vs system messages
- **FR-007**: System MUST handle greetings and simple acknowledgments without triggering retrieval
- **FR-008**: Backend MUST validate and sanitize all input before processing
- **FR-009**: System MUST preserve conversation history within browser session
- **FR-010**: Frontend MUST display loading indicator while awaiting backend response
- **FR-011**: System MUST show user-friendly error messages when backend is unavailable
- **FR-012**: Backend MUST enable CORS for frontend domain access
- **FR-013**: System MUST NOT expose API keys, database credentials, or internal configuration to frontend
- **FR-014**: Frontend MUST allow configuration of backend API endpoint URL via environment variable
- **FR-015**: System MUST support both global search and selected-text query modes
- **FR-016**: Frontend MUST auto-detect text selection and offer contextual query option
- **FR-017**: System MUST display confidence indicators for low-confidence responses
- **FR-018**: Backend MUST remain stateless - no server-side session storage required
- **FR-019**: Frontend MUST function on mobile devices with responsive layout
- **FR-020**: System MUST prevent submission of empty or whitespace-only queries

### Key Entities

- **Query**: User's question with optional mode (global/selected) and persona preference
- **Response**: Answer text with source citations, confidence level, and retrieval metadata
- **Source Citation**: Reference to textbook chapter/section with clickable URL and relevance score
- **Chat Message**: Individual message in conversation history with role (user/assistant) and content
- **Session State**: Temporary browser-side storage of conversation history and user preferences

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users receive answers to textbook questions within 5 seconds for 95% of queries
- **SC-002**: 90% of in-scope questions receive relevant grounded answers
- **SC-003**: Zero instances of hallucinated content not present in textbook
- **SC-004**: Users can navigate to source sections via citation links with 100% accuracy
- **SC-005**: Chat widget loads and renders on all textbook pages without breaking layout
- **SC-006**: System handles 50 concurrent users without performance degradation
- **SC-007**: Frontend gracefully handles backend failures with clear error messages in 100% of cases
- **SC-008**: Conversation history persists across page navigation within same browser session
- **SC-009**: Mobile users can interact with chat widget without layout issues on screens 375px+ wide
- **SC-010**: Out-of-scope questions receive appropriate decline messages rather than guessed answers

## Assumptions

- Readers have modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Backend API is deployed to accessible URL (development: localhost, production: cloud service)
- Textbook content is already indexed in vector database (Qdrant)
- No user authentication required for chatbot access
- Conversation history is session-scoped (no cross-device or persistent history)
- Frontend is deployed as static site (no server-side rendering)
- API calls are made client-side from browser (not server-side)
- HTTPS used for production deployment (HTTP acceptable for local development)
- Single language support (English) - no internationalization required

## Dependencies

- **Existing RAG Backend**: FastAPI service with /query endpoint operational
- **Vector Database**: Qdrant Cloud with indexed textbook chunks
- **Docusaurus Site**: Static site framework already deployed
- **ChatWidget Component**: React component already implemented
- **Network Connectivity**: Stable internet connection for API communication

## Out of Scope

- User authentication or authorization
- Persistent conversation history across sessions
- Multi-user chat or collaboration features
- Admin dashboard for monitoring queries
- A/B testing or analytics integration
- Customizable chat widget themes beyond existing brand colors
- Voice input or text-to-speech output
- File upload or image-based queries
- Backend deployment automation or CI/CD pipelines
- Database migration or backup strategies
- Multi-language support or localization

## Constraints

- Frontend must remain stateless static site (no backend server for frontend)
- Backend must not store user conversations or personal data
- API communication must use standard HTTP/HTTPS protocols
- Chat widget must not increase page load time by more than 500ms
- Frontend bundle size increase must not exceed 100KB
- No external JavaScript libraries beyond React (already in Docusaurus)
- CORS configuration must whitelist only known frontend domains
- API responses must be JSON format only (no HTML, XML, or custom formats)

## Frontend–Backend Integration Acceptance Criteria

### API Contract Validation

- [ ] Frontend sends POST requests to /query endpoint with correct JSON structure
- [ ] Backend accepts requests from whitelisted frontend origins (CORS configured)
- [ ] Backend returns responses in documented JSON schema
- [ ] Frontend correctly parses and displays all response fields (answer, sources, confidence)
- [ ] Error responses from backend are handled gracefully with user-friendly messages

### Connection Reliability

- [ ] Frontend displays loading state while awaiting backend response
- [ ] Frontend implements timeout (10 seconds) for API requests
- [ ] Frontend retries failed requests once before showing error
- [ ] Backend responds with appropriate HTTP status codes (200, 400, 500)
- [ ] Network failures show clear "connection lost" message to user

### Security Verification

- [ ] No API keys or credentials visible in frontend code or network requests
- [ ] CORS headers properly restrict access to approved frontend domains
- [ ] Input validation prevents injection attacks on both frontend and backend
- [ ] HTTPS enforced for production deployment

### User Experience Validation

- [ ] Chat widget renders correctly on all textbook pages
- [ ] Source links navigate to correct textbook sections
- [ ] Conversation history persists across page navigation within session
- [ ] Mobile layout adapts properly to small screens (tested on 375px width)
- [ ] Loading indicators and error states provide clear feedback

### Configuration Flexibility

- [ ] Backend API URL is configurable via frontend environment variable
- [ ] Frontend builds successfully with both development and production API URLs
- [ ] Backend CORS origins configurable via environment variable
- [ ] Both systems can be deployed independently without coupling
