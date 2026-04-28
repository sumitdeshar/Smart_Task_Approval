# 🚀 Project TODO: Auth + Leave Management System

## ✅ Completed

- [x] Register API implemented
- [x] Basic login setup
- [x] OAuth login integrated (partial)

---

## 🔄 In Progress

- [ ] Add role field in User model
  - Roles: `employee`, `manager`, `admin`

---

## 🛠️ Authentication & Authorization

### OAuth + JWT Integration

- [x] Integrate OAuth flow with backend
- [x] Verify OAuth JWT token properly
- [x] Extract user info from OAuth provider

### Role-Based Access Control (RBAC)

- [x] Store user roles in database
- [x] Generate JWT with role payload
- [x] Middleware to:
  - [x] Decode JWT
  - [x] Validate token
  - [x] Check user role
- [ ] Restrict API access based on roles

---

## 📄 Leave Management System

### Employee Features

- [ ] Create Leave Application Form
  - Fields:
    - [ ] Employee ID
    - [ ] Leave Type
    - [ ] Start Date
    - [ ] End Date
    - [ ] Reason
- [ ] Submit leave request
- [ ] Store leave in database

### Manager Features

- [ ] View all leave requests
- [ ] Approve leave ✅
- [ ] Reject leave ❌
- [ ] Add optional comments

---

## 🗄️ Database Design

### User Table

- [ ] id
- [ ] name
- [ ] email
- [ ] role

### Leave Table

- [ ] id
- [ ] employee_id (FK)
- [ ] leave_type
- [ ] start_date
- [ ] end_date
- [ ] reason
- [ ] status (pending/approved/rejected)
- [ ] manager_comment

---

## 💰 Salary Integration

- [ ] Fetch approved leaves
- [ ] Calculate leave days
- [ ] Deduct from salary (if applicable)
- [ ] Generate salary report

---

## 🧪 Testing

- [ ] Test OAuth login flow
- [ ] Test JWT validation
- [ ] Test role-based access
- [ ] Test leave request lifecycle

---

## 🎯 Final Goals

- [ ] Secure authentication (OAuth + JWT)
- [ ] Fully working RBAC
- [ ] Functional leave system
- [ ] Salary impact calculation

---

## 🧠 Notes / Ideas

- Consider using:
  - Refresh tokens for better auth handling
  - Audit logs for leave approval/rejection
  - Notifications (email or in-app)

---

## 📊 Visual Progress Tracker

| Module             | Status         |
| ------------------ | -------------- |
| Auth (OAuth + JWT) | 🔄 In Progress |
| RBAC               | ⏳ Pending     |
| Leave System       | ⏳ Pending     |
| Salary Integration | ⏳ Pending     |
| Testing            | ⏳ Pending     |
