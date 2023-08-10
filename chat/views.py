from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from .models import CustomUser, Gender, ChatGoal, AgePref, Personality, PolitCoordinates, GeoCoordinates, UserInfo, Preferences
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness
from .serializers import CustomUserSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from threading import Thread
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
import logging
import json
import pycountry_convert as pc
import time
import threading
import math
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
logger = logging.getLogger(__name__)
from django.views.decorators.http import require_http_methods

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()