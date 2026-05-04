# 🏢 Leave Management System

A backend REST API for managing employee leave requests, approvals, and payroll integration — built with role-based access control (RBAC) and JWT authentication.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Authentication & Authorization](#authentication--authorization)
- [Roles & Permissions](#roles--permissions)
- [Database Schema](#database-schema)
- [Development Status](#development-status)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)

---

## Overview

The Leave Management System allows employees to apply for leave through a structured workflow. Managers can approve or revoke those requests, and the leave records are factored into payroll calculations. The system uses OAuth 2.0 with JWT tokens and enforces role-based access at every API boundary.

---

## Features

- ✅ User registration and OAuth-based login
- 🔐 JWT verification and authorization middleware
- 👥 Role-based access control (Employee, Manager, Admin)
- 📝 Leave application submission by employees
- ✔️ Leave approval / revocation by managers
- 💰 Leave data integration with payroll processing
- 🗄️ Persistent storage of leave records with employee association

---

## Tech Stack

> _(Update this section to match your actual stack)_

| Layer     | Technology      |
| --------- | --------------- |
| Runtime   | Python          |
| Framework | FastAPI         |
| Auth      | OAuth 2.0 + JWT |
| Database  | PostgreSQL      |
| ORM       | SQLAlchemy      |
| Testing   | Pytest          |

---

## Architecture

```
┌─────────────┐     OAuth / JWT      ┌──────────────────┐
│   Client    │ ──────────────────►  │   Auth Middleware │
└─────────────┘                      └────────┬─────────┘
                                              │ Role Check
                                     ┌────────▼─────────┐
                                     │   Route Handlers  │
                                     │  /auth  /leaves   │
                                     │  /users /payroll  │
                                     └────────┬─────────┘
                                              │
                                     ┌────────▼─────────┐
                                     │    Database       │
                                     │  Users | Leaves   │
                                     └──────────────────┘
```

Multi-Protocol API Design (Learning Extension)
🧩 API Paradigms Used
Type Purpose Use Case
REST CRUD operations Users, Leaves, Payroll
WebSocket Real-time updates Notifications, status updates
GraphQL Flexible queries Dashboard, aggregated data
gRPC Internal communication Service-to-service calls
SOAP Legacy simulation External HR integration
⚡ WebSocket (Real-Time)
Notify employee when leave is approved/revoked
Notify manager of new leave request
Optional chat system

Example:

{
"event": "LEAVE_APPROVED",
"data": {
"leaveId": "123",
"status": "APPROVED"
}
}
🔍 GraphQL API

Endpoint:

/api/graphql

Example:

query {
user {
name
role
leaves {
status
startDate
endDate
}
}
}
🚀 gRPC (Internal Services)
Auth Service → JWT validation
Leave Service → business logic
Payroll Service → salary calculation

Flow:

Leave Service → Auth Service (verify role)
Leave Service → Payroll Service (update salary)
🏛️ SOAP (Legacy Simulation)

Example XML:

<LeaveRequest>
  <EmployeeId>123</EmployeeId>
  <StartDate>2026-05-01</StartDate>
  <EndDate>2026-05-05</EndDate>
  <Status>APPROVED</Status>
</LeaveRequest>
🏗️ Extended Architecture
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
        │Leave Service│  │Auth Service│
        └──────┬──────┘  └─────┬──────┘
               │               │
               └──────┬────────┘
                      │
                ┌─────▼──────┐
                │ Payroll    │
                └─────┬──────┘
                      │
                ┌─────▼──────┐
                │ SOAP Client│
                └────────────┘
---

## API Reference

### Auth Routes — `/api/auth`

| Method | Endpoint          | Description                     | Status         |
| ------ | ----------------- | ------------------------------- | -------------- |
| POST   | `/register`       | Register a new user             | ✅ Done        |
| POST   | `/login`          | OAuth login, returns JWT        | ✅ Done        |
| GET    | `/oauth/callback` | OAuth provider callback handler | 🔄 In Progress |

### User Routes — `/api/users`

| Method | Endpoint | Description                 | Status  |
| ------ | -------- | --------------------------- | ------- |
| GET    | `/me`    | Get current user profile    | 📋 Todo |
| PATCH  | `/me`    | Update current user profile | 📋 Todo |

### Leave Routes — `/api/leaves`

| Method | Endpoint       | Description                                | Status  |
| ------ | -------------- | ------------------------------------------ | ------- |
| POST   | `/`            | Employee submits a leave application       | 📋 Todo |
| GET    | `/`            | Get all leaves (manager) or own (employee) | 📋 Todo |
| GET    | `/:id`         | Get a specific leave by ID                 | 📋 Todo |
| PATCH  | `/:id/approve` | Manager approves a leave request           | 📋 Todo |
| PATCH  | `/:id/revoke`  | Manager revokes a leave request            | 📋 Todo |

### Payroll Routes — `/api/payroll`

| Method | Endpoint       | Description                             | Status  |
| ------ | -------------- | --------------------------------------- | ------- |
| GET    | `/:employeeId` | Get payroll summary factoring in leaves | 📋 Todo |

---

## Authentication & Authorization

This system uses **OAuth 2.0** for authentication and **JWT** for stateless session management.

**Login Flow:**

```
1. User initiates OAuth login
2. OAuth provider authenticates the user
3. Server verifies the OAuth token
4. Server issues a signed JWT containing { userId, role }
5. Client sends JWT in Authorization header on every subsequent request
6. Auth middleware validates JWT and attaches user context to the request
```

**Using the token:**

```http
GET /api/leaves
Authorization: Bearer <your_jwt_token>
```

---

## Roles & Permissions

| Action                  | Employee | Manager | Admin |
| ----------------------- | -------- | ------- | ----- |
| Apply for leave         | ✅       | ✅      | ✅    |
| View own leaves         | ✅       | ✅      | ✅    |
| View all leaves         | ❌       | ✅      | ✅    |
| Approve / revoke leaves | ❌       | ✅      | ✅    |
| View payroll data       | ❌       | ✅      | ✅    |
| Manage users            | ❌       | ❌      | ✅    |

Roles are embedded in the JWT payload at login and enforced by middleware on every protected route.

---

## Database Schema

### `users`

| Field     | Type      | Notes                          |
| --------- | --------- | ------------------------------ |
| id        | UUID      | Primary key                    |
| name      | String    |                                |
| email     | String    | Unique                         |
| role      | Enum      | `EMPLOYEE`, `MANAGER`, `ADMIN` |
| oauthId   | String    | From OAuth provider            |
| createdAt | Timestamp |                                |

### `leaves`

| Field      | Type      | Notes                                        |
| ---------- | --------- | -------------------------------------------- |
| id         | UUID      | Primary key                                  |
| employeeId | UUID      | Foreign key → `users.id`                     |
| startDate  | Date      |                                              |
| endDate    | Date      |                                              |
| reason     | String    |                                              |
| status     | Enum      | `PENDING`, `APPROVED`, `REVOKED`             |
| reviewedBy | UUID      | Foreign key → `users.id` (manager), nullable |
| createdAt  | Timestamp |                                              |

---

## Development Status

| Module                          | Status       |
| ------------------------------- | ------------ |
| User registration               | ✅ Complete  |
| OAuth login + JWT issuance      | ✅ Complete  |
| Add role field to user model    | ✅ Completed |
| Embed roles in JWT payload      | ✅ Completed |
| Role-based middleware / guards  | ✅ Completed |
| Leave application form + API    | 📋 Todo      |
| Manager approve / revoke leaves | 📋 Todo      |
| Payroll integration with leaves | 📋 Todo      |

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/your-org/leave-management-system.git
cd leave-management-system

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env

# 4. Run database migrations
npm run migrate

# 5. Start the development server
npm run dev
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
# Server
PORT=3000
NODE_ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/leave_db

# JWT
JWT_SECRET=your_super_secret_key
JWT_EXPIRES_IN=7d

# OAuth
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret
OAUTH_CALLBACK_URL=http://localhost:8000/api/auth/oauth/callback
```

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m "feat: add leave approval endpoint"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Open a Pull Request against `main`

Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

> **Note:** This project is under active development. APIs marked 📋 Todo are subject to change before release.
