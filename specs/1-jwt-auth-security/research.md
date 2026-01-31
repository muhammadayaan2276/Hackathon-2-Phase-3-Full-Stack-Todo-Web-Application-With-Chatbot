# Research Summary: JWT Authentication & Security for Todo Application

## Decision 1: Token Refresh Strategy

**Decision**: Implement basic refresh tokens with short-lived access tokens (15-minute access tokens, 7-day refresh tokens)

**Rationale**: 
- Provides better user experience than requiring re-authentication every 15 minutes
- Maintains security by using short-lived access tokens
- Refresh tokens can be stored securely and rotated
- Aligns with industry best practices for web applications

**Alternatives Considered**:
- **No refresh tokens**: Simpler but poor UX (users must re-authenticate frequently)
- **Long-lived access tokens**: Better UX but higher security risk if token is compromised
- **Rotating refresh tokens**: Highest security but more complex implementation

**Implementation Guidance**:
- Access tokens: 15 minutes lifetime
- Refresh tokens: 7 days lifetime, stored in HttpOnly cookies
- Refresh endpoint: POST `/api/auth/refresh` requiring valid refresh token
- On refresh, issue new access token and new refresh token (rotation)

## Decision 2: Authentication Error Messages

**Decision**: Use generic error messages that don't distinguish between non-existent users and invalid passwords

**Rationale**:
- Prevents user enumeration attacks (security best practice)
- OWASP recommends consistent error messages for authentication failures
- Maintains security while providing sufficient feedback for legitimate users

**Specific Implementation**:
- For both invalid credentials and non-existent users: "Invalid email or password"
- For expired tokens: "Session expired. Please sign in again."
- For invalid tokens: "Invalid session. Please sign in again."

**Alternatives Considered**:
- **Detailed errors**: Better UX but enables enumeration attacks
- **Different errors for different cases**: Compromises security for usability
- **Generic but helpful**: "Authentication failed" - too vague for users

## Decision 3: Non-existent Task Handling

**Decision**: Return 404 Not Found for non-existent tasks, regardless of ownership

**Rationale**:
- Follows REST API conventions (resource not found = 404)
- Provides clear feedback to clients about resource existence
- Security impact is minimal since task IDs are UUIDs (hard to enumerate)
- Better developer experience than ambiguous 403 responses

**Security Considerations**:
- Task IDs will be UUIDs (128-bit), making enumeration practically impossible
- Rate limiting at infrastructure level will prevent brute force attempts
- 404 responses don't reveal whether a task exists for a specific user

**Alternatives Considered**:
- **403 Forbidden**: Better security against enumeration but violates REST principles
- **404 for GET, 403 for POST/PUT/DELETE**: Inconsistent behavior, confusing for developers
- **Generic 400 Bad Request**: Too vague, doesn't follow HTTP semantics

## Additional Research Findings

### JWT Best Practices
- Use HS256 algorithm with 256-bit+ secret key
- Include `iat` (issued at) and `exp` (expiration) claims
- Add `jti` (JWT ID) for token revocation if needed later
- Validate `aud` (audience) and `iss` (issuer) claims

### Better Auth Integration
- Configure with `secret` from `BETTER_AUTH_SECRET` environment variable
- Set `jwtExpiresIn` to 15 minutes for access tokens
- Enable `useHttpOnlyCookies` for secure token storage
- Configure `cookieDomain` appropriately for production

### FastAPI JWT Middleware
- Use `python-jose` library for JWT verification
- Implement custom middleware class for request processing
- Cache verified tokens per request to avoid repeated verification
- Handle token extraction from Authorization header and cookies

### Security Hardening
- Add rate limiting for authentication endpoints
- Implement request validation for all inputs
- Sanitize all error messages to prevent information leakage
- Use HTTPS in production (assumed as standard)

## Summary of Decisions
1. ✅ Refresh tokens: 15-min access, 7-day refresh
2. ✅ Generic error messages: "Invalid email or password" for auth failures
3. ✅ 404 Not Found: for non-existent tasks (UUID-based IDs)