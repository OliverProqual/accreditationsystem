# Accreditation System

A **full-stack web application** for managing accreditation workflows.  

- **Backend**: FastAPI  
- **Frontend**: React  
- **Database**: MySQL  

The system manages centres, courses, candidates, users, cohorts, registrations, and issued certificates, with authentication and role-based access.  

---

## 📂 Project Structure

```

.
├── backend/               # FastAPI backend
│   ├── routers/           # API route handlers
│   ├── cruds/             # Database operations
│   ├── models/            # SQLAlchemy models
│   └── main.py            # FastAPI entrypoint
│
├── frontend/              # React frontend
│   ├── src/               # React components, pages, services
│   └── package.json
│
├── database/
│   └── schema.sql         # MySQL schema creation script
│
└── README.md

````

---

## 🗄 Database Schema

The schema is defined in [`database/schema.sql`](database/schema.sql).  
It includes tables for:

- Centres  
- Candidates  
- Certificates  
- Courses  
- Users  
- Cohorts  
- Course Registrations  
- Issued Certificates  

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+  
- Node.js 18+  
- MySQL 8+  

### 2. Setup Database
```bash
mysql -u root -p < database/schema.sql
````

Update the backend database connection settings (DSN example):

```
mysql+pymysql://username:password@localhost:3306/accreditationsystem
```

### 3. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

API Docs:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Frontend (React)

```bash
cd frontend
npm install
npm start
```

Frontend → [http://localhost:3000](http://localhost:3000)

---

## 🔐 Authentication & Roles

* **JWT-based authentication**
* Roles: `AccreditationStaff`, `CentreStaff`, `Instructor`
* Currently supports login and read-only access

---

## 📌 Roadmap

* [ ] CRUD operations for all entities
* [ ] Role-based frontend authorization
* [ ] Candidate registration workflows
* [ ] Course enrolments and payments
* [ ] Certificate issuance UI
* [ ] Reporting & analytics

---

## 🛠 Tech Stack

* **Backend**: FastAPI, SQLAlchemy, PyMySQL
* **Frontend**: React, Axios
* **Database**: MySQL

---

## 📜 License

Licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

```

Do you want me to also add a **quick start with Docker Compose** section, in case you or others want one-command setup later?
```
