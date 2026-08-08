# 🏥 Clinic Management System

A full-stack clinic management system built with Python, FastAPI, SQLModel, SQLite, and a simple HTML/CSS/JavaScript frontend.

## ✨ Features

- 🔐 User authentication
- 👥 Patient management
- 👨‍⚕️ Doctor management
- 📅 Appointment management
- ➕ Add patients and doctors
- 🗑️ Delete patients, doctors, and appointments
- 🔒 Protected API endpoints
- 🎟️ Token-based authentication
- 🗄️ SQLite database
- 🌐 Simple web dashboard

## 🛠️ Technologies

### Backend

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

## 📁 Project Structure

```text
clinic/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── patients.py
│   ├── doctors.py
│   └── appointments.py
│
└── clinic/
    └── frontend/
        ├── index.html
        ├── dashboard.html
        ├── patients.html
        ├── doctors.html
        └── appointments.html