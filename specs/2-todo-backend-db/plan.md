# Implementation Plan: Todo Backend & Database

**Branch**: `2-todo-backend-db` | **Date**: 2026-01-20 | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure, reliable backend API and database layer to support multi-user Todo operations using Python FastAPI, Neon Serverless PostgreSQL with SQLModel ORM, and JWT-based authentication. The backend will provide full CRUD functionality for todo tasks with proper user isolation and concurrent request handling capabilities.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, Uvicorn, PyJWT, python-multipart
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Backend API service
**Performance Goals**: Handle at least 100 concurrent requests per second for task listing without degradation in response time
**Constraints**: Must implement JWT authentication with shared secret (`BETTER_AUTH_SECRET`), follow REST conventions, complete implementation within 1 week
**Scale/Scope**: Multi-user support with proper user isolation for tasks

## Constitution Check

Based on the project constitution (which appears to be a template that needs to be filled in), I'll evaluate the planned implementation:

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

- **Test-First (NON-NEGOTIABLE)**: The plan includes writing tests for all API endpoints and authentication middleware before implementation. All CRUD operations will have corresponding test cases.
- **Integration Testing**: Since this feature involves database integration, authentication, and API contracts, comprehensive integration tests will be required between these components.
- **Observability**: The backend will include proper logging for debugging and monitoring purposes.
- **CLI Interface**: Though not directly applicable to a backend API, the service will follow a text I/O protocol with JSON responses.

Potential issues to address:
- The constitution file itself is a template that needs to be properly filled out for the project. This represents a gap in governance that should be addressed early in the project lifecycle.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   └── task_router.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── main.py
├── tests/
│   ├── unit/
│   │   ├── test_models/
│   │   └── test_services/
│   ├── integration/
│   │   ├── test_api/
│   │   └── test_auth/
│   └── conftest.py
├── requirements.txt
├── requirements-dev.txt
├── alembic/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── README.md
```

**Structure Decision**: Selected the backend structure with separate modules for models, services, API routes, middleware, and configuration. This provides clear separation of concerns and maintainability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Using multiple dependencies (FastAPI, SQLModel, PyJWT) | Required for robust API, ORM, and authentication | Would compromise functionality and security |
| Neon Serverless PostgreSQL | Provides scalability and managed infrastructure | Self-hosted solutions would increase operational complexity |

## Phase 0: Research & Resolution of Unknowns

### Research Tasks Completed

1. **Authentication Implementation Research**
   - Decision: Use PyJWT for handling JWT tokens with middleware approach
   - Rationale: Standard library for JWT in Python ecosystem with good FastAPI integration
   - Alternatives considered: Authlib, python-jose (selected PyJWT for simplicity and community support)

2. **Database Connection Pooling Research**
   - Decision: Use SQLModel's built-in connection handling with Neon Serverless PostgreSQL
   - Rationale: SQLModel is built on SQLAlchemy which provides excellent connection pooling
   - Alternatives considered: Manual connection management (rejected for complexity)

3. **Concurrent Request Handling Research**
   - Decision: Leverage FastAPI's async capabilities and Uvicorn ASGI server
   - Rationale: FastAPI is designed for high-performance concurrent requests
   - Alternatives considered: Sync frameworks like Flask (rejected for performance limitations)

4. **Environment Configuration Research**
   - Decision: Use Pydantic Settings for configuration management
   - Rationale: Integrates well with FastAPI and provides validation
   - Alternatives considered: Simple environment variable loading (rejected for lack of validation)

## Phase 1: Design & Contracts

### Data Model Design

**Task Entity:**
- `id` (UUID, primary key)
- `title` (string, mandatory, max length 255)
- `description` (string, optional, max length 1000)
- `completed` (boolean, default False)
- `user_id` (UUID, foreign key to User, mandatory)
- `created_at` (datetime, auto-generated)
- `updated_at` (datetime, auto-generated)

**User Entity:**
- `id` (UUID, primary key)
- `email` (string, unique, mandatory, max length 255)
- `created_at` (datetime, auto-generated)
- `updated_at` (datetime, auto-generated)

### API Contracts

**Base URL**: `/api/{user_id}`

**Endpoints:**
1. `GET /tasks` → List all tasks for a user
2. `POST /tasks` → Create a new task
3. `GET /tasks/{id}` → Get a specific task
4. `PUT /tasks/{id}` → Update a specific task
5. `DELETE /tasks/{id}` → Delete a specific task
6. `PATCH /tasks/{id}/complete` → Toggle task completion status