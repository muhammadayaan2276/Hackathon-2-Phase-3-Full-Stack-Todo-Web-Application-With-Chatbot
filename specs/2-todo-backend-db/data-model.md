# Data Model: Todo Backend & Database

## Task Entity

Represents a single todo item.

### Attributes
- `id` (UUID, primary key)
- `title` (string, mandatory, max length 255)
- `description` (string, optional, max length 1000)
- `completed` (boolean, default False)
- `user_id` (UUID, foreign key to User, mandatory)
- `created_at` (datetime, auto-generated)
- `updated_at` (datetime, auto-generated)

### Relationships
- Belongs to one User (many-to-one relationship)

### Validation Rules
- Title must be present and not exceed 255 characters
- User ID must reference an existing user
- Completed status can be toggled via PATCH request

## User Entity

Represents a registered user in the system (managed by authentication system).

### Attributes
- `id` (UUID, primary key)
- `email` (string, unique, mandatory, max length 255)
- `created_at` (datetime, auto-generated)
- `updated_at` (datetime, auto-generated)

### Relationships
- Has many Tasks (one-to-many relationship)

### Validation Rules
- Email must be valid and unique
- User must exist before tasks can be associated with them

## State Transitions

### Task Completion
- `completed: false` → `completed: true` (via PATCH /api/{user_id}/tasks/{id}/complete)
- `completed: true` → `completed: false` (via PATCH /api/{user_id}/tasks/{id}/complete)

## Indexes
- Index on `user_id` for efficient querying of user-specific tasks
- Index on `completed` for efficient filtering of completed/incomplete tasks
- Composite index on `(user_id, completed)` for efficient user-specific filtering