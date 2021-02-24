from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re
from api.user.models import CustomUser
import sys
# Create your views here.


def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))

import json
@csrf_exempt
def signup(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid paramenter only'})
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        user = CustomUser(
            name=body['name'],
            email=body['email'],
            is_staff=False,
            is_superuser=False,
            phone=body['phone'],
            gender=body['gender'],
        )
        user.set_password(body['password'])
        user.save()
        return JsonResponse({'status': 'successful'})
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if str(exc_obj) == str('UNIQUE constraint failed: user_customuser.email'):
            return JsonResponse({'error': 'Email alredy exist'})
        if str(exc_obj) == str('UNIQUE constraint failed: user_customuser.phone'):
            return JsonResponse({'error': 'Phone alredy exist'})
            
        print('Exception \nline:',exc_tb.tb_lineno,'\nException:',exc_obj,'\ntype:', exc_type)
        return JsonResponse({'status': 'unsuccessful'})

@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid paramenter only'})
    print(request.body)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['email']
    password = body['password']
    # validation part    
    UserModel = get_user_model()

    try:
        if re.match(".+@.+\..+", username):
            print("email")
            user = UserModel.objects.get(email=username)
        if re.match("\d{5}([- ]*)\d{5}",username):
            print("phonr")
            user = UserModel.objects.get(phone=username)
        print(user.check_password(password))
        if user.check_password(password):
            if re.match(".+@.+\..+", username):
                usr_dict = UserModel.objects.filter(
                    email=username).values().first()
            if re.match("\d{5}([- ]*)\d{5}",username):
                usr_dict = UserModel.objects.filter(
                    phone=username).values().first()
            usr_dict.pop('password')
            #if user.session_token != "0":
            #    return JsonResponse({'error': "Previous session exists!"})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'error': 'Invalid password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})

@csrf_exempt
def signout(request, id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user ID'})

    return JsonResponse({'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]
