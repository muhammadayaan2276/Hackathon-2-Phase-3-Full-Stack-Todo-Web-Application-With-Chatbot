# Research Decisions: Responsive Todo UI

## Clarification 1: Token Storage Strategy

**Decision**: Use HttpOnly cookies for JWT storage (Option A)

**Rationale**: 
- Most secure against XSS attacks compared to localStorage
- Better Auth (mentioned in constraints) typically uses cookie-based authentication
- Modern Next.js App Router supports server-side cookie handling
- Reduces frontend complexity for token management
- Aligns with security best practices for web applications

**Alternatives considered**:
- localStorage: Easier for SPA but vulnerable to XSS if CSP not properly configured
- Memory storage: Requires refresh token mechanism, more complex implementation
- Hybrid approach: Cookies for auth, localStorage for non-sensitive data - overcomplicates

## Clarification 2: Error Handling Granularity

**Decision**: Context-specific messages with error codes (Option B)

**Rationale**:
- Provides better debugging and user guidance than generic messages
- Backend already returns structured errors (from JWT auth implementation)
- Can map backend error codes to user-friendly frontend messages
- Maintains consistency with existing backend error patterns
- Allows for targeted recovery actions based on error type

**Alternatives considered**:
- Generic messages only: Simpler but less helpful for users and developers
- Technical details in dev mode: Good for development but requires environment detection
- Custom error mapping: More work but provides optimal UX

## Clarification 3: Mobile Navigation Pattern

**Decision**: Bottom navigation bar with 3 main sections (Option A)

**Rationale**:
- Standard mobile pattern that users are familiar with
- Optimized for thumb reach on mobile devices
- Supports the core todo functionality well (List, Add, Profile/Settings)
- Works well with Next.js App Router layout system
- Matches success criteria for mobile-first responsive design

**Alternatives considered**:
- Hamburger menu: Less discoverable, requires extra tap for common actions
- Tab-based with swipe: Modern but may confuse some users, especially for task management
- Floating action button: Good for add action but insufficient for full navigation

## Additional Research Notes

- Next.js 16+ App Router supports server components for authentication flows
- Better Auth integration should use middleware for route protection
- Responsive design should use CSS Grid/Flexbox with mobile-first breakpoints
- API client should use fetch with interceptors for JWT attachment
- Loading states should use skeleton screens for better perceived performance