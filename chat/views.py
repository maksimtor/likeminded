from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from .models import CustomUser, Gender, ChatGoal, AgePref, Personality, PolitCoordinates, GeoCoordinates, UserInfo, Preferences
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness
from chat.tools.userModTools import convert_user_to_json, create_empty_user, create_user_with_profile, update_user
from .serializers import UserSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from threading import Thread
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
import logging
import json
import pycountry_convert as pc
import time
import threading
import math
logger = logging.getLogger(__name__)

# class UserView(viewsets.ModelViewSet):  
#     serializer_class = UserSerializer   
#     queryset = CustomUser.objects.all()   

@method_decorator(csrf_exempt, name='dispatch')
class UserView(DetailView):
    def get(self, request, user_id):
        print (self)
        print(user_id)
        user = User.objects.get(id=int(user_id))
        return convert_user_to_json(user)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        if data['registration']:
            create_empty_user(data)
            return JsonResponse({'problems': 'none'})
        else:
            custom_user = create_user_with_profile(data)
            print("Created CustomUser " + str(custom_user.pk))
            return JsonResponse({'user_id':custom_user.pk})

    def put(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        update_user(data)
        return JsonResponse({'good': 'good'})

@method_decorator(csrf_exempt, name='dispatch')
class ProfilePhoto(View):
    def post(self, request):
        user_id = request.POST['user_id']
        photo = request.FILES['image']
        user = CustomUser.objects.get(id=user_id)
        user.user_info.photo.save(str(photo), photo)
        print(photo)
        return JsonResponse({'e':'e'})

@method_decorator(csrf_exempt, name='dispatch')
class IgnoreUser(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        print(data['user1'])
        user1_id = int(data['user1'])
        print(data['user2'])
        user2_id = int(data['user2'])
        custom_user_1 = CustomUser.objects.get(id=user1_id)
        custom_user_2 = CustomUser.objects.get(id=user2_id)
        custom_user_1.ignored_users.add(custom_user_2)
        custom_user_1.save()
        return JsonResponse({'result': 'Ignored!'})

@method_decorator(csrf_exempt, name='dispatch')
class ValidateUserRegistration(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        # Getting CustomUser data
        userName = data['username']
        userEmail = data['email']
        usernameExists = User.objects.filter(username=userName)
        emailExists = User.objects.filter(email=userEmail)
        if (usernameExists and emailExists):
            return JsonResponse({'problems': 'both'})
        elif (usernameExists):
            return JsonResponse({'problems': 'username'})
        elif (emailExists):
            return JsonResponse({'problems': 'email'})
        else:
            return JsonResponse({'problems': 'none'})

@method_decorator(csrf_exempt, name='dispatch')
class ValidateLogin(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        userEmail = data['email']
        userPassword = data['password']
        userExists = User.objects.filter(email=userEmail, password=userPassword)
        if (userExists):
            return JsonResponse({'exists': 'yes'})
        else:
            return JsonResponse({'exists': 'no'})