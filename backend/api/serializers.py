from rest_framework import serializers
from api.models import *

class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = ['number']

class DepartmentSerializer(serializers.ModelSerializer):
    contact = PhoneSerializer(many=True)

    class Meta:
        model = Department
        fields = ['address','contact','post_index']

class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['email', 'first_name',
                  'last_name', 'user_type',
                  'password']

class MyUserSerializerList(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'user_type',
                  'department']

class EmployeeSerializerList(serializers.ModelSerializer):
    contact = PhoneSerializer(many=True)
    user = MyUserSerializerList(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'expirience',
                  'salary','contact','rank','information']

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['expirience', 'salary', 'rank', 'information']

class CitizenshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizenship
        fields = ['code','name']

class DocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doc_migr_pers
        fields = ['serial_number', 'issued_by', 'issued_when', 'expires_when']

class MigrantSerializerList(serializers.ModelSerializer):
    contact = PhoneSerializer(many=True)
    citizenship = CitizenshipSerializer(many=True)
    document = DocSerializer(many=True)
    class Meta:
        model = Migrant
        fields = ['name', 'address', 'birthday',
                'birthday_place','citizenship','profession',
                'contact', 'document', 'status']

class MigrantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Migrant
        fields = ['name', 'address', 'birthday', 'birthday_place', 'profession']


class RegistrationStatemenetSerializerList(serializers.ModelSerializer):
    department = DepartmentSerializer(many=True)
    person = MigrantSerializerList(many=True)

    class Meta:
        model = Registration_Statement
        fields = ['department', 'person', 'date', 'status']

class RegistrationStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration_Statement
        fields = ['date']