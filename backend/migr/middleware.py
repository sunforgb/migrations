from django.db import connection
from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView
from api.models import MyUser


class RlsMiddleware(object):
    def __init__ (self, get_response):
        self.get_response = get_response
        
    #https://stackoverflow.com/questions/26240832/django-and-middleware-which-uses-request-user-is-always-anonymous
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        if request.path.startswith('/api/users'):
            return self.get_response(request)
        if request.path.startswith('/api/'):
            return self.get_response(request)
        drf_request: RestFrameworkRequest = APIView().initialize_request(request) 
        user_id = drf_request.user.id
        if user_id is not None:
            user = MyUser.objects.get(id=user_id)
            user_type = user.user_type
            with connection.cursor() as cursor:
                if user_type == 'employee':
                    cursor.execute(f'SET ROLE employee_{user.id}')
                elif user_type == 'analyst':
                    cursor.execute('SET ROLE analyst')
                elif user_type == 'department_dir':
                    cursor.execute(f'SET ROLE department_dir_{user.id}')
                else:
                    cursor.execute(f'SET ROLE postgres')
        response = self.get_response(request)
        return response