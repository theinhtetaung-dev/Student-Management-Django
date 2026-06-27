from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True, db_column='Student_Id')
    roll_no = models.CharField(max_length=50, unique=True, db_column='RollNo')
    name = models.CharField(max_length=100, db_column='Name')
    major = models.CharField(max_length=100, db_column='Major')

    class Meta:
        db_table = 'Tbl_Student'

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
