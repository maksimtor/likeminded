from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from .models import HistoricalChat, CustomUser, Chat, Gender, ChatGoal, AgePref, Personality, PolitCoordinates, GeoCoordinates, UserInfo, Preferences, SearchingInstance, ChatRoom
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
def create_historical_chat(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user1'])
    user1_id = int(data['user1'])
    print(data['user2'])
    user2_id = int(data['user2'])

    chat = HistoricalChat.objects.create(chattedWith=CustomUser.objects.get(id=user2_id))
    chat.save()
    me = CustomUser.objects.get(id=user1_id)
    me.historicalChats.add(chat)
    me.save()
    return JsonResponse({'chat_ids': ''})

@csrf_exempt
def get_historical_chats(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user_id'])
    user_id = data['user_id']
    reformed_chats = []
    chats = CustomUser.objects.get(id=int(user_id)).historicalChats.all()
    print(CustomUser.objects.get(id=int(user_id)).user.username)
    for c in chats:
        reformed_chats.append({'id': c.chattedWith.id, 'name':c.chattedWith.name, 'timestamp': c.timestamp})
    print(reformed_chats)
    return JsonResponse({'result': reformed_chats})

@csrf_exempt
def get_most_like_minded(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)
    user_id = data['user_id']
    user = User.objects.get(id=user_id)
    userProfile = user.profile

    users = User.objects.all()
    accepted_users = []
    for u in users:
        potential_profile = u.profile
        if (calcAcceptance(mainUser=userProfile, targetUser=potential_profile) == 1 and calcAcceptance(mainUser=potential_profile, targetUser=userProfile) == 1 and potential_profile!=userProfile and potential_profile not in userProfile.sentFriendRequests.all() and potential_profile not in userProfile.ignoredUsers.all() and potential_profile not in userProfile.usersIgnoredBy.all() and potential_profile not in userProfile.friends.all()):
            l1 = calcLikeness(mainUser=userProfile, targetUser=potential_profile)
            l2 = calcLikeness(mainUser=potential_profile, targetUser=userProfile)
            result = (l1+l2)/2
            accepted_users.append({'id': u.profile.id, 'like_mindness': result, 'name': u.username})
    result_users = sorted(accepted_users, key=lambda d: d['like_mindness'], reverse=True)[0:10]
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
        'interests': custom_user.userInfo.interests,
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
        'areaRestrictToggle': custom_user.userPrefs.area_restrict,
        'persPref': custom_user.userPrefs.personality,
        'goals': custom_user.userPrefs.goals,
        'genderPref': custom_user.userPrefs.gender,
        'ageRange': [custom_user.userPrefs.age.min_age, custom_user.userPrefs.age.max_age],
        'ageOptimal': custom_user.userPrefs.age.optimal_age,
        'description': custom_user.userInfo.description
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
    cu = CustomUser.objects.get(id=int(user_id))
    chats = CustomUser.objects.get(id=int(user_id)).chats.all()
    for c in chats:
        print(c.participants.exclude(id=user_id)[0].id)
        friend = c.participants.exclude(id=user_id)[0]
        if friend not in cu.ignoredUsers.all() and cu not in friend.ignoredUsers.all():
            chat_ids.append({'chat_id': c.id, 'user_id': c.participants.exclude(id=user_id)[0].id, 'last_message': c.messages.order_by('-timestamp').all()[0].message, 'read_last_message': c.messages.order_by('-timestamp').all()[0].read})
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
def send_friend_request(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user1'])
    user1_id = int(data['user1'])
    print(data['user2'])
    user2_id = int(data['user2'])
    custom_user_1 = CustomUser.objects.get(id=user1_id)
    custom_user_2 = CustomUser.objects.get(id=user2_id)
    if custom_user_2 in custom_user_1.receivedFriendRequests.all():
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(CustomUser.objects.get(id=user1_id))
        chat_room.participants.add(CustomUser.objects.get(id=user2_id))
        custom_user_1.friends.add(custom_user_2)
        custom_user_2.friends.add(custom_user_1)
        custom_user_1.save()
        custom_user_2.save()
        return JsonResponse({'result': 'Match!'})
    else:
        custom_user_1.sentFriendRequests.add(custom_user_2)
        custom_user_1.save()
        custom_user_2.save()
        return JsonResponse({'result': 'Request sent!'})

@csrf_exempt
def ignore_user(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data['user1'])
    user1_id = int(data['user1'])
    print(data['user2'])
    user2_id = int(data['user2'])
    custom_user_1 = CustomUser.objects.get(id=user1_id)
    custom_user_2 = CustomUser.objects.get(id=user2_id)
    custom_user_1.ignoredUsers.add(custom_user_2)
    custom_user_1.save()
    return JsonResponse({'result': 'Ignored!'})

@csrf_exempt
def read_messages(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    chat_id = int(data['chat_id'])
    friend_id = int(data['friend_id'])
    messages = ChatRoom.objects.get(id=chat_id).messages.filter(user=CustomUser.objects.get(id=friend_id).user)
    for m in messages:
        m.read = True
        m.save()
    print(messages)
    return JsonResponse({'result': 'Read!'})

@csrf_exempt
def create_user(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)
    userName = data['name']
    userAge = data['age']
    userGender = data['gender']['value']
    userAreaRestrictToggle=data['areaRestrictToggle']
    userLocPref=data['locPref']
    userAreaPref=data['areaPref']
    if (userGender == 'M'):
        userGender = Gender.MALE
    elif (userGender == 'F'):
        userGender = Gender.FEMALE
    else:
        userGender = Gender.ANYTHING
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
        area_restrict=userAreaRestrictToggle,
        loc_area=userAreaPref,
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
    userDescription = data['description']
    userAge = data['age']
    userAreaRestrictToggle=data['areaRestrictToggle']
    userLocPref=data['locPref']
    userAreaPref=data['areaPref']
    print('area pref')
    print(userAreaPref)
    userGender = data['gender']['value']
    if (userGender == 'M'):
        userGender = Gender.MALE
    elif (userGender == 'F'):
        userGender = Gender.FEMALE
    else:
        userGender = Gender.ANYTHING
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
    userAreaPref = data['areaPref']
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
    info.interests=userInterestsReformed
    info.description=userDescription
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
    prefs.area_restrict=userAreaRestrictToggle
    prefs.loc_area=userAreaPref
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