from django.db import connection
from rest_framework.request import Request as RestFrameworkRequest
from rest_framework.views import APIView



class RlsMiddleware(object):
    def __init__ (self, get_response):
        self.get_response = get_response
        
    #https://stackoverflow.com/questions/26240832/django-and-middleware-which-uses-request-user-is-always-anonymous
    # def __call__ (self, request):
    #     if request.path.startswith('/admin/'):
    #         return self.get_response(request)
    #     drf_request: RestFrameworkRequest = APIView().initialize_request(request) 
    #     user_id = drf_request.user.id
    #     if user_id is not None:
    #         print(f'user_is is: {user_id}')
    #         user = MyUser.objects.get(id=user_id)
    #         user_type = user.user_type
    #         with connection.cursor() as cursor:
    #             if user_type == 2:
    #                 cursor.execute('SET ROLE master')
    #             elif user_type == 3:
    #                 cursor.execute('SET ROLE manager')
    #             elif user_type == 4:
    #                 cursor.execute('SET ROLE analyst')
    #             elif user_type == 5 and not user.is_staff:
    #                 cursor.execute(f'SET ROLE salon_dir_{user_id}')
    #             elif user_type == 1:
    #                 cursor.execute(f'SET ROLE client')
    #             else:
    #                 cursor.execute(f'SET ROLE postgres')
    #     response = self.get_response(request)
    #     return response
    def __call__(self, request):
        print(request)
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        print(request)
        drf_request: RestFrameworkRequest = APIView().initialize_request(request)
        user_id = drf_request.user.id
        print(f'user_id is: {user_id}')
        print('Hello!')