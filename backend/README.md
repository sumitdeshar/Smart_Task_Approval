# 🧠 Smart Task Tracking & Discussion Management System

A backend REST API for collaborative task management, assignment tracking, problem discussions, and documented solution workflows — built with role-based access control (RBAC), JWT authentication, and multi-protocol API architecture.

---

# 📋 Table of Contents

- [Overview](#overview)
- [Core Idea](#core-idea)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Multi-Protocol API Design](#multi-protocol-api-design)
- [API Reference](#api-reference)
- [Authentication & Authorization](#authentication--authorization)
- [Roles & Permissions](#roles--permissions)
- [Database Schema](#database-schema)
- [Development Status](#development-status)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

---

# Overview

The Smart Task Tracking & Discussion Management System is designed to help teams collaboratively manage tasks, investigate problems, document discussions, assign responsibilities, and preserve final solutions for future reference.

Unlike traditional task managers that only track completion status, this platform focuses heavily on:

- Problem-solving workflows
- Task discussions
- Decision history
- Assignment tracking
- Solution documentation
- Team collaboration
- Activity auditing

The system supports multiple API paradigms including REST, GraphQL, WebSocket, gRPC, and SOAP simulation for learning distributed backend architecture.

---

# Core Idea

This project is centered around:

```text
Tasks → Discussions → Collaboration → Resolution → Documentation
```

Every task can contain:

- Multiple assigned users
- Real-time discussions
- Status updates
- Activity logs
- Final resolutions
- Root cause analysis
- Historical records

The platform acts as both:

- a task management system
- and a knowledge/documentation system

---

# Features

- ✅ User registration and JWT authentication
- 🔐 OAuth 2.0 + JWT authorization middleware
- 👥 Role-based access control (RBAC)
- 📝 Task creation and assignment
- 📌 Task status and priority management
- 💬 Task-specific discussions and comments
- 📚 Final solution and resolution documentation
- 📊 Activity tracking and audit logging
- ⚡ Real-time updates using WebSockets
- 🔍 Flexible GraphQL querying
- 🚀 Internal service communication with gRPC
- 🏛️ SOAP simulation for legacy integrations
- 🗄️ Persistent PostgreSQL storage

---

# Tech Stack

> _(Update according to your actual implementation)_

| Layer           | Technology            |
| --------------- | --------------------- |
| Runtime         | Python                |
| Framework       | FastAPI               |
| Authentication  | OAuth 2.0 + JWT       |
| Database        | PostgreSQL            |
| ORM             | SQLModel / SQLAlchemy |
| Validation      | Pydantic              |
| Realtime        | WebSocket             |
| API Query Layer | GraphQL               |
| Internal RPC    | gRPC                  |
| Legacy Protocol | SOAP Simulation       |
| Testing         | Pytest                |

---

# Architecture

```text
┌─────────────┐     OAuth / JWT      ┌──────────────────┐
│   Client    │ ──────────────────►  │   Auth Middleware │
└─────────────┘                      └────────┬─────────┘
                                              │ Role Check
                                     ┌────────▼─────────┐
                                     │   Route Handlers  │
                                     │ /auth /tasks      │
                                     │ /users /comments  │
                                     └────────┬─────────┘
                                              │
                                     ┌────────▼─────────┐
                                     │    Database       │
                                     │ Users | Tasks     │
                                     │ Comments          │
                                     └──────────────────┘
```

---

# Multi-Protocol API Design

# 🧩 API Paradigms Used

| Type      | Purpose                | Use Case                        |
| --------- | ---------------------- | ------------------------------- |
| REST      | CRUD operations        | Tasks, Users, Comments          |
| WebSocket | Real-time updates      | Notifications, live discussions |
| GraphQL   | Flexible querying      | Dashboards, analytics           |
| gRPC      | Internal communication | Auth & task services            |
| SOAP      | Legacy simulation      | Enterprise integrations         |

---

# ⚡ WebSocket (Real-Time)

Used for:

- Real-time task updates
- New discussion notifications
- Assignment alerts
- Status changes
- Live collaboration

Example:

```json
{
  "event": "TASK_UPDATED",
  "data": {
    "taskId": "123",
    "status": "IN_PROGRESS"
  }
}
```

---

# 🔍 GraphQL API

Endpoint:

```text
/api/graphql
```

Example:

```graphql
query {
  task(id: "123") {
    title
    status
    comments {
      message
      user {
        name
      }
    }
  }
}
```

---

# 🚀 gRPC (Internal Services)

Services:

- Auth Service
- Task Service
- Notification Service
- Activity Service

Flow:

```text
Task Service → Auth Service (verify permissions)
Task Service → Notification Service (broadcast update)
Task Service → Activity Service (store logs)
```

---

# 🏛️ SOAP (Legacy Simulation)

Example XML:

```xml
<TaskUpdate>
  <TaskId>123</TaskId>
  <Status>RESOLVED</Status>
  <ResolvedBy>User_001</ResolvedBy>
</TaskUpdate>
```

---

# 🏗️ Extended Architecture

```text
                ┌─────────────┐
                │   Client    │
                └──────┬──────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     REST API      GraphQL API   WebSocket Server
        │              │              │
        └──────┬───────┴───────┬──────┘
               │               │
        ┌──────▼──────┐  ┌─────▼──────┐
        │Task Service │  │Auth Service│
        └──────┬──────┘  └─────┬──────┘
               │               │
               └──────┬────────┘
                      │
                ┌─────▼──────┐
                │Activity Log│
                └─────┬──────┘
                      │
                ┌─────▼──────┐
                │ SOAP Client│
                └────────────┘
```

---

# API Reference

# SQLModel Tips

```python
# SQLModel internally automatically does scalars()

# exec() = execute() + scalars()

# Common Methods:

scalar()
scalar_one()
scalar_one_or_none()

first()
one()
one_or_none()

all()
```

---

# For RBAC

We use a concept where a async function is wrapped with another function(not necessarily async) to create a dependency injection to check roles of each user try to call APIs. This done so that it become callable function meaning the inner function is only executed only while called.

# This Pattern Is Called

# Higher-order function

# Dependency factory

# Closure

# The inner function "remembers" allowed_roles.

# That memory behavior is called a closure.

---

# Auth Routes — `/api/auth`

| Method | Endpoint          | Description            | Status         |
| ------ | ----------------- | ---------------------- | -------------- |
| POST   | `/register`       | Register new user      | ✅ Done        |
| POST   | `/login`          | Login and get JWT      | ✅ Done        |
| POST   | `/refresh-token`  | Refresh access token   | 📋 Todo        |
| GET    | `/oauth/callback` | OAuth callback handler | 🔄 In Progress |

---

# User Routes — `/api/users`

| Method | Endpoint | Description                 | Status  |
| ------ | -------- | --------------------------- | ------- |
| GET    | `/me`    | Get current user profile    | 📋 Todo |
| PATCH  | `/me`    | Update current user profile | 📋 Todo |
| GET    | `/`      | Get all users               | 📋 Todo |

---

# Task Routes — `/api/tasks`

| Method | Endpoint        | Description          | Status  |
| ------ | --------------- | -------------------- | ------- |
| POST   | `/`             | Create new task      | 📋 Todo |
| GET    | `/`             | Get tasks            | 📋 Todo |
| GET    | `/:id`          | Get specific task    | 📋 Todo |
| PATCH  | `/:id`          | Update task          | 📋 Todo |
| DELETE | `/:id`          | Delete task          | 📋 Todo |
| PATCH  | `/:id/status`   | Update task status   | 📋 Todo |
| PATCH  | `/:id/assign`   | Assign users to task | 📋 Todo |
| PATCH  | `/:id/unassign` | Remove assignment    | 📋 Todo |

---

# Discussion Routes — `/api/comments`

| Method | Endpoint        | Description                 | Status  |
| ------ | --------------- | --------------------------- | ------- |
| POST   | `/task/:taskId` | Add task discussion/comment | 📋 Todo |
| GET    | `/task/:taskId` | Get all discussions         | 📋 Todo |
| PATCH  | `/:commentId`   | Edit comment                | 📋 Todo |
| DELETE | `/:commentId`   | Delete comment              | 📋 Todo |

---

# Resolution Routes — `/api/resolutions`

| Method | Endpoint        | Description          | Status  |
| ------ | --------------- | -------------------- | ------- |
| POST   | `/task/:taskId` | Add final resolution | 📋 Todo |
| GET    | `/task/:taskId` | Get task resolutions | 📋 Todo |

---

# Activity Routes — `/api/activity`

| Method | Endpoint        | Description                | Status  |
| ------ | --------------- | -------------------------- | ------- |
| GET    | `/task/:taskId` | Get task activity timeline | 📋 Todo |

---

# Authentication & Authorization

This system uses:

- OAuth 2.0
- JWT Authentication
- Role-Based Access Control (RBAC)

---

# Login Flow

```text
1. User authenticates
2. Server validates credentials
3. JWT is generated
4. Client stores JWT
5. JWT sent in Authorization header
6. Middleware validates token
7. Request proceeds with attached user context
```

---

# Using the Token

```http
GET /api/tasks
Authorization: Bearer <your_jwt_token>
```

---

# Roles & Permissions

| Action              | User | Manager | Admin |
| ------------------- | ---- | ------- | ----- |
| Create tasks        | ✅   | ✅      | ✅    |
| Comment on tasks    | ✅   | ✅      | ✅    |
| View assigned tasks | ✅   | ✅      | ✅    |
| Assign users        | ❌   | ✅      | ✅    |
| Resolve tasks       | ✅   | ✅      | ✅    |
| View activity logs  | ❌   | ✅      | ✅    |
| Manage users        | ❌   | ❌      | ✅    |

Roles are embedded in JWT payloads and validated through middleware.

---

# Database Schema

# `users`

| Field     | Type      | Notes                  |
| --------- | --------- | ---------------------- |
| id        | UUID      | Primary key            |
| name      | String    |                        |
| email     | String    | Unique                 |
| password  | String    | Hashed password        |
| role      | Enum      | USER / MANAGER / ADMIN |
| createdAt | Timestamp |                        |

---

# `tasks`

| Field       | Type      | Notes                   |
| ----------- | --------- | ----------------------- |
| id          | UUID      | Primary key             |
| title       | String    |                         |
| description | Text      | Nullable                |
| status      | Enum      | OPEN / IN_PROGRESS etc. |
| priority    | Enum      | LOW / MEDIUM / HIGH     |
| createdBy   | UUID      | FK → users.id           |
| deadline    | Timestamp | Nullable                |
| createdAt   | Timestamp |                         |

---

# `task_assignments`

| Field      | Type      | Notes         |
| ---------- | --------- | ------------- |
| id         | UUID      | Primary key   |
| taskId     | UUID      | FK → tasks.id |
| userId     | UUID      | FK → users.id |
| assignedAt | Timestamp |               |

---

# `task_comments`

| Field     | Type      | Notes         |
| --------- | --------- | ------------- |
| id        | UUID      | Primary key   |
| taskId    | UUID      | FK → tasks.id |
| userId    | UUID      | FK → users.id |
| message   | Text      |               |
| createdAt | Timestamp |               |

---

# `task_resolutions`

| Field      | Type      | Notes         |
| ---------- | --------- | ------------- |
| id         | UUID      | Primary key   |
| taskId     | UUID      | FK → tasks.id |
| resolvedBy | UUID      | FK → users.id |
| rootCause  | Text      | Nullable      |
| solution   | Text      | Nullable      |
| createdAt  | Timestamp |               |

---

# `task_activity`

| Field     | Type      | Notes         |
| --------- | --------- | ------------- |
| id        | UUID      | Primary key   |
| taskId    | UUID      | FK → tasks.id |
| userId    | UUID      | FK → users.id |
| action    | String    |               |
| details   | Text      | Nullable      |
| createdAt | Timestamp |               |

---

# Development Status

| Module                      | Status      |
| --------------------------- | ----------- |
| User registration           | ✅ Complete |
| JWT authentication          | ✅ Complete |
| RBAC authorization          | ✅ Complete |
| Task CRUD APIs              | 📋 Todo     |
| Task assignment system      | 📋 Todo     |
| Discussion/comment system   | 📋 Todo     |
| Resolution tracking         | 📋 Todo     |
| WebSocket notifications     | 📋 Todo     |
| GraphQL integration         | 📋 Todo     |
| gRPC internal communication | 📋 Todo     |
| SOAP integration simulation | 📋 Todo     |

---

# Getting Started

```bash
# 1. Clone repository
git clone https://github.com/your-org/smart-task-system.git

# 2. Move into project
cd smart-task-system

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# Windows
venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Setup environment variables
cp .env.example .env

# 7. Run migrations
alembic upgrade head

# 8. Start development server
uvicorn main:app --reload
```

---

# Environment Variables

```env
# Server
PORT=8000
ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/task_db

# JWT
JWT_SECRET=your_secret_key
JWT_EXPIRE_MINUTES=30

# OAuth
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret
OAUTH_CALLBACK_URL=http://localhost:8000/api/auth/oauth/callback
```

---

# Future Improvements

- File uploads & attachments
- Mention/tag system
- Email notifications
- Search indexing
- Team/workspace support
- Kanban board UI
- AI-generated task summaries
- Automatic issue categorization
- Task dependency graph
- Full audit dashboard

---

# Contributing

1. Create feature branch

```bash
git checkout -b feature/your-feature
```

2. Commit changes

```bash
git commit -m "feat: add task assignment system"
```

3. Push branch

```bash
git push origin feature/your-feature
```

4. Open Pull Request

Follow Conventional Commits specification.

---

> Note:
> This project is under active development and architecture may evolve as additional collaboration and workflow features are implemented.
