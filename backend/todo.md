# 🚀 Project TODO: Auth + Leave Management System

## ✅ Completed

- [x] Register API implemented
- [x] Basic login setup
- [x] OAuth login integrated (partial)

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
- [x] Restrict API access based on roles

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

- [x] id
- [x] name
- [x] email
- [x] role

### Leave Table

- [x] id
- [x] employee_id (FK)
- [x] leave_type
- [x] start_date
- [x] end_date
- [x] reason
- [x] status (pending/approved/rejected)
- [x] manager_comment

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

- [x] Secure authentication (OAuth + JWT)
- [x] Fully working RBAC
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

| Module             | Status       |
| ------------------ | ------------ |
| Auth (OAuth + JWT) | ✅ Completed |
| RBAC               | ✅ Completed |
| Leave System       | ⏳ Pending   |
| Salary Integration | ⏳ Pending   |
| Testing            | ⏳ Pending   |
