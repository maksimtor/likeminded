from django.test import TestCase
from chat.models import User, UserInfo, ChatGoal, PolitCoordinates, GeoCoordinates, Gender, Preferences, AgePref, Personality
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness
from random import randrange
import pycountry

def create_random_user():
    # pol eco
    pol_eco = randrange(-10,10)/10
    # pol cult
    pol_cult = randrange(-10,10)/10
    # geo lat
    geo_lat = randrange(-90,90)
    # geo lon
    geo_lon = randrange(-180,80)
    # langs
    # countries = [country.alpha2 for country in pycountry.countries]
    countries = list(pycountry.countries)
    langs = [countries[randrange(0,len(countries))].alpha_2, countries[randrange(0,len(countries))].alpha_2]
    if (randrange(0,20) != 0):
        langs[0] = 'RU'
    # interests
    interests = ['Music', 'Movies', 'Art', 'Hiking', 'Intenet', 'Books', 'Fashion', 'Sport']
    my_interests = []
    for interest in interests:
        if (randrange(0,2) == 0):
            my_interests.append(interest)
    # age
    age = randrange(18, 50)
    # gender
    gender=Gender.MALE
    rn = randrange(1,3)
    if (rn==1):
        gender=Gender.FEMALE
    # goals null?
    goals = ChatGoal.ANYTHING
    rn = randrange(1,10)
    if (rn == 1):
        goals = ChatGoal.FRIENDSHIP
    elif (rn == 2):
        goals = ChatGoal.ROMANTIC
    # age prefs null?
    age_pref = None
    if (randrange(0,2) == 1):
        age_pref_min = randrange(18, 40)
        age_pref_max = randrange(age_pref_min+1, 100)
        age_pref_opt = randrange(age_pref_min, age_pref_max)
        age_pref = AgePref.objects.create(min_age=age_pref_min, max_age=age_pref_max, optimal_age=age_pref_opt)
        age_pref.save()
    # polit boolean
    polit = False
    if (randrange(0,4) != 1):
        polit = True
    # int bool
    inter = False
    if (randrange(0,4) != 1):
        inter = True
    # loc bool
    locat = False
    if (randrange(0,4) != 1):
        locat = True

    loc_area = ['RU']

    personality_bool = False
    if (randrange(0,4) != 1):
        personality_bool = True
    personality = Personality.objects.create(extraversion=(randrange(0,10)/10), agreeableness=(randrange(0,10)/10), openness=(randrange(0,10)/10), conscientiousness=(randrange(0,10)/10), neuroticism=(randrange(0,10)/10))

    # gender bool
    pref_gender = Gender.ANYTHING
    rn = randrange(0,10)
    if (rn == 1):
        pref_gender = Gender.FEMALE
    elif (rn == 2):
        pref_gender = Gender.MALE


    pol = PolitCoordinates.objects.create(eco=pol_eco, cult=pol_cult)
    pol.save()
    geo = GeoCoordinates.objects.create(lat=geo_lat, lon=geo_lon)
    geo.save()
    user_info = UserInfo.objects.create(
        languages=langs,
        interests=my_interests,
        country='DE',
        polit_coordinates=pol,
        location=geo,
        age=age,
        gender=gender,
        personality=personality
        )
    user_info.save()
    user_pref = Preferences.objects.create(
        goals=goals,
        age=age_pref,
        polit=polit,
        interests=inter,
        location=locat,
        gender=pref_gender,
        personality=personality_bool,
        loc_area=loc_area
        )
    user_pref.save()
    user = User.objects.create(name="Maksimmas", userInfo=user_info, userPrefs=user_pref)
    user.save()
    print(user)
    return user

class AcceptanceTestCase(TestCase):
    def test_animals_can_speak(self):
        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))

        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))

        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))
        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))
        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))

        print('\n')
        user1 = create_random_user()
        user2 = create_random_user()
        print(calcAcceptance(mainUser=user1, targetUser=user2))
        print(calcAcceptance(mainUser=user2, targetUser=user1))

        if (calcAcceptance(mainUser=user1, targetUser=user2) == 1 and calcAcceptance(mainUser=user1, targetUser=user2) == 1):
            print(calcLikeness(mainUser=user1, targetUser=user2))
            print(calcLikeness(mainUser=user2, targetUser=user1))
