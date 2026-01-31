# Tasks: Todo Backend & Database

**Feature**: Todo Backend & Database | **Branch**: `2-todo-backend-db` | **Date**: 2026-01-20

**Input**: Feature specification, implementation plan, data model, API contracts, and research from `/specs/2-todo-backend-db/`

## Overview

This document contains actionable, dependency-ordered tasks for implementing the Todo Backend & Database feature. Tasks are organized by user story to enable independent implementation and testing.

## Dependencies

- User Story 1 (Task Creation) → User Story 2 (View Tasks) → User Story 3 (Update Task) → User Story 4 (Delete Task) → User Story 5 (Toggle Task Completion)
- Foundational components (models, auth) must be completed before user story implementations

## Parallel Execution Examples

- User Story 2 (View Tasks) can be developed in parallel with User Story 3 (Update Task) once foundational components are in place
- Unit tests can be developed in parallel with implementation tasks

## Implementation Strategy

- **MVP First**: Complete User Story 1 (Task Creation) with minimal authentication and basic models
- **Incremental Delivery**: Add features incrementally with each user story
- **Test-Driven Development**: Write tests alongside implementation

---

## Phase 1: Setup

### Goal
Initialize the project structure and configure dependencies as outlined in the implementation plan.

### Tasks

- [X] T001 Create project directory structure: `backend/src/models`, `backend/src/services`, `backend/src/api`, `backend/src/middleware`, `backend/src/config`, `backend/tests/unit`, `backend/tests/integration`
- [X] T002 Create requirements.txt with FastAPI, SQLModel, Pydantic, Uvicorn, PyJWT, python-multipart, pytest, httpx
- [X] T003 Create requirements-dev.txt with development dependencies
- [X] T004 Create Dockerfile for containerization
- [X] T005 Create docker-compose.yml for local development
- [X] T006 Create README.md with project overview and setup instructions
- [X] T007 Create alembic.ini for database migrations
- [X] T008 Create alembic/versions directory for migration files
- [X] T009 Create alembic/env.py for migration environment

---

## Phase 2: Foundational Components

### Goal
Implement core components that are prerequisites for all user stories: models, authentication, and database configuration.

### Tasks

- [X] T010 [P] Create backend/src/models/__init__.py
- [X] T011 [P] [US1] Create backend/src/models/user.py with User model as specified in data model
- [X] T012 [P] [US1] Create backend/src/models/task.py with Task model as specified in data model
- [X] T013 [P] Create backend/src/config/settings.py using Pydantic Settings with DATABASE_URL and BETTER_AUTH_SECRET
- [X] T014 [P] Create backend/src/database.py with database session setup and engine configuration
- [X] T015 [P] Create backend/src/main.py with FastAPI app initialization
- [X] T016 [P] Create backend/src/middleware/__init__.py
- [X] T017 [P] Create backend/src/middleware/auth_middleware.py with JWT token extraction and validation
- [X] T018 [P] Create backend/src/services/__init__.py
- [X] T019 [P] Create backend/src/services/auth_service.py with JWT utilities
- [X] T020 Create backend/src/database/engine.py to initialize database engine with settings

---

## Phase 3: User Story 1 - Task Creation (Priority: P1)

### Goal
As an authenticated user, I want to create new todo tasks via the API, ensuring they are associated with my user account.

### Independent Test
Can be fully tested by sending a POST request to the `/api/{user_id}/tasks` endpoint with valid task data and an authenticated JWT token, and then verifying the task's existence and ownership via a GET request.

### Tasks

- [X] T021 [P] Create backend/src/services/task_service.py with create_task function
- [X] T022 [P] Create backend/src/api/__init__.py
- [X] T023 [P] Create backend/src/api/task_router.py with POST /{user_id}/tasks endpoint
- [X] T024 [P] Create backend/src/api/auth_router.py with authentication endpoints if needed
- [X] T025 [US1] Integrate task creation endpoint with auth middleware to verify user identity
- [X] T026 [US1] Ensure task creation associates the task with the authenticated user ID
- [X] T027 [US1] Add validation to ensure title is present and doesn't exceed 255 characters
- [X] T028 [US1] Write unit tests for task creation service in backend/tests/unit/test_services/test_task_service.py
- [X] T029 [US1] Write integration tests for task creation endpoint in backend/tests/integration/test_api/test_task_creation.py
- [X] T030 [US1] Test that created tasks are associated with the correct user

---

## Phase 4: User Story 2 - View Tasks (Priority: P1)

### Goal
As an authenticated user, I want to view my list of todo tasks and individual task details via the API, ensuring I can only see my own tasks.

### Independent Test
Can be fully tested by sending GET requests to `/api/{user_id}/tasks` and `/api/{user_id}/tasks/{id}` with an authenticated JWT token and verifying that only tasks belonging to the authenticated user are returned.

### Tasks

- [X] T031 [P] [US2] Extend task_service.py with get_tasks and get_task_by_id functions
- [X] T032 [P] [US2] Add GET /{user_id}/tasks endpoint to task_router.py for listing tasks
- [X] T033 [P] [US2] Add GET /{user_id}/tasks/{id} endpoint to task_router.py for retrieving specific task
- [X] T034 [US2] Implement user filtering in get_tasks function to return only user's tasks
- [X] T035 [US2] Implement user filtering in get_task_by_id function to return only user's task
- [X] T036 [US2] Add proper error handling for unauthorized access to other users' tasks (return 403/404)
- [X] T037 [US2] Write unit tests for get_tasks and get_task_by_id functions
- [X] T038 [US2] Write integration tests for GET endpoints
- [X] T039 [US2] Test that users can only see their own tasks
- [X] T040 [US2] Test that users receive 403/404 when accessing others' tasks

---

## Phase 5: User Story 3 - Update Task (Priority: P1)

### Goal
As an authenticated user, I want to update an existing todo task via the API, ensuring I can only modify my own tasks.

### Independent Test
Can be fully tested by sending a PUT request to `/api/{user_id}/tasks/{id}` with valid updated task data and an authenticated JWT token, and then verifying the changes via a GET request.

### Tasks

- [X] T041 [P] [US3] Extend task_service.py with update_task function
- [X] T042 [P] [US3] Add PUT /{user_id}/tasks/{id} endpoint to task_router.py
- [X] T043 [US3] Implement user verification in update_task function to ensure user owns the task
- [X] T044 [US3] Add proper error handling for unauthorized updates (return 403/404)
- [X] T045 [US3] Implement validation for updated task data
- [X] T046 [US3] Write unit tests for update_task function
- [X] T047 [US3] Write integration tests for PUT endpoint
- [X] T048 [US3] Test that users can only update their own tasks
- [X] T049 [US3] Test that users receive 403/404 when trying to update others' tasks

---

## Phase 6: User Story 4 - Delete Task (Priority: P1)

### Goal
As an authenticated user, I want to delete an existing todo task via the API, ensuring I can only delete my own tasks.

### Independent Test
Can be fully tested by sending a DELETE request to `/api/{user_id}/tasks/{id}` with an authenticated JWT token, and then verifying the task's absence via a GET request.

### Tasks

- [X] T050 [P] [US4] Extend task_service.py with delete_task function
- [X] T051 [P] [US4] Add DELETE /{user_id}/tasks/{id} endpoint to task_router.py
- [X] T052 [US4] Implement user verification in delete_task function to ensure user owns the task
- [X] T053 [US4] Add proper error handling for unauthorized deletions (return 403/404)
- [X] T054 [US4] Return 204 No Content status after successful deletion
- [X] T055 [US4] Write unit tests for delete_task function
- [X] T056 [US4] Write integration tests for DELETE endpoint
- [X] T057 [US4] Test that users can only delete their own tasks
- [X] T058 [US4] Test that users receive 403/404 when trying to delete others' tasks

---

## Phase 7: User Story 5 - Toggle Task Completion (Priority: P1)

### Goal
As an authenticated user, I want to mark a todo task as complete or incomplete via the API, ensuring I can only modify my own tasks.

### Independent Test
Can be fully tested by sending a PATCH request to `/api/{user_id}/tasks/{id}/complete` with an authenticated JWT token, and then verifying the completion status via a GET request.

### Tasks

- [X] T059 [P] [US5] Extend task_service.py with toggle_task_completion function
- [X] T060 [P] [US5] Add PATCH /{user_id}/tasks/{id}/complete endpoint to task_router.py
- [X] T061 [US5] Implement user verification in toggle_task_completion function to ensure user owns the task
- [X] T062 [US5] Add proper error handling for unauthorized toggles (return 403/404)
- [X] T063 [US5] Write unit tests for toggle_task_completion function
- [X] T064 [US5] Write integration tests for PATCH endpoint
- [X] T065 [US5] Test that users can only toggle completion of their own tasks
- [X] T066 [US5] Test that users receive 403/404 when trying to toggle others' tasks
- [X] T067 [US5] Test that completion status is properly toggled

---

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper error handling, logging, documentation, and performance considerations.

### Tasks

- [X] T068 Add comprehensive error handling and custom exception classes
- [X] T069 Implement proper logging throughout the application
- [X] T070 Add request/response validation using Pydantic models
- [ ] T071 Add rate limiting to prevent abuse
- [ ] T072 Add database indexes as specified in data model (user_id, completed, composite)
- [ ] T073 Write comprehensive integration tests covering edge cases
- [X] T074 Add API documentation with Swagger/OpenAPI
- [ ] T075 Perform security audit of JWT implementation
- [X] T076 Add environment-specific configurations (dev, staging, prod)
- [ ] T077 Conduct performance testing to ensure 100+ concurrent requests capability
- [X] T078 Update README.md with complete API documentation and usage examples
- [ ] T079 Create deployment scripts or configurations
- [ ] T080 Perform final integration testing of all user stories together