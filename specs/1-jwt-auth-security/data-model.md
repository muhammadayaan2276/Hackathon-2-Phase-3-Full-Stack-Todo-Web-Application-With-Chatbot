# Data Model: JWT Authentication & Security for Todo Application

## Entities

### User
Represents an authenticated user in the system.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | UUID | Unique identifier for the user | Required, immutable |
| email | string | User's email address | Required, unique, valid email format |
| created_at | timestamp | When the user account was created | Required, auto-generated |
| updated_at | timestamp | When the user account was last updated | Auto-generated |

**Relationships**:
- One-to-many with Task (user owns multiple tasks)
- No direct relationships with other entities

### JWT Token
Represents the authentication token used for API requests.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| payload.user_id | UUID | Reference to the user ID | Required, must exist in User table |
| payload.email | string | User's email from registration | Required, must match User.email |
| payload.exp | timestamp | Expiration time | Required, > current time |
| signature | string | HMAC-SHA256 signature | Required, verified against shared secret |

**Constraints**:
- Token must be signed with `BETTER_AUTH_SECRET`
- Payload must contain `user_id` and `email`
- Token expiration must be validated on every request
- Tokens are stateless (no server-side storage)

### Task
Represents a todo item owned by a user.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | UUID | Unique identifier for the task | Required, immutable |
| title | string | Task title | Required, 1-100 characters |
| description | string | Task description | Optional, max 1000 characters |
| completed | boolean | Whether the task is completed | Required, default false |
| owner_id | UUID | Reference to the user who owns this task | Required, must exist in User table |
| created_at | timestamp | When the task was created | Required, auto-generated |
| updated_at | timestamp | When the task was last updated | Auto-generated |

**Relationships**:
- Many-to-one with User (task belongs to one user)
- No other relationships

## Validation Rules

### User Validation
- Email must be unique across all users
- Password must meet minimum complexity requirements (8+ characters, mix of letters/numbers)
- User creation must be atomic (email uniqueness check + creation)

### Task Validation
- Title must not be empty
- Owner_id must reference an existing user
- Only the owner can modify or delete the task
- Completed status can only be toggled by the owner

## State Transitions

### User State
- **Created**: After successful signup
- **Active**: After successful signin (no explicit state, determined by valid JWT)
- **Disabled**: Not in scope (per constraints)

### Task State
- **Created**: After task creation
- **Completed**: After completion toggle by owner
- **Deleted**: After deletion by owner

## Security Considerations

- All user identifiers (UUIDs) should be opaque to prevent enumeration
- Task IDs should be UUIDs, not sequential integers
- JWT payload should not contain sensitive information beyond user_id and email
- Token signatures must be verified using HMAC-SHA256 with the shared secret
- Clock skew tolerance: ±5 minutes for token expiration validation