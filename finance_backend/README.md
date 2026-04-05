```markdown
# Finance Data Processing and Access Control Backend

A robust, role-based REST API for managing and analyzing financial records. Built with Django REST Framework, PostgreSQL, and Docker.

## 🚀 Features Achieved
1. **User & Role Management:** Custom User model with specific RBAC permissions (`Admin`, `Analyst`, `Editor`).
2. **JWT Authentication:** Secure login and token generation using `djangorestframework-simplejwt`.
3. **Financial Records Management:** Full CRUD capabilities with pagination, sorting, and filtering.
4. **Dashboard Analytics:** High-performance PostgreSQL aggregations for totals, categorized expenses, and monthly trends.
5. **Validation & Reliability:** Custom serializer validation to prevent negative amounts and future dates.
6. **Auto-Generated Documentation:** Interactive Swagger UI powered by `drf-spectacular`.

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

**3. Create a Superuser (Admin) to test the API:**
```bash
docker-compose exec web python manage.py createsuperuser
```
*(Or use the testing credentials provided below if the database volume is included).*

---

## 📖 API Documentation & Testing

**Interactive Swagger UI:**
Once the server is running, navigate to:
👉 **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**

From here, you can view all endpoints, required parameters, and test the API directly in your browser. 

**Test Credentials:**
* **Username:** `admin`
* **Password:** `admin`
*(Note: Use the `/api/auth/login/` endpoint to generate your Bearer token, then click the "Authorize" padlock in the Swagger UI to authenticate).*

## Architectural Decisions
* **Dashboard Logic:** Instead of creating a separate Django app for the dashboard, the analytics logic was integrated directly into the `finance` app views to prevent unnecessary cross-app dependencies and strictly adhere to the Single Responsibility Principle.
* **Filtering & Sorting:** Handled via query parameters on the list endpoint rather than separate URLs, ensuring a clean and RESTful design pattern.
```


