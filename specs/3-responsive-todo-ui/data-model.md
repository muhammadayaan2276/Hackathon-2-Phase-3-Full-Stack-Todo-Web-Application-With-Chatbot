# Data Model: Responsive Todo UI

## Entities

### User
- **id**: string (UUID) - unique identifier
- **email**: string - user's email address (unique)
- **created_at**: datetime - when user was created
- **authentication_state**: enum (authenticated, unauthenticated) - current auth status
- **session_expiry**: datetime - when current session expires

### Todo
- **id**: string (UUID) - unique identifier
- **title**: string (required) - task title (max 255 chars)
- **description**: string (optional) - task description (max 1000 chars)
- **completed**: boolean - whether task is completed
- **created_at**: datetime - when task was created
- **updated_at**: datetime - when task was last updated
- **user_id**: string (UUID) - foreign key to User.id
- **priority**: enum (low, medium, high) - task priority level
- **due_date**: datetime (optional) - deadline for task

## Relationships
- One User → Many Todos (1:N relationship)
- Todo belongs to exactly one User

## Validation Rules
- Todo title must be non-empty (min 1 character)
- Todo title max length: 255 characters
- Todo description max length: 1000 characters
- User email must be valid email format
- User email must be unique
- Completed status defaults to false
- Priority defaults to "medium"

## State Transitions
- Todo: created → active → completed → archived
- User: unauthenticated → authenticated → logged_out

## Constraints
- Frontend must not store or transmit user_id from URL parameters (use JWT claims only)
- All todo operations must be scoped to current authenticated user
- Backend enforces user isolation; frontend should not trust client-provided user_id

## Assumptions
- Backend already implements user isolation at API level
- JWT tokens contain user_id and email claims
- Timestamps are in UTC format
- UUID format follows RFC 4122 standard