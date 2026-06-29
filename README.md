# Dajan Go Project

### 📁 Project Flow Explained

This is a "hybrid" project. One Django app serves both the user interface and the data.

| URL | Type | Serves |
| :--- | :--- | :--- |
| `/students/` | Web page | The HTML UI |
| `/students/api/students/` | REST API | Returns JSON data for all students |
| `/students/api/students/1/` | REST API | Returns JSON for a specific student |

The HTML page (`index.html`) acts as a client, calling these APIs using JavaScript `fetch` in the browser.

---

### 🔄 Full Request Flow
1. **Browser / Postman:** Sends an HTTP Request (GET, POST, PUT, DELETE).
2. **`urls.py`:** The "Traffic Director" that routes the request to the correct view.
3. **`views.py`:** The "Receptionist" that receives the request and coordinates the response.
4. **`services.py`:** The "Brain" that processes business logic, such as data validation and duplicate checks.
5. **`repositories.py`:** The "Database Helper" that interacts exclusively with the database.
6. **`models.py`:** The "Blueprint" that defines the structure of the `Tbl_Student` table.
7. **MySQL DB:** The "Storage" where the data resides.

---

### 📂 File Roles Explained
* **`urls.py` (Router):** Decides which function handles a specific URL.
* **`views.py` (Controller):** Reads the incoming request, triggers the service, and sends back JSON.
* **`services.py` (Business Logic):** Validates data and manages business rules.
* **`repositories.py` (DB Access):** The only layer authorized to interact with the database.
* **`models.py` (Table Schema):** Defines the columns and structure of the `Tbl_Student` table.
* **`apps.py` (App Config):** Boilerplate used by Django to register the app.
* **`tests.py` (Unit Tests):** Placeholders for future test code.
* **`admin.py` (Admin Panel):** Registers models for use in the Django admin UI.

---


### 🔁 "Create a Student"
When a **POST** request is sent to `/students/api/students/` with student data:
1.  **`urls.py`** routes the request to `views.api_students()`.
2.  **`views.py`** reads the JSON and calls the service layer.
3.  **`services.py`** validates the fields and performs duplicate checks.
4.  **`repositories.py`** uses the Django ORM to execute the save operation.
5.  **`MySQL`** performs the actual `INSERT` operation in the database.
6.  **Response:** The process reverses, and `views.py` returns a JSON confirmation to the client.

---

### 💡 Summary
The project follows a clean, modular architecture (View → Service → Repository → Model → DB). Keep `apps.py` to ensure the application functions correctly, and manage `tests.py` based on your project's testing requirements.
