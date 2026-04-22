# Finance Data Processing and Access Control Backend

A robust, role-based REST API for managing and analyzing financial records. Built with Django REST Framework, PostgreSQL, and Docker.

## 🚀 Features Achieved
1. **User & Role Management:** Custom User model with specific RBAC permissions (`Admin`, `Analyst`, `Editor`).
2. **JWT Authentication:** Secure login and token generation using `djangorestframework-simplejwt`.
3. **Financial Records Management:** Full CRUD capabilities with pagination, sorting, and filtering.
4. **Dashboard Analytics:** High-performance PostgreSQL aggregations for totals, categorized expenses, and monthly trends.
5. **Validation & Reliability:** Custom serializer validation to prevent negative amounts and future dates.
6. **Auto-Generated Documentation:** Interactive Swagger UI powered by `drf-spectacular`.

## 👥 Roles & Access Control
This API enforces strict Role-Based Access Control (RBAC) to ensure data integrity and security.

* **🛡️ Admin:** Full system access. Can create, read, update, and delete all financial records. Has full access to dashboard analytics and user management.
* **✍️ Editor:** Data entry focus. Can view all, create new, but only modify/delete their own records.
* **📊 Analyst:** Read-only oversight. Can view all financial records and access the dashboard analytics to generate reports, but *cannot* create, modify, or delete any data.

## 🛠️ Tech Stack
* **Framework:** Django 5.x / Django REST Framework
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose
* **Documentation:** Swagger / OpenAPI

---

## ⚙️ How to Run the Project Locally

This project is fully containerized. You do not need to install Python or PostgreSQL on your local machine.

**1. Build and start the containers:**
```bash
docker-compose up -d --build
```

**2. Apply database migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**3. Load dummy data:**
The repository includes a `live_data.json` file pre-populated with users and financial records. Load it to instantly populate your local database:
```bash
docker-compose exec web python manage.py loaddata live_data.json
```

*(Optional: If you prefer to start with an empty database instead of loading the dummy data, you can create a fresh admin account using `docker-compose exec web python manage.py createsuperuser`)*

---

## 📖 API Documentation & Testing

**Interactive Swagger UI:**
Once the server is running, navigate to:
👉 **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**

From here, you can view all endpoints, required parameters, and test the API directly in your browser. 

**Test Credentials:**
Use the `/api/auth/login/` endpoint to generate your Bearer token with the credentials below. Once generated, click the "Authorize" padlock in the Swagger UI and enter your token to authenticate as that specific role.

* **Admin User:**
  * **Username:** `admin`
  * **Password:** `admin`
* **Editor User:**
  * **Username:** `bob_editor`
  * **Password:** `testpassword123` 
* **Analyst User:**
  * **Username:** `alice_analyst`
  * **Password:** `testpassword123`

*(Note: These credentials will only work if you have run the `loaddata` command in Step 3).*

## 🏗️ Architectural Decisions
* **Dashboard Logic:** Instead of creating a separate Django app for the dashboard, the analytics logic was integrated directly into the `finance` app views to prevent unnecessary cross-app dependencies and strictly adhere to the Single Responsibility Principle.
* **Filtering & Sorting:** Handled via query parameters on the list endpoint rather than separate URLs, ensuring a clean and RESTful design pattern.
