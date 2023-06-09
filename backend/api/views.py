from rest_framework import generics, viewsets, status, views, filters
from django.db import connection
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.hashers import make_password
from django.db import connection
import django_filters.rest_framework
from api.models import *
from api.serializers import *

# def method_permission_classes(classes):
#     def decorator(func):
#         def decorated_func(self, *args, **kwargs):
#             self.permission_classes = classes
#             # this call is needed for request permissions
#             self.check_permissions(self.request)
#             return func(self, *args, **kwargs)
#         return decorated_func
#     return decorator

class EmployeeViewSet(viewsets.ModelViewSet): 
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerList
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {
        'user__user_type': ['exact'],
        'user__department': ['exact']
    }

    def create(self, request, *args, **kwargs):
        print(request.data)
        print(request)
        q = request.data
        dict_ = q
        if (type(q) != type(dict())):
            dict_ = {k: q.getlist(k) if len(q.getlist(k))>1 else v for k, v in q.items()}
        user_info = request.data.pop('user')
        contact_info = request.data.pop('contact')
        serializer_employee = EmployeeSerializer(data=request.data)
        serializer_user = MyUserSerializer(data=user_info)
        serializer_phone = PhoneSerializer(data=contact_info)
        myuser = None
        if serializer_user.is_valid():
            myuser = MyUser.objects.create_user(**serializer_user.data)
        else:
            return Response({'message': 'Cant create user'}, status=status.HTTP_400_BAD_REQUEST)
        phone, created = Phone.objects.get_or_create(**serializer_phone.initial_data)
        if phone is None:
            MyUser.objects.delete(id=myuser.id)
            return Response({'message': 'Cant create phone'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer_employee.is_valid(raise_exception=True):
            print(phone)
            employee = Employee.objects.create(**serializer_employee.data, user=myuser, contact=phone)
            phone.save()
            myuser.save()
            employee.save()
            return Response(employee.id, status=status.HTTP_201_CREATED)
        else:
            MyUser.objects.delete(id=myuser.id)
            Phone.objects.delete(id=phone.id)
            return Response({'message': 'Cant create employee'}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk is not None:
            employee = Employee.objects.get(id=pk)
            if employee is not None:
                request_expirience = request.data.get('expirience')
                request_salary = request.data.get('salary')
                request_rank = request.data.get('rank')
                request_information = request.data.get('information')
                request_phone = request.data.get('contact')
                request_user = request.data.get('user')
                if request_expirience is not None:
                    employee.expirience = request_expirience
                if request_information is not None:
                    employee.information = request_information
                if request_rank is not None:
                    employee.rank = request_rank
                if request_salary is not None:
                    employee.salary = request_salary
                if request_user is not None:
                    request_email = request_user.get('email')
                    request_user_type = request_user.get('user_type')
                    request_first_name = request_user.get('first_name')
                    request_last_name = request_user.get('last_name')
                    request_department = request_user.get('department')
                    if request_email is not None:
                        employee.user.email = request_email
                    if request_first_name is not None:
                        employee.user.first_name = request_first_name
                    if request_user_type is not None:
                        employee.user.user_type = request_user_type
                    if request_last_name is not None:
                        employee.user.last_name = request_last_name
                    if request_department is not None:
                        employee.user.department.clear()
                        for item in request_department:
                            employee.user.department.add(Department.objects.get(id=item.get('id')))
                if request_phone is not None:
                    employee.phone = Phone.objects.get_or_create(number=request_phone)
                employee.save()
                return Response({'message': 'Employee Patched'}, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response({'message': 'Employee Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'pk in url not found'}, status=status.HTTP_404_NOT_FOUND)

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [IsAuthenticated] 

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated] 

class DocViewSet(viewsets.ModelViewSet):
    queryset = Doc_migr_pers.objects.all()
    serializer_class = DocSerializer
    permission_classes = [IsAuthenticated] 

class MigrantViewSet(viewsets.ModelViewSet):
    queryset = Migrant.objects.all()
    serializer_class = MigrantSerializerList
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        q = request.data
        dict_ = q
        if (type(q) != type(dict())):
            dict_ = {k: q.getlist(k) if len(q.getlist(k))>1 else v for k, v in q.items()}
        print(dict_)
        citizenship_info = request.data.pop('citizenship')
        doc_info = request.data.pop('document')
        phone_info = request.data.pop('contact')
        serializer_citizen = CitizenshipSerializer(data=citizenship_info)
        serializer_phone = PhoneSerializer(data=phone_info)
        serializer_doc = DocSerializer(data=doc_info)
        serializer_migrant = MigrantSerializer(data=request.data)
        citizen, creat = Citizenship.objects.get_or_create(**serializer_citizen.initial_data)
        if serializer_migrant.is_valid():
            phone, create = Phone.objects.get_or_create(**serializer_phone.initial_data)
            doc, created = Doc_migr_pers.objects.get_or_create(**serializer_doc.initial_data)
            migrant = Migrant.objects.create(**serializer_migrant.data, citizenship=citizen, contact=phone, document=doc)
            citizen.save()
            phone.save()
            doc.save()
            migrant.save()
            return Response(serializer_migrant.data, status.HTTP_201_CREATED)
        return Response({'message': 'Migrant info is not valid'}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request,*args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk is None:
            return Response({'message': 'Cant find pk in url'}, status=status.HTTP_404_NOT_FOUND)
        migrant = Migrant.objects.get(id=pk)
        if migrant is None:
            return Response({'message': 'Migrant Not Found'}, status=status.HTTP_404_NOT_FOUND)
        request_phone = request.data.get('contact')
        request_citizen = request.data.get('citizenship')
        request_name = request.data.get('name')
        request_address = request.data.get('address')
        request_birthday = request.data.get('birthday')
        request_birthday_place = request.data.get('birthday_place')
        request_profession = request.data.get('profession')
        request_status = request.data.get('status')
        if request_phone is not None:
            migrant.phone = Phone.objects.get(number=request_phone)
        if request_citizen is not None:
            migrant.citizenship = Citizenship.objects.get(name=request_citizen)
        if request_name is not None:
            migrant.name = request_name
        if request_address is not None:
            migrant.address = request_address
        if request_birthday is not None:
            migrant.birthday = request_birthday
        if request_birthday_place is not None:
            migrant.birthday_place = request_birthday_place
        if request_profession is not None:
            migrant.profession = request_profession
        if request_status is not None:
            migrant.status = request_status
        migrant.save()
        return Response({'message': 'Migrant Patched'}, status=status.HTTP_206_PARTIAL_CONTENT)

class RegistrationStatementViewSet(viewsets.ModelViewSet):
    # queryset = Registration_Statement.objects.all()
    serializer_class = RegistrationStatemenetSerializerList

    def get_queryset(self):
        with connection.cursor() as cursor:
            if self.request.user.user_type == 'admin':
                print("Admin")
                return Registration_Statement.objects.all()
            if self.request.user.user_type == 'employee':
                cursor.execute(f'SET ROLE employee_{self.request.user.id}')
                print("Employee")
                return Registration_Statement.objects.filter(status="pending")
            if self.request.user.user_type == 'department_dir':
                cursor.execute(f'SET ROLE department_dir_{self.request.user.id}')
                print("Department_dir")
                return Registration_Statement.objects.filter(status="approval")
            if self.request.user.user_type == 'analyst':
                cursor.execute(f'SET ROLE analyst')
                return Registration_Statement.objects.all()

    def create(self, request, *args, **kwargs):
        q = request.data
        dict_ = q
        if (type(q) != type(dict())):
            dict_ = {k: q.getlist(k) if len(q.getlist(k))>1 else v for k, v in q.items()}
        serializer = RegistrationStatementSerializer(data=dict_)
        with connection.cursor() as cursor:
            if self.request.user.user_type == 'employee':
                cursor.execute(f'SET ROLE employee_{self.request.user.id}')
            if self.request.user.user_type == 'department_dir':
                cursor.execute(f'SET ROLE department_dir_{self.request.user.id}')
            if self.request.user.user_type == 'analyst':
                cursor.execute(f'SET ROLE analyst')
        if serializer.is_valid():
            department = Department.objects.get(address=dict_.get('department'))
            if department is None:
                return Response({'message': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
            person = Migrant.objects.get(id=dict_.get('migrant'))
            if person is None:
                return Response({'message': 'Migrant not found'}, status=status.HTTP_404_NOT_FOUND)
            statement = Registration_Statement.objects.create(department=department, person=person, **serializer.data)
            statement.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

class UnRegistrationStatementViewSet(viewsets.ModelViewSet):
    # queryset = Unregistration_Statement.objects.all()
    serializer_class = RegistrationStatemenetSerializerList

    def get_queryset(self):
        with connection.cursor() as cursor:
            if self.request.user.user_type == 'admin':
                print("Admin")
                return Unregistration_Statement.objects.all()
            if self.request.user.user_type == 'employee':
                cursor.execute(f'SET ROLE employee_{self.request.user.id}')
                print("Employee")
                return Unregistration_Statement.objects.filter(status="pending")
            if self.request.user.user_type == 'department_dir':
                cursor.execute(f'SET ROLE department_dir_{self.request.user.id}')
                print("Department_dir")
                return Unregistration_Statement.objects.filter(status="approval")
            if self.request.user.user_type == 'analyst':
                return Unregistration_Statement.objects.all()

    def create(self, request, *args, **kwargs):
        q = request.data
        dict_ = q
        if (type(q) != type(dict())):
            dict_ = {k: q.getlist(k) if len(q.getlist(k))>1 else v for k, v in q.items()}
        serializer = RegistrationStatementSerializer(data=dict_)
        with connection.cursor() as cursor:
            if self.request.user.user_type == 'employee':
                cursor.execute(f'SET ROLE employee_{self.request.user.id}')
            if self.request.user.user_type == 'department_dir':
                cursor.execute(f'SET ROLE department_dir_{self.request.user.id}')
            if self.request.user.user_type == 'analyst':
                cursor.execute(f'SET ROLE analyst')
        if serializer.is_valid():
            department = Department.objects.get(address=dict_.get('department'))
            if department is None:
                return Response({'message': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
            person = Migrant.objects.get(id=dict_.get('migrant'))
            if person is None:
                return Response({'message': 'Migrant not found'}, status=status.HTTP_404_NOT_FOUND)
            statement = Registration_Statement.objects.create(department=department, person=person, **serializer.data)
            statement.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

class ReportRegStatement(views.APIView):

    def get(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if ((user_type != 'admin') and (user_type != 'analyst')):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        with connection.cursor() as cur:
            cur.execute('CALL report_registration_statement()')
        return Response({'message': user_type}, status=status.HTTP_200_OK)

class ReportUnRegStatements(views.APIView):

    def get(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if ((user_type != 'admin') and (user_type != 'analyst')):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        with connection.cursor() as cur:
            cur.execute('CALL report_unregistration_statement()')
        return Response({'message': user_type}, status=status.HTTP_200_OK)
    
class UpdateAppRegStatus(views.APIView):

    def patch(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if (user_type == 'employee'):
            print(request.data)
            id_doc = request.data['id']
            state = Registration_Statement.objects.get(id=id_doc)
            state.status = 'approval'
            state.save()
            return Response({'message': user_type}, status=status.HTTP_200_OK)
        if (user_type != 'department_dir'):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        print(request.data)
        id = request.data['id']
        with connection.cursor() as cur:
            cur.execute(f'Select "update_reg_status"({id})')
        return Response({'message': user_type}, status=status.HTTP_200_OK)

class UpdateAppUnRegStatus(views.APIView):

    def patch(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if (user_type == 'employee'):
            id_doc = request.data['id']
            state = Unregistration_Statement.objects.get(id=id_doc)
            state.status = 'approval'
            state.save()
            return Response({'message': user_type}, status=status.HTTP_200_OK)
        if (user_type != 'department_dir'):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        print(request.data)
        id = request.data['id']
        with connection.cursor() as cur:
            cur.execute(f'Select "update_unreg_status"({id})')
        return Response({'message': user_type}, status=status.HTTP_200_OK)

class UpdateDecRegStatus(views.APIView):

    def patch(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        id_doc = request.data['id']
        state = Registration_Statement.objects.get(id=id_doc)
        state.status = "declined"
        state.save()
        return Response({'message': user_type}, status=status.HTTP_200_OK)

class UpdateDecUnRegStatus(views.APIView):

    def patch(self, request, format=None):
        try:
            user_type = request.user.user_type
        except AttributeError:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        id_doc = request.data['id']
        state = Unregistration_Statement.objects.get(id=id_doc)
        state.status = "declined"
        state.save()
        with connection.cursor() as cur:
            cur.execute(f'Select "update_unreg_status"({id})')
        return Response({'message': user_type}, status=status.HTTP_200_OK)


# Create your views here.
