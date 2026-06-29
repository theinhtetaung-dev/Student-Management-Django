from django.db.models import Q
from .models import Student

class StudentRepository:
    def get_all(self):
        """Retrieve all students ordered by student_id descending."""
        return Student.objects.all().order_by('-student_id')

    def get_by_id(self, student_id):
        """Retrieve a single student by ID, return None if not found."""
        try:
            return Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return None

    def get_by_roll_no(self, roll_no):
        """Retrieve a single student by Roll Number, return None if not found."""
        try:
            return Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            return None

    def create(self, roll_no, name, major):
        """Create and save a new student."""
        student = Student(roll_no=roll_no, name=name, major=major)
        student.save()
        return student

    def update(self, student, roll_no, name, major):
        """Update and save an existing student."""
        student.roll_no = roll_no
        student.name = name
        student.major = major
        student.save()
        return student

    def delete(self, student):
        """Delete a student from the database."""
        student.delete()

    def get_paginated(self, search_query=None, offset=0, limit=10):
        """Get paginated and filtered students list."""
        queryset = Student.objects.all().order_by('-student_id')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(major__icontains=search_query) |
                Q(roll_no__icontains=search_query)
            )
        return queryset[offset:offset + limit]

    def count(self, search_query=None):
        """Get total count of students, optionally filtered by search query."""
        queryset = Student.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(major__icontains=search_query) |
                Q(roll_no__icontains=search_query)
            )
        return queryset.count()

    def get_unique_majors_count(self):
        """Get the count of unique majors in the system."""
        return Student.objects.values('major').distinct().count()
