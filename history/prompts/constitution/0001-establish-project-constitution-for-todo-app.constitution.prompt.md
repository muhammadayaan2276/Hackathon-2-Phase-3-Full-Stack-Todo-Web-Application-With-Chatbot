---
id: 0001
title: Establish Project Constitution for Todo App
stage: constitution
date: 2026-01-20
surface: agent
model: gemini-pro
feature: none
branch: 1-console-todo-app
user: Ayaan Zeeshan
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution Project**Phase II – Todo Full-Stack Web Application**## Core Principles- **Accuracy:** All API endpoints and frontend features must work as specified.  - **Security:** User data must be fully protected, with proper JWT-based authentication.  - **Responsiveness:** UI must adapt to all device sizes.  - **Reliability:** Backend must handle concurrent users with correct task isolation.  - **Maintainability:** Codebase structured for easy future enhancements.  ## Key Standards- RESTful API conventions for all backend endpoints.  - JWT token usage for authentication and user verification.  - Database queries must only return data for authenticated users.  - Frontend must dynamically display data from backend using Next.js 16+ App Router.  - Frontend forms must validate input and handle errors gracefully.  - Code must follow clean code principles and be well-commented.  - Consistent naming conventions for files, functions, and variables.  ## Constraints- **Frontend:** Next.js 16+ with App Router  - **Backend:** Python FastAPI  - **Database:** Neon Serverless PostgreSQL using SQLModel ORM  - **Authentication:** Better Auth + JWT integration  - **API endpoints:** GET, POST, PUT, DELETE, PATCH as per task operations  - **JWT Secret Key:** Shared between frontend and backend via environment variable (`BETTER_AUTH_SECRET`)  - Must implement all 5 basic level Todo features  ## Success Criteria- All CRUD operations function correctly for authenticated users only.  - JWT authentication works end-to-end and tokens are verified on backend.  - Users can only view and modify their own tasks.  - Frontend is responsive and shows dynamic task updates.  - Proper error handling and user feedback implemented.  - Backend handles concurrent requests without data leaks.  - End-to-end integration passes all functional tests.

## Response snapshot

I have created the project constitution at .specify/memory/constitution.md based on the principles you provided. The version is 1.0.0. I have also verified that the existing templates are consistent with the new constitution.

## Outcome

- ✅ Impact: Established the foundational principles and standards for the project.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: The provided details were comprehensive, allowing for a detailed constitution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
