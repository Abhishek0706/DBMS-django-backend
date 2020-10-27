from django.http import HttpResponse
from django.db import connection
import json

# Create your views here.
from rest_framework import status
from rest_framework.parsers import JSONParser


def get_student(request):
    if request.method != 'GET':
        return HttpResponse(content='only get request allowed', status=status.HTTP_400_BAD_REQUEST)

    hostel = request.GET.get('hostel', None)
    enrollment_no = request.GET.get('enrollment_no', None)

    if hostel is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.student.enrollment_no , year_no, branch, email, full_name, phone_no, date_of_birth, bhawan
            FROM public.student INNER JOIN public.userdata
            ON public.student.enrollment_no = public.userdata.enrollment_no 
            WHERE LOWER(bhawan) LIKE LOWER(%s) ;
            """, (hostel,))

            rows = cursor.fetchall()

    elif enrollment_no is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.student.enrollment_no , year_no, branch, email, full_name, phone_no, date_of_birth, bhawan
            FROM public.student INNER JOIN public.userdata
            ON public.student.enrollment_no = public.userdata.enrollment_no
            WHERE public.student.enrollment_no = %s ;
            """, (enrollment_no,))

            rows = cursor.fetchall()

    else:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.student.enrollment_no , year_no, branch, email, full_name, phone_no, date_of_birth, bhawan
            FROM public.student INNER JOIN public.userdata
            ON public.student.enrollment_no = public.userdata.enrollment_no
            """)

            rows = cursor.fetchall()

    result = []
    for row in rows:
        # temp = {'enrollment_no': row[0], 'year_no': row[1], 'branch': row[2], 'email': row[3], 'full_name': row[4],
        #         'phone_no': row[5], 'date_of_birth': str(row[6]), 'bhawan': row[7]}
        temp = {'user': {'enrollment_no': row[0], 'full_name': row[4],
                         'phone_no': row[5], 'date_of_birth': str(row[6]), 'bhawan': row[7]}, 'year_no': row[1],
                'branch': row[2], 'email': row[3]}
        result.append(temp)

    json_data = json.dumps(result)
    return HttpResponse(json_data, content_type="application/json", status=status.HTTP_200_OK)


def add_student(request):
    if request.method != 'POST':
        return HttpResponse(content='only post request allowed', status=status.HTTP_400_BAD_REQUEST)
    _data = JSONParser().parse(request)
    enrollment_no = _data.get('enrollment_no', None)
    full_name = _data.get('full_name', None)
    phone_no = _data.get('phone_no', None)
    date_of_birth = _data.get('date_of_birth', None)
    bhawan = _data.get('hostel', None)
    year_no = _data.get('year_no', None)
    branch = _data.get('branch', None)
    email = _data.get('email', None)

    if (enrollment_no is None) or (full_name is None) or (phone_no is None) or (date_of_birth is None) or (
            bhawan is None) or (year_no is None) or (branch is None) or (email is None):
        return HttpResponse(content="all data not provided : enrollment_no, full_name, phone_no, data_of_birth, "
                                    "hostel, year_no, branch, email", status=status.HTTP_400_BAD_REQUEST)
    try:
        year_no = int(year_no)
    except ValueError:
        return HttpResponse(content='year can not convert into int', status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS( SELECT * FROM public.userdata WHERE enrollment_no = %s);
        """, (enrollment_no,))
        row = cursor.fetchone()
    if row[0]:
        return HttpResponse(content="user with this enrollment_no already exists", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO public.userdata (enrollment_no, full_name, phone_no, date_of_birth, bhawan) 
        VALUES (%s ,LOWER(%s), %s, TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI:SS'), LOWER(%s)) ;
        """, (enrollment_no, full_name, phone_no, date_of_birth, bhawan))
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO public.student (enrollment_no, year_no, branch, email) 
        VALUES (%s, %s, LOWER(%s), %s) ;
        """, (enrollment_no, year_no, branch, email))

    connection.commit()

    return HttpResponse(content="student added",status=status.HTTP_200_OK)


def get_worker(request):
    if request.method != 'GET':
        return HttpResponse(content='only get request allowed', status=status.HTTP_400_BAD_REQUEST)

    hostel = request.GET.get('hostel', None)
    enrollment_no = request.GET.get('enrollment_no', None)

    if hostel is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.worker.enrollment_no , public.worker.worker_role, full_name, phone_no, date_of_birth, 
            bhawan,salary, shift_start, shift_end 
            FROM (public.worker INNER JOIN public.userdata 
            ON public.worker.enrollment_no = public.userdata.enrollment_no) 
            INNER JOIN public.workerrole 
            ON LOWER(public.worker.worker_role) LIKE LOWER(public.workerrole.worker_role) 
            WHERE LOWER(bhawan) LIKE LOWER(%s) ;
            """, (hostel,))

            rows = cursor.fetchall()

    elif enrollment_no is not None:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.worker.enrollment_no , public.worker.worker_role, full_name, phone_no, date_of_birth, 
            bhawan,salary, shift_start, shift_end 
            FROM (public.worker INNER JOIN public.userdata
            ON public.worker.enrollment_no = public.userdata.enrollment_no)
            INNER JOIN public.workerrole
            ON LOWER(public.worker.worker_role) LIKE LOWER(public.workerrole.worker_role) 
            WHERE public.worker.enrollment_no = %s ;
            """, (enrollment_no,))

            rows = cursor.fetchall()

    else:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.worker.enrollment_no , public.worker.worker_role, full_name, phone_no, date_of_birth, 
            bhawan,salary, shift_start, shift_end 
            FROM (public.worker INNER JOIN public.userdata
            ON public.worker.enrollment_no = public.userdata.enrollment_no)
            INNER JOIN public.workerrole
            ON LOWER(public.worker.worker_role) LIKE LOWER(public.workerrole.worker_role) 
            """)

            rows = cursor.fetchall()

    result = []
    for row in rows:
        # temp = {'enrollment_no': row[0], 'worker_role': row[1], 'full_name': row[2],
        #         'phone_no': row[3], 'date_of_birth': str(row[4]), 'bhawan': row[5],
        #         'salary': row[6], 'shift_start': str(row[7]), 'shift_end': str(row[8])}

        temp = {
            'user': {'enrollment_no': row[0], 'full_name': row[2], 'phone_no': row[3], 'date_of_birth': str(row[4]),
                     'bhawan': row[5], }, 'worker_role': row[1], 'salary': row[6], 'shift_start': str(row[7]),
            'shift_end': str(row[8])}

        result.append(temp)

    json_data = json.dumps(result)
    return HttpResponse(json_data, content_type="application/json", status=status.HTTP_200_OK)


def add_worker(request):
    if request.method != 'POST':
        return HttpResponse(content='only post request allowed', status=status.HTTP_400_BAD_REQUEST)
    _data = JSONParser().parse(request)
    enrollment_no = _data.get('enrollment_no', None)
    full_name = _data.get('full_name', None)
    phone_no = _data.get('phone_no', None)
    date_of_birth = _data.get('date_of_birth', None)
    bhawan = _data.get('hostel', None)
    worker_role = _data.get('worker_role', None)

    if (enrollment_no is None) or (full_name is None) or (phone_no is None) or (date_of_birth is None) or (
            bhawan is None) or (worker_role is None):
        return HttpResponse(content="all data not provided : enrollment_no, full_name, phone_no, data_of_birth, "
                                    "hostel, worker_role", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS( SELECT * FROM public.userdata WHERE enrollment_no = %s);
        """, (enrollment_no,))
        row = cursor.fetchone()
    if row[0]:
        return HttpResponse(content="user with this enrollment_no already exists", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS( SELECT * FROM public.workerrole WHERE LOWER(worker_role) LIKE LOWER(%s));
        """, (worker_role,))
        row = cursor.fetchone()
    if not row[0]:
        return HttpResponse(content="worker role does not exists", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO public.userdata (enrollment_no, full_name, phone_no, date_of_birth, bhawan) 
        VALUES (%s ,LOWER(%s), %s, TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI:SS'), LOWER(%s)) ;
        """, (enrollment_no, full_name, phone_no, date_of_birth, bhawan))
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO public.worker (enrollment_no, worker_role) 
        VALUES (%s, LOWER(%s)) ;
        """, (enrollment_no, worker_role))

    connection.commit()

    return HttpResponse(content="worker added",status=status.HTTP_200_OK)


def get_workerrole(request):
    if request.method != 'GET':
        return HttpResponse(content='only get request allowed', status=status.HTTP_400_BAD_REQUEST)

    worker_role = request.GET.get('worker_role', None)
    if worker_role is None:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM public.workerrole ;
            """)
            rows = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT EXISTS (SELECT * FROM public.workerrole WHERE LOWER(worker_role) LIKE LOWER(%s));
            """, (worker_role,))
            row = cursor.fetchone()

        if not row[0]:
            return HttpResponse(content='this workerrole does not exists', status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT * FROM public.workerrole 
            WHERE LOWER(worker_role) LIKE LOWER (%s);
            """, (worker_role,))
            rows = cursor.fetchall()

    result = []
    for row in rows:
        temp = {'worker_role': row[0], 'salary': row[1],
                'shift_start': str(row[2]), 'shift_end': str(row[3])}
        result.append(temp)

    json_data = json.dumps(result)
    return HttpResponse(json_data, content_type="application/json", status=status.HTTP_200_OK)


def add_workerrole(request):
    if request.method != 'POST':
        return HttpResponse(content='only post request allowed', status=status.HTTP_400_BAD_REQUEST)

    _data = JSONParser().parse(request)

    worker_role = _data.get('worker_role', None)
    salary = _data.get('salary', None)
    shift_start = _data.get('shift_start', None)
    shift_end = _data.get('shift_end', None)

    if (worker_role is None) or (salary is None) or (shift_start is None) or (shift_end is None):
        return HttpResponse(content="all data not provided : worker_role, salary, shift_start, shift_end",
                            status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS (SELECT * FROM public.workerrole WHERE LOWER(worker_role) LIKE LOWER(%s));
        """, (worker_role,))
        row = cursor.fetchone()

    if row[0]:
        return HttpResponse(content='this workerrole already exists', status=status.HTTP_400_BAD_REQUEST)

    try:
        salary = float(salary)
    except ValueError:
        return HttpResponse(content='salary can not convert into float', status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        INSERT INTO public.workerrole (worker_role, salary, shift_start, shift_end) 
        VALUES (LOWER(%s), %s, TO_TIMESTAMP(%s, 'HH24:MI:SS'), TO_TIMESTAMP(%s, 'HH24:MI:SS')) ;
        """, (worker_role, salary, shift_start, shift_end))

    connection.commit()

    return HttpResponse(content="workerrole added", status=status.HTTP_200_OK)


def del_workerrole(request):
    if request.method != 'POST':
        return HttpResponse(content='only post request allowed', status=status.HTTP_400_BAD_REQUEST)

    _data = JSONParser().parse(request)

    worker_role = _data.get('worker_role', None)

    if worker_role is None:
        return HttpResponse(content="worker_role is required", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS (SELECT * FROM public.workerrole WHERE LOWER(worker_role) LIKE LOWER(%s));
        """, (worker_role,))
        row = cursor.fetchone()

    if not row[0]:
        return HttpResponse(content='this workerrole does not exists', status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        DELETE FROM public.workerrole 
        WHERE LOWER(public.workerrole.worker_role) LIKE LOWER(%s) ;
        """, (worker_role,))

    connection.commit()

    return HttpResponse(content="workerrole deleted", status=status.HTTP_200_OK)


def update_workerrole(request):
    if request.method != 'POST':
        return HttpResponse(content='only post request allowed', status=status.HTTP_400_BAD_REQUEST)

    _data = JSONParser().parse(request)

    worker_role = _data.get('worker_role', None)
    salary = _data.get('salary', None)
    shift_start = _data.get('shift_start', None)
    shift_end = _data.get('shift_end', None)

    if worker_role is None:
        return HttpResponse(content="worker_role is required", status=status.HTTP_400_BAD_REQUEST)

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS (SELECT * FROM public.workerrole WHERE LOWER(worker_role) LIKE LOWER(%s));
        """, (worker_role,))
        row = cursor.fetchone()

    if not row[0]:
        return HttpResponse(content='this workerrole does not exists', status=status.HTTP_400_BAD_REQUEST)

    if (salary is None) and (shift_start is None) and (shift_end is None):
        return HttpResponse(content="atleast one field is required : salary, shift_start, shift_end",
                            status=status.HTTP_400_BAD_REQUEST)
    if salary is not None:
        try:
            salary = float(salary)
        except ValueError:
            return HttpResponse(content='salary can not convert into float', status=status.HTTP_400_BAD_REQUEST)

    raw_query = "UPDATE public.workerrole SET "
    tuple = ()
    if salary is not None:
        raw_query += "salary = %s,"
        tuple += (salary,)
    if shift_start is not None:
        raw_query += "shift_start = %s,"
        tuple += (shift_start,)
    if shift_end is not None:
        raw_query += "shift_end = %s,"
        tuple += (shift_end,)

    raw_query = raw_query[:-1]

    raw_query += "WHERE LOWER(worker_role) LIKE LOWER(%s)"
    tuple += (worker_role,)

    with connection.cursor() as cursor:
        cursor.execute(raw_query, tuple)

    connection.commit()

    return HttpResponse(content="workerrole updated", status=status.HTTP_200_OK)


def get_login_info(request):
    if request.method != 'GET':
        return HttpResponse(content='only get request allowed', status=status.HTTP_400_BAD_REQUEST)

    enrollment_no = request.GET.get('enrollment_no', None)
    if enrollment_no is None:
        return HttpResponse(content="all data not provided : enrollment_no", status=status.HTTP_400_BAD_REQUEST)

    exists = False
    _type = None
    worker = None
    student = None

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS( SELECT * FROM public.student WHERE enrollment_no = %s);
        """, (enrollment_no,))
        row = cursor.fetchone()

    if row[0]:
        exists = True
        _type = 'student'
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.student.enrollment_no , year_no, branch, email, full_name, phone_no, date_of_birth, bhawan
            FROM public.student INNER JOIN public.userdata
            ON public.student.enrollment_no = public.userdata.enrollment_no
            WHERE public.student.enrollment_no = %s ;
            """, (enrollment_no,))

            data = cursor.fetchone()
        student = {
            'user': {'enrollment_no': data[0], 'full_name': data[4], 'phone_no': data[5], 'date_of_birth': str(data[6]),
                     'bhawan': data[7]}, 'year_no': data[1], 'branch': data[2], 'email': data[3],
        }

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT EXISTS( SELECT * FROM public.worker WHERE enrollment_no = %s);
        """, (enrollment_no,))
        row = cursor.fetchone()

    if row[0]:
        exists = True
        _type = 'worker'
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT public.worker.enrollment_no , public.worker.worker_role, full_name, phone_no, date_of_birth, 
            bhawan,salary, shift_start, shift_end 
            FROM (public.worker INNER JOIN public.userdata
            ON public.worker.enrollment_no = public.userdata.enrollment_no)
            INNER JOIN public.workerrole
            ON LOWER(public.worker.worker_role) LIKE LOWER(public.workerrole.worker_role) 
            WHERE public.worker.enrollment_no = %s ;
            """, (enrollment_no,))

            data = cursor.fetchone()

        worker = {'user': {'enrollment_no': data[0], 'full_name': data[2],
                           'phone_no': data[3], 'date_of_birth': str(data[4]), 'bhawan': data[5], },
                  'worker_role': data[1], 'salary': data[6], 'shift_start': str(data[7]), 'shift_end': str(data[8])}

    result = {'exists': exists, 'type': _type, 'student': student, 'worker': worker}

    json_data = json.dumps(result)
    return HttpResponse(json_data, content_type="application/json", status=status.HTTP_200_OK)
