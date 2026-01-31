# Feature Specification: Todo Backend & Database

**Feature Branch**: `2-todo-backend-db`  
**Created**: 2026-01-20  
**Status**: Draft  
**Input**: User description: "Backend & Database for Todo Full-Stack Web Application**Target audience:** Full-stack developers implementing backend and database layers for multi-user web apps **Focus:** Implementing secure, scalable, and reliable backend APIs with persistent data storage **Success criteria:**- RESTful API endpoints fully functional for CRUD operations: - `GET /api/{user_id}/tasks` → List tasks - `POST /api/{user_id}/tasks` → Create task - `GET /api/{user_id}/tasks/{id}` → Get task details - `PUT /api/{user_id}/tasks/{id}` → Update task - `DELETE /api/{user_id}/tasks/{id}` → Delete task - `PATCH /api/{user_id}/tasks/{id}/complete` → Toggle task completion - Backend correctly verifies JWT tokens and authenticates users - Queries only return tasks for the authenticated user - Database (Neon Serverless PostgreSQL) integration works via SQLModel ORM - Middleware filters and validates all requests by user ID - Backend can handle concurrent requests reliably **Constraints:**- Backend: Python FastAPI - Database: Neon Serverless PostgreSQL using SQLModel ORM - JWT authentication must use shared secret (`BETTER_AUTH_SECRET`) - Endpoints must follow REST conventions - Must implement all 5 basic-level Todo features - Complete implementation within 1 week **Not building:**- Frontend pages or UI elements - Authentication UI components (handled by frontend) - API documentation beyond basic route testing - Non-Todo related backend features"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Creation (Priority: P1)

As an authenticated user, I want to create new todo tasks via the API, ensuring they are associated with my user account.

**Why this priority**: This is a core feature enabling users to add content to their todo list.

**Independent Test**: Can be fully tested by sending a POST request to the `/api/{user_id}/tasks` endpoint with valid task data and an authenticated JWT token, and then verifying the task's existence and ownership via a GET request.

**Acceptance Scenarios**:

1.  **Given** an authenticated user and valid task data, **When** a POST request is sent to `/api/{user_id}/tasks`, **Then** a new task is created and returned with a 201 status code, and the task is associated with the authenticated user.

---

### User Story 2 - View Tasks (Priority: P1)

As an authenticated user, I want to view my list of todo tasks and individual task details via the API, ensuring I can only see my own tasks.

**Why this priority**: This is a core feature allowing users to retrieve and review their tasks.

**Independent Test**: Can be fully tested by sending GET requests to `/api/{user_id}/tasks` and `/api/{user_id}/tasks/{id}` with an authenticated JWT token and verifying that only tasks belonging to the authenticated user are returned.

**Acceptance Scenarios**:

1.  **Given** an authenticated user with existing tasks, **When** a GET request is sent to `/api/{user_id}/tasks`, **Then** a list of tasks belonging to that user is returned with a 200 status code.
2.  **Given** an authenticated user and a valid task ID belonging to that user, **When** a GET request is sent to `/api/{user_id}/tasks/{id}`, **Then** the details of that specific task are returned with a 200 status code.
3.  **Given** an authenticated user and a task ID belonging to *another* user, **When** a GET request is sent to `/api/{user_id}/tasks/{id}`, **Then** a 403 Forbidden or 404 Not Found status code is returned.

---

### User Story 3 - Update Task (Priority: P1)

As an authenticated user, I want to update an existing todo task via the API, ensuring I can only modify my own tasks.

**Why this priority**: This is a core feature enabling users to manage and modify their existing tasks.

**Independent Test**: Can be fully tested by sending a PUT request to `/api/{user_id}/tasks/{id}` with valid updated task data and an authenticated JWT token, and then verifying the changes via a GET request.

**Acceptance Scenarios**:

1.  **Given** an authenticated user and a valid task ID belonging to that user, **When** a PUT request is sent to `/api/{user_id}/tasks/{id}` with updated data, **Then** the task is updated and returned with a 200 status code.
2.  **Given** an authenticated user and a task ID belonging to *another* user, **When** a PUT request is sent to `/api/{user_id}/tasks/{id}`, **Then** a 403 Forbidden or 404 Not Found status code is returned.

---

### User Story 4 - Delete Task (Priority: P1)

As an authenticated user, I want to delete an existing todo task via the API, ensuring I can only delete my own tasks.

**Why this priority**: This is a core feature enabling users to remove unwanted tasks from their list.

**Independent Test**: Can be fully tested by sending a DELETE request to `/api/{user_id}/tasks/{id}` with an authenticated JWT token, and then verifying the task's absence via a GET request.

**Acceptance Scenarios**:

1.  **Given** an authenticated user and a valid task ID belonging to that user, **When** a DELETE request is sent to `/api/{user_id}/tasks/{id}`, **Then** the task is deleted and a 204 No Content status code is returned.
2.  **Given** an authenticated user and a task ID belonging to *another* user, **When** a DELETE request is sent to `/api/{user_id}/tasks/{id}`, **Then** a 403 Forbidden or 404 Not Found status code is returned.

---

### User Story 5 - Toggle Task Completion (Priority: P1)

As an authenticated user, I want to mark a todo task as complete or incomplete via the API, ensuring I can only modify my own tasks.

**Why this priority**: This is a core feature enabling users to track the status of their tasks.

**Independent Test**: Can be fully tested by sending a PATCH request to `/api/{user_id}/tasks/{id}/complete` with an authenticated JWT token, and then verifying the completion status via a GET request.

**Acceptance Scenarios**:

1.  **Given** an authenticated user and a valid task ID belonging to that user, **When** a PATCH request is sent to `/api/{user_id}/tasks/{id}/complete`, **Then** the completion status of the task is toggled and the updated task is returned with a 200 status code.
2.  **Given** an authenticated user and a task ID belonging to *another* user, **When** a PATCH request is sent to `/api/{user_id}/tasks/{id}/complete`, **Then** a 403 Forbidden or 404 Not Found status code is returned.

### Edge Cases

-   What happens when a user attempts to access or modify a task that does not belong to them? A 403 Forbidden or 404 Not Found response should be returned.
-   What happens if the provided JWT token is invalid, expired, or missing? A 401 Unauthorized response should be returned.
-   What happens if required fields are missing or invalid during task creation or update? A 422 Unprocessable Entity (or 400 Bad Request) response with details should be returned.
-   What happens when a request is made for a non-existent task ID? A 404 Not Found response should be returned.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The backend system MUST provide RESTful API endpoints for Create, Read (list and detail), Update, Delete, and Toggle Completion operations on todo tasks.
-   **FR-002**: The backend system MUST authenticate all API requests using JWT tokens, verifying their validity and expiry.
-   **FR-003**: The backend system MUST authorize users to access and modify only the todo tasks that belong to their authenticated user ID.
-   **FR-004**: The backend system MUST store todo tasks persistently in a Neon Serverless PostgreSQL database.
-   **FR-005**: The backend system MUST utilize SQLModel ORM for all database interactions.
-   **FR-006**: The backend system MUST implement middleware to extract and validate the `user_id` from the JWT token and use it to filter and scope all task-related operations.
-   **FR-007**: The backend system MUST be capable of handling concurrent requests reliably without data corruption or deadlocks.
-   **FR-008**: The backend system MUST be implemented using Python FastAPI.

### Key Entities *(include if feature involves data)*

-   **Task**: Represents a single todo item.
    *   **Attributes**: `id` (UUID, primary key), `title` (string, mandatory), `description` (string, optional), `completed` (boolean, default False), `user_id` (UUID, foreign key to User), `created_at` (datetime), `updated_at` (datetime).
-   **User**: (Implicitly managed by the authentication system, but needed for task ownership).
    *   **Attributes**: `id` (UUID, primary key).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: All RESTful API endpoints for CRUD operations on tasks function correctly (verified by automated tests).
-   **SC-002**: Backend correctly verifies JWT tokens for every authenticated request (verified by authentication integration tests).
-   **SC-003**: Queries for tasks return only tasks associated with the authenticated user ID (verified by authorization integration tests).
-   **SC-004**: Database (Neon Serverless PostgreSQL) integration via SQLModel ORM works seamlessly for all task operations.
-   **SC-005**: Custom middleware successfully filters and validates requests based on authenticated `user_id`.
-   **SC-006**: The backend handles at least 100 concurrent requests per second for task listing without degradation in response time (verified by load tests).
-   **SC-007**: The backend implementation is completed within 1 week.
