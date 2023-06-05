from rest_framework import serializers
from api.models import *

class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = ['number']

class DepartmentSerializer(serializers.ModelSerializer):
    contact = PhoneSerializer(many=False)

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
    contact = PhoneSerializer(many=False)
    user = MyUserSerializerList(many=False)

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
        fields = ['code', 'name']

class DocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doc_migr_pers
        fields = ['serial_number', 'issued_by', 'issued_when', 'expires_when']

class MigrantSerializerList(serializers.ModelSerializer):
    contact = PhoneSerializer(many=False)
    citizenship = CitizenshipSerializer(many=False)
    document = DocSerializer(many=False)
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
    department = DepartmentSerializer(many=False)
    person = MigrantSerializerList(many=False)

    class Meta:
        model = Registration_Statement
        fields = ['id','department', 'person', 'date', 'status']

class RegistrationStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration_Statement
        fields = ['date']