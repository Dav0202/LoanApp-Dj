# 🏦 Django Loan Management System API

A Django REST Framework-based Loan Management API with built-in fraud detection and admin moderation.

---

## 🚀 Features

- ✅ User Registration and Token-based Login
- ✅ Submit, View, and Track Loan Applications
- ✅ Admin-only approval, rejection, and flagging of loans
- ✅ Basic Fraud Detection:
  - More than 3 loans submitted in the past 24 hours
  - Loan amount exceeds ₦5,000,000
  - More than 10 users using the same email domain
- ✅ Admin email alert on flagged loans (mocked to terminal)
- ✅ Role-based permissions (user vs admin)
- ✅ Paginated endpoints
- ✅ Swagger/OpenAPI documentation

---

## 🤔 Assumptions
Authentication uses DRF TokenAuth for simplicity.

Fraud checks are performed only at the time of loan submission.

"Flagged" loans must be manually reviewed by admins.

Admins are determined by Django’s is_staff flag.

Email backend is mocked to terminal.

---

## ⚙️ Setup & Installation

Follow the steps below to get started:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin user
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

# 7. Run the tests
python manage.py test

📘 API Documentation
Visit the Swagger UI after starting the server:
📎 http://127.0.0.1:8000/swagger/

Author
---
Dav0202
