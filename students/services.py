from .repositories import StudentRepository

class StudentService:
    def __init__(self):
        self.repository = StudentRepository()

    def _validate_student_data(self, roll_no, name, major):
        """Validate input fields."""
        if not roll_no or not str(roll_no).strip():
            raise ValueError("Roll Number is required.")
        if not name or not str(name).strip():
            raise ValueError("Student Name is required.")
        if not major or not str(major).strip():
            raise ValueError("Major is required.")

    def get_student(self, student_id):
        """Get student by ID. Raises ValueError if not found."""
        student = self.repository.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        return student

    def create_student(self, roll_no, name, major):
        """Validate and create a new student."""
        roll_no = str(roll_no).strip()
        name = str(name).strip()
        major = str(major).strip()

        self._validate_student_data(roll_no, name, major)

        # Check for duplicate RollNo
        existing = self.repository.get_by_roll_no(roll_no)
        if existing:
            raise ValueError(f"Roll Number '{roll_no}' is already registered.")

        return self.repository.create(roll_no, name, major)

    def update_student(self, student_id, roll_no, name, major):
        """Validate and update an existing student."""
        roll_no = str(roll_no).strip()
        name = str(name).strip()
        major = str(major).strip()

        self._validate_student_data(roll_no, name, major)

        student = self.repository.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")

        # Check if another student has the same RollNo
        existing = self.repository.get_by_roll_no(roll_no)
        if existing and existing.pk != student.pk:
            raise ValueError(f"Roll Number '{roll_no}' is already in use by another student.")

        return self.repository.update(student, roll_no, name, major)

    def delete_student(self, student_id):
        """Delete an existing student."""
        student = self.repository.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        self.repository.delete(student)

    def get_students_list(self, search_query=None, page=1, limit=5):
        """Get filtered and paginated list of students with page details."""
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1

        try:
            limit = int(limit)
            if limit < 1:
                limit = 5
        except (ValueError, TypeError):
            limit = 5

        total_count = self.repository.count(search_query)
        
        # Calculate pagination
        import math
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 1
        
        if page > total_pages:
            page = total_pages

        offset = (page - 1) * limit
        students_qs = self.repository.get_paginated(search_query, offset, limit)

        # Map to dict list
        items = []
        for s in students_qs:
            items.append({
                'student_id': s.student_id,
                'roll_no': s.roll_no,
                'name': s.name,
                'major': s.major
            })

        return {
            'items': items,
            'total_count': total_count,
            'page': page,
            'limit': limit,
            'total_pages': total_pages
        }

    def get_stats(self):
        """Retrieve high level statistics for dashboard."""
        total_students = self.repository.count()
        unique_majors = self.repository.get_unique_majors_count()
        return {
            'total_students': total_students,
            'unique_majors': unique_majors
        }
