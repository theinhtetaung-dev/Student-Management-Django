import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .services import StudentService



@ensure_csrf_cookie
def index_view(request):
    """Renders the main single-page application UI."""
    return render(request, 'students/index.html')


def api_students(request):
    """
    GET: Get paginated and filtered list of students and overall stats.
    POST: Create a new student.
    """
    service = StudentService()

    if request.method == 'GET':
        search_query = request.GET.get('q', '').strip()
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 5)

        data = service.get_students_list(search_query=search_query, page=page, limit=limit)
        stats = service.get_stats()
        return JsonResponse({
            'success': True,
            'data': data,
            'stats': stats
        })

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            roll_no = body.get('roll_no', '')
            name = body.get('name', '')
            major = body.get('major', '')

            student = service.create_student(roll_no, name, major)
            return JsonResponse({
                'success': True,
                'message': 'Student created successfully.',
                'student': {
                    'student_id': student.student_id,
                    'roll_no': student.roll_no,
                    'name': student.name,
                    'major': student.major
                }
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)

def api_student_detail(request, student_id):
    """
    GET: Retrieve details of a single student.
    PUT/POST: Update details of an existing student.
    DELETE: Delete an existing student.
    """
    service = StudentService()
    if request.method == 'GET':
        try:
            student = service.get_student(student_id)
            return JsonResponse({
                'success': True,
                'student': {
                    'student_id': student.student_id,
                    'roll_no': student.roll_no,
                    'name': student.name,
                    'major': student.major
                }
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=404)

    elif request.method in ['PUT', 'POST']:
        try:
            body = json.loads(request.body)
            roll_no = body.get('roll_no', '')
            name = body.get('name', '')
            major = body.get('major', '')

            student = service.update_student(student_id, roll_no, name, major)
            return JsonResponse({
                'success': True,
                'message': 'Student updated successfully.',
                'student': {
                    'student_id': student.student_id,
                    'roll_no': student.roll_no,
                    'name': student.name,
                    'major': student.major
                }
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    elif request.method == 'DELETE':
        try:
            service.delete_student(student_id)
            return JsonResponse({
                'success': True,
                'message': 'Student deleted successfully.'
            })
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)
