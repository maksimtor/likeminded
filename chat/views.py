from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from .models import CustomUser, Chat, Gender, ChatGoal, AgePref, Personality, PolitCoordinates, GeoCoordinates, UserInfo, Preferences, SearchingInstance, ChatRoom
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness
from .serializers import UserSerializer, ChatSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync, sync_to_async
from threading import Thread
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
import logging
import json
import pycountry_convert as pc
import time
import threading
logger = logging.getLogger(__name__)

class UserView(viewsets.ModelViewSet):  
    serializer_class = UserSerializer   
    queryset = CustomUser.objects.all()   

class ChatView(viewsets.ModelViewSet):  
    serializer_class = ChatSerializer   
    queryset = Chat.objects.all()

@csrf_exempt
def get_most_like_minded(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)
    user_id = data['user_id']
    user = User.objects.get(id=user_id)
    userProfile = user.profile

    users = User.objects.all()
    accepted_users = [{'id': 0, 'like_mindness': 0}]
    for u in users:
        potential_profile = u.profile
        if (calcAcceptance(mainUser=userProfile, targetUser=potential_profile) == 1 and calcAcceptance(mainUser=potential_profile, targetUser=userProfile) == 1):
            l1 = calcLikeness(mainUser=userProfile, targetUser=potential_profile)
            l2 = calcLikeness(mainUser=potential_profile, targetUser=userProfile)
            result = (l1+l2)/2
            accepted_users.append({'id': u.profile.id, 'like_mindness': result})
    result_users = sorted(accepted_users, key=lambda d: d['like_mindness'], reverse=True)[0:2]
    print(result_users)
    return JsonResponse({'result': result_users})

@csrf_exempt
def validate_user_does_not_exists(request):
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

@csrf_exempt
def validate_login(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    # Getting CustomUser data
    userEmail = data['email']
    userPassword = data['password']
    userExists = User.objects.filter(email=userEmail, password=userPassword)
    if (userExists):
        return JsonResponse({'exists': 'yes'})
    else:
        return JsonResponse({'exists': 'no'})

@csrf_exempt
def create_real_user(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    username = data['username']
    email = data['email']
    password = data['password']
    hu = User.objects.create_user(username=username, email=email, password=password)
    hu.save()
    pc = PolitCoordinates.objects.create(eco=0, cult=0)
    pc.save()
    gc = GeoCoordinates.objects.create(lat=0, lon=0)
    gc.save()
    pers = Personality.objects.create(extraversion=0.5, agreeableness=0.5, conscientiousness=0.5, openness=0.5, neuroticism=0.5)
    pers.save()
    info = UserInfo.objects.create(polit_coordinates=pc, location=gc, personality=pers)
    info.save()

    ap = AgePref.objects.create(min_age=18, max_age=100, optimal_age=25)
    ap.save()
    prefs = Preferences.objects.create(age=ap)
    prefs.save()
    u = CustomUser.objects.create(user=hu, userInfo=info, userPrefs=prefs)
    u.save()
    return JsonResponse({'problems': 'none'})

@csrf_exempt
def get_user_profile(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user_id'])
    user_id = data['user_id']
    user = User.objects.get(id=int(user_id))
    custom_user = user.profile
    print(custom_user)
    user_data = {
        'name': user.username,
        'age': custom_user.userInfo.age,
        'gender': custom_user.userInfo.gender,
        'languages': custom_user.userInfo.languages,
        'interests': custom_user.userInfo.interests,
        'country': custom_user.userInfo.country,
        'locToggle': custom_user.userInfo.location != None,
        'geoLat': custom_user.userInfo.location.lat,
        'geoLon': custom_user.userInfo.location.lon,
        'polEco': custom_user.userInfo.polit_coordinates.eco*10,
        'polGov': custom_user.userInfo.polit_coordinates.cult*10,
        'personalityExtraversion': custom_user.userInfo.personality.extraversion*10,
        'personalityAgreeableness': custom_user.userInfo.personality.agreeableness*10,
        'personalityOpenness': custom_user.userInfo.personality.openness*10,
        'personalityConscientiousness': custom_user.userInfo.personality.conscientiousness*10,
        'personalityNeuroticism': custom_user.userInfo.personality.neuroticism*10,
        'politPref': custom_user.userPrefs.polit,
        'intPref': custom_user.userPrefs.interests,
        'locPref': custom_user.userPrefs.location,
        'areaPref': custom_user.userPrefs.loc_area,
        'persPref': custom_user.userPrefs.personality,
        'goals': custom_user.userPrefs.goals,
        'genderPref': custom_user.userPrefs.gender,
        'ageRange': [custom_user.userPrefs.age.min_age, custom_user.userPrefs.age.max_age],
        'ageOptimal': custom_user.userPrefs.age.optimal_age
    }
    print(user_data)
    return JsonResponse(user_data)

@csrf_exempt
def get_user_chats(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user_id'])
    user_id = data['user_id']
    chat_ids = []
    chats = CustomUser.objects.get(id=int(user_id)).chats.all()
    for c in chats:
        chat_ids.append(c.id)
    print(chat_ids)
    return JsonResponse({'chat_ids': chat_ids})

@csrf_exempt
def create_chat_room(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user1'])
    user1_id = int(data['user1'])
    print(data['user2'])
    user2_id = int(data['user2'])
    chat_room = ChatRoom.objects.create()
    chat_room.participants.add(CustomUser.objects.get(id=user1_id))
    chat_room.participants.add(CustomUser.objects.get(id=user2_id))
    return JsonResponse({'chat_ids': ''})

@csrf_exempt
def create_user(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)
    userName = data['name']
    userAge = data['age']
    userGender = data['gender']['value']
    userCountry = None
    if (userGender == 'M'):
        userGender = Gender.MALE
    elif (userGender == 'F'):
        userGender = Gender.FEMALE
    else:
        userGender = Gender.ANYTHING
    userLanguages = data['languages']
    userLanguagesReformed = []
    for l in userLanguages:
        userLanguagesReformed.append(l['value'])
    userInterests = data['interests']
    userInterestsReformed = []
    for i in userInterests:
        userInterestsReformed.append(i['value'])
    userGeoLat = data['geoLat']
    userGeoLon = data['geoLon']
    userLocToggle = data['locToggle']
    userPolEco = data['polEco']/10
    userPolGov = data['polGov']/10
    userPersonalityExtraversion = data['personalityExtraversion']/10
    userPersonalityAgreeableness = data['personalityAgreeableness']/10
    userPersonalityOpenness = data['personalityOpenness']/10
    userPersonalityConscientiousness = data['personalityConscientiousness']/10
    userPersonalityNeuroticism = data['personalityNeuroticism']/10
    userPolitPref = data['politPref']
    userIntPref = data['intPref']
    userLocPref = data['locPref']
    # userAreaPref = data['areaPref']
    userAreaPrefReformed = []
    # for i in userAreaPref:
    #     userAreaPrefReformed.append(i['value'])
    userPersPref = data['persPref']
    userGoals = data['goals']['value']
    if (userGoals == 'FR'):
        userGoals = ChatGoal.FRIENDSHIP
    elif (userGoals == 'RO'):
        userGoals = ChatGoal.ROMANTIC
    else:
        userGoals = ChatGoal.ANYTHING
    userGenderPref = data['genderPref']['value']
    if (userGenderPref == 'M'):
        userGenderPref = Gender.MALE
    elif (userGenderPref == 'F'):
        userGenderPref = Gender.FEMALE
    else:
        userGenderPref = Gender.ANYTHING
    userAgeRange = data['ageRange']
    userAgeOptimal = data['ageOptimal']
    
    age_pref = AgePref.objects.create(min_age=userAgeRange[0], max_age=userAgeRange[1], optimal_age=userAgeOptimal)
    age_pref.save()
    personality = Personality.objects.create(
        extraversion=userPersonalityExtraversion,
        agreeableness=userPersonalityAgreeableness,
        openness=userPersonalityOpenness,
        conscientiousness=userPersonalityConscientiousness,
        neuroticism=userPersonalityNeuroticism
    )
    personality.save()
    pol = PolitCoordinates.objects.create(eco=userPolEco, cult=userPolGov)
    pol.save()
    geo = None
    if (userLocToggle):
        print('save geo')
        geo = GeoCoordinates.objects.create(lat=userGeoLat, lon=userGeoLon)
        geo.save()
    user_info = UserInfo.objects.create(
        country=userCountry,
        languages=userLanguagesReformed,
        interests=userInterestsReformed,
        polit_coordinates=pol,
        location=geo,
        age=userAge if isinstance(userAge, int) else None,
        gender=userGender,
        personality=personality
        )
    user_info.save()
    user_pref = Preferences.objects.create(
        goals=userGoals,
        age=age_pref,
        polit=userPolitPref,
        interests=userIntPref,
        location=userLocPref,
        gender=userGenderPref,
        personality=userPersPref,
        loc_area=None
        )
    user_pref.save()
    custom_user = CustomUser.objects.create(name=userName, userInfo=user_info, userPrefs=user_pref)
    custom_user.save()
    print("Created CustomUser " + str(custom_user.pk))
    return JsonResponse({'user_id':custom_user.pk})


@csrf_exempt
def update_profile(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    # Getting CustomUser data
    userId = data['user_id']
    userName = data['name']
    userAge = data['age']
    userGender = data['gender']['value']
    userCountry = None
    if (userGender == 'M'):
        userGender = Gender.MALE
    elif (userGender == 'F'):
        userGender = Gender.FEMALE
    else:
        userGender = Gender.ANYTHING
    userLanguages = data['languages']
    userLanguagesReformed = []
    if (userLanguages):
        for l in userLanguages:
            userLanguagesReformed.append(l['value'])
    userInterestsReformed = []
    if 'interests' in data.keys():
        userInterests = data['interests']
        for i in userInterests:
            userInterestsReformed.append(i['value'])
    userGeoLat = data['geoLat']
    print(userGeoLat)
    userGeoLon = data['geoLon']
    userPolEco = data['polEco']/10
    userPolGov = data['polGov']/10
    userPersonalityExtraversion = data['personalityExtraversion']/10
    print(userPersonalityExtraversion)
    userPersonalityAgreeableness = data['personalityAgreeableness']/10
    userPersonalityOpenness = data['personalityOpenness']/10
    userPersonalityConscientiousness = data['personalityConscientiousness']/10
    userPersonalityNeuroticism = data['personalityNeuroticism']/10
    userPolitPref = data['politPref']
    userIntPref = data['intPref']
    userLocPref = data['locPref']
    # userAreaPref = data['areaPref']
    userAreaPrefReformed = []
    # for i in userAreaPref:
    #     userAreaPrefReformed.append(i['value'])
    userPersPref = data['persPref']
    userGoals = data['goals']['value']
    if (userGoals == 'FR'):
        userGoals = ChatGoal.FRIENDSHIP
    elif (userGoals == 'RO'):
        userGoals = ChatGoal.ROMANTIC
    else:
        userGoals = ChatGoal.ANYTHING
    userGenderPref = data['genderPref']['value']
    if (userGenderPref == 'M'):
        userGenderPref = Gender.MALE
    elif (userGenderPref == 'F'):
        userGenderPref = Gender.FEMALE
    else:
        userGenderPref = Gender.ANYTHING
    userAgeRange = data['ageRange']
    userAgeOptimal = data['ageOptimal']

    user = User.objects.get(id=userId)
    user.username = userName
    profile = user.profile

    info = profile.userInfo
    info.country=userCountry
    info.languages=userLanguagesReformed
    info.interests=userInterestsReformed
    pol = info.polit_coordinates
    pol.eco=userPolEco
    pol.cult=userPolGov
    pol.save()
    info.polit_coordinates=pol
    geo = info.location
    geo.lat=userGeoLat
    geo.lon=userGeoLon
    geo.save()
    info.location=geo
    info.age=userAge
    print(info.location.lat)
    info.gender=userGender
    personality=info.personality
    personality.extraversion=userPersonalityExtraversion
    personality.agreeableness=userPersonalityAgreeableness
    personality.openness=userPersonalityOpenness
    personality.conscientiousness=userPersonalityConscientiousness
    personality.neuroticism=userPersonalityNeuroticism
    print(personality.extraversion)
    personality.save()
    info.personality=personality
    info.save()


    prefs = profile.userPrefs
    prefs.goals=userGoals
    prefs.polit=userPolitPref
    prefs.interests=userIntPref
    prefs.location=userLocPref
    prefs.gender=userGenderPref
    prefs.personality=userPersPref
    prefs.loc_area=None
    age_pref = prefs.age
    age_pref.min_age=userAgeRange[0]
    age_pref.max_age=userAgeRange[1]
    age_pref.optimal_age=userAgeOptimal
    age_pref.save()
    prefs.age_pref = age_pref
    prefs.save()

    profile.userInfo = info
    profile.userPrefs = prefs
    profile.save()
    user.save()
    print(user.profile.userInfo.location.lat)
    return JsonResponse({'good': 'good'})

@permission_classes([IsAuthenticated])
def get_chats(request):
    CustomUser = request.CustomUser
    pass

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def room_for_searching(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })