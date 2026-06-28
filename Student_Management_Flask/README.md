# Student Management System

A Flask application demonstrating a feature-based (Vertical Slicing) project structure, using Pandas and Excel for data storage.

## Why Feature-Based Structure (Modular / Vertical Slicing)?

Traditional web apps group files by technical type (e.g., all controllers in one folder, all models in another). As a project scales, navigating between a feature's model, route, and template becomes cumbersome. 

**Feature-based architecture** organizes code by business domain (e.g., all `students` related files together).

### Key Benefits of this Structure:

1. **Scalability:** When adding a new feature (e.g., `teachers` or `courses`), you simply create a new folder under `app/features/`. The core application remains untouched.
2. **Discoverability:** Everything related to a student (routes, services, templates) is inside `app/features/students/`. You don't have to jump across the entire project tree.
3. **Decoupling:** Each feature acts as a mini-application (Flask Blueprint). This makes it easier to extract features into microservices later if necessary.
4. **Team Workflow:** Different developers or teams can work on separate feature folders simultaneously with minimal merge conflicts.

## Directory Tree

```text
.
├── app/
│   ├── __init__.py                # Application Factory (Registers blueprints)
│   ├── core/                      # Global utilities, configs, and shared services
│   │   ├── __init__.py
│   │   └── data_manager.py        # Pandas Excel Data Layer with file locking
│   └── features/                  # Feature modules
│       ├── __init__.py
│       └── students/              # 'Students' Vertical Slice
│           ├── __init__.py
│           ├── routes.py          # Students Blueprint & HTTP endpoints
│           ├── services.py        # (Optional) Business logic separate from routes
│           └── templates/
│               └── students/
│                   └── list.html  # Responsive Bootstrap 5 UI
├── data/
│   └── students.xlsx              # Excel database file (auto-generated on run)
├── requirements.txt               # Dependencies
├── run.py                         # Application entry point
└── README.md                      # Project documentation
```

## Data Layer Architecture

The data layer uses `pandas` to read and write an Excel file. To avoid file locking and corruption issues when multiple requests hit the server simultaneously:
- A `DataManager` class encapsulates all pandas operations.
- `filelock` is used around read/write operations to ensure safe concurrent access across threads and processes.
- The system automatically provisions the `.xlsx` file and its columns on first run if it does not exist.

## Setup and Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python run.py
   ```
3. Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)
