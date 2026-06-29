from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.core.data_manager import DataManager

students_bp = Blueprint(
    'students', 
    __name__, 
    template_folder='templates'
)

data_manager = DataManager('data/students.xlsx')

@students_bp.route('/')
def list_students():
    # Return all students to the template and let client-side JS handle search/pagination without refreshing
    all_students = data_manager.get_all_students()
    
    total_active_students = len(all_students)
    active_majors = len(set(s.get('major') for s in all_students if s.get('major')))
    
    return render_template('students/list.html', 
                           students=all_students,
                           total_active_students=total_active_students,
                           active_majors=active_majors)

@students_bp.route('/add', methods=['POST'])
def add_student():
    roll_no = request.form.get('roll_no')
    studentName = request.form.get('studentName')
    major = request.form.get('major')
    
    if roll_no and studentName and major:
        data_manager.add_student({
            'roll_no': roll_no,
            'studentName': studentName,
            'major': major
        })
        flash('Student added successfully!', 'success')
    else:
        flash('All fields are required.', 'danger')
        
    return redirect(url_for('students.list_students'))

@students_bp.route('/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    roll_no = request.form.get('roll_no')
    studentName = request.form.get('studentName')
    major = request.form.get('major')
    
    if roll_no and studentName and major:
        data_manager.update_student(student_id, {
            'roll_no': roll_no,
            'studentName': studentName,
            'major': major
        })
        flash('Student updated successfully!', 'success')
    else:
        flash('All fields are required.', 'danger')
        
    return redirect(url_for('students.list_students'))

@students_bp.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    success = data_manager.delete_student(student_id)
    if success:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Error deleting student.', 'danger')
    return redirect(url_for('students.list_students'))
