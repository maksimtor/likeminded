from django.test import TestCase
from chat.models import CustomUser, UserInfo, ChatGoal, PolitCoordinates, GeoCoordinates, Gender, Preferences, AgePref, Personality
from django.contrib.auth.models import User
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness, AcceptanceCalculator, LikenessCalculator
from random import randrange
import pycountry
import string
import random
from django.test import Client, TestCase
import json
from chat.consumers import ChatSearchConsumer
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import include, re_path
from asgiref.sync import sync_to_async

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
	else:
		age_pref = AgePref.objects.create(min_age=18, max_age=100, optimal_age=20)
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

	area_restrict = False
	if (randrange(0,4) != 1):
		area_restrict = True

	loc_area = randrange(0,20000)

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
		area_restrict=area_restrict,
		loc_area=loc_area
		)
	user_pref.save()
	user = CustomUser.objects.create(name="Maksimmas", user_info=user_info, user_prefs=user_pref)
	user.save()

	username = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
	email = username + '@gmail.com'
	real_user = User.objects.create_user(username=username, email=email, password='123')
	user.user = real_user
	user.save()
	print(user)
	return user

def create_empty_user():
	personality = Personality.objects.create(extraversion=0.5, agreeableness=0.5, openness=0.5, conscientiousness=0.5, neuroticism=0.5)
	pol = PolitCoordinates.objects.create(eco=0, cult=0)
	pol.save()
	geo = GeoCoordinates.objects.create(lat=0, lon=0)
	geo.save()
	user_info = UserInfo.objects.create(
		languages=['RU'],
		interests=[],
		country='RU',
		polit_coordinates=pol,
		location=geo,
		age=24,
		gender=Gender.MALE,
		personality=personality
		)
	user_info.save()
	age_pref = AgePref.objects.create(min_age=18, max_age=100, optimal_age=24)
	age_pref.save()
	user_pref = Preferences.objects.create(age=age_pref)
	user_pref.save()
	user = CustomUser.objects.create(name="John", user_info=user_info, user_prefs=user_pref)
	user.save()

	username = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
	email = username + '@gmail.com'
	real_user = User.objects.create_user(username=username, email=email, password='123')
	user.user = real_user
	user.save()
	#print(user)
	return user

class AcceptanceTestCase(TestCase):
	def setUp(self):
		self.first_user = create_empty_user()
		self.second_user = create_empty_user()

	def test_areas_matching(self):
		# restriction of the first user does not match with the second one
		self.second_user.user_info.location.lat = 10
		self.second_user.user_info.location.lon = 10
		self.second_user.user_info.location.save()
		self.second_user.user_info.save()
		self.second_user.save()

		self.first_user.user_prefs.area_restrict = True
		self.first_user.user_prefs.loc_area = 500
		self.first_user.user_prefs.save()
		self.first_user.save()
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Distance is too big for at least one of the parties")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Distance is too big for at least one of the parties")
		# restriction of the second user does not match with the first one
		self.first_user.user_info.location.lat = 10
		self.first_user.user_info.location.lon = 10
		self.first_user.user_info.location.save()
		self.first_user.user_info.save()
		self.first_user.user_prefs.area_restrict = False
		self.first_user.user_prefs.save()
		self.first_user.save()

		self.second_user.user_prefs.area_restrict = True
		self.second_user.user_prefs.loc_area = 500
		self.second_user.user_prefs.save()
		self.second_user.user_info.location.lat = 0
		self.second_user.user_info.location.lon = 0
		self.second_user.user_info.location.save()
		self.second_user.user_info.save()
		self.second_user.save()
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Distance is too big for at least one of the parties")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Distance is too big for at least one of the parties")
		# both do not match
		self.second_user.user_prefs.area_restrict = True
		self.second_user.user_prefs.loc_area = 500
		self.second_user.user_prefs.save()
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Distance is too big for at least one of the parties")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Distance is too big for at least one of the parties")
		# both match
		self.first_user.user_info.location.lat = 0
		self.first_user.user_info.location.lon = 0
		self.first_user.user_info.location.save()
		self.first_user.user_info.save()
		self.first_user.save()
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

	def test_goals_matching(self):
		# goals do not match
		self.first_user.user_prefs.goals = ChatGoal.ROMANTIC
		self.second_user.user_prefs.goals = ChatGoal.FRIENDSHIP
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Goals don't match")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Goals don't match")
		# matches
		self.first_user.user_prefs.goals = ChatGoal.ANYTHING
		self.second_user.user_prefs.goals = ChatGoal.FRIENDSHIP
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

		self.first_user.user_prefs.goals = ChatGoal.ROMANTIC
		self.second_user.user_prefs.goals = ChatGoal.ANYTHING
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

		self.first_user.user_prefs.goals = ChatGoal.ROMANTIC
		self.second_user.user_prefs.goals = ChatGoal.ROMANTIC
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

	def test_ages_matching(self):
		# age pref of the first user does not match the second ones age
		self.first_user.user_prefs.age = AgePref(min_age=18, max_age=25)
		self.second_user.user_info.age = 26
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Age prefs don't match")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Age prefs don't match")
		# age pref of the second user does not match the first ones age
		self.second_user.user_prefs.age = AgePref(min_age=18, max_age=25)
		self.second_user.user_info.age = 24
		self.first_user.user_info.age = 26
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Age prefs don't match")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Age prefs don't match")
		# ages match
		self.first_user.user_info.age=24
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

	def test_genders_matching(self):
		# gender pref of the first user does not match with the second one
		self.first_user.user_prefs.gender = Gender.FEMALE
		self.second_user.user_info.gender = Gender.MALE
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Gender 2 prefs don't match")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Gender 1 prefs don't match")
		# gender pref of the second user does not match with the first one
		self.first_user.user_info.gender = Gender.MALE
		self.first_user.user_prefs.gender = Gender.ANYTHING
		self.second_user.user_info.gender = Gender.FEMALE
		self.second_user.user_prefs.gender = Gender.FEMALE
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), False)
		self.assertEqual(u1ca.error, "Gender 1 prefs don't match")
		self.assertEqual(u2ca.users_match(), False)
		self.assertEqual(u2ca.error, "Gender 2 prefs don't match")
		# match
		self.first_user.user_prefs.gender = Gender.FEMALE
		self.first_user.user_info.gender = Gender.MALE
		self.second_user.user_info.gender = Gender.FEMALE
		self.second_user.user_prefs.gender = Gender.MALE
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)

		self.first_user.user_prefs.gender = Gender.ANYTHING
		self.first_user.user_info.gender = Gender.MALE
		self.second_user.user_info.gender = Gender.MALE
		self.second_user.user_prefs.gender = Gender.MALE
		u1ca = AcceptanceCalculator(main_user=self.first_user, target_user=self.second_user)
		u2ca = AcceptanceCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertEqual(u1ca.users_match(), True)
		self.assertEqual(u2ca.users_match(), True)


class LikemindnessTestCase(TestCase):
	def setUp(self):
		# first user will be rich profile user
		self.first_user = create_empty_user()
		self.first_user.user_info.interests = ['music', 'reading', 'hiking', 'art', 'philosophy']
		self.first_user.user_info.location = GeoCoordinates.objects.create(lat=55.751244, lon=37.618423)
		self.first_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=0.2, cult=0)
		self.first_user.user_info.personality=Personality.objects.create(extraversion=0.4, agreeableness=0.4, openness=0.8, conscientiousness=0.7, neuroticism=0.8)
		self.first_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.first_user.user_prefs.polit = True
		self.first_user.user_prefs.interests = True
		self.first_user.user_prefs.location = True
		self.first_user.user_prefs.personality = True
		self.first_user.user_prefs.goals = ChatGoal.ROMANTIC
		self.first_user.user_prefs.gender = Gender.FEMALE

		# we will modify info and prefs of second user below
		self.second_user = create_empty_user()
		self.second_user.user_prefs.goals = ChatGoal.ROMANTIC
		self.second_user.user_prefs.gender = Gender.MALE

	def test_only_age(self):
		self.second_user.user_info.location = None
		self.second_user.user_info.polit_coordinates=None
		self.second_user.user_info.personality=None
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.second_user.user_prefs.save()
		self.second_user.save()
		# print("oa")
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.50 and u1cl.calc_likeness() < 0.53)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		# print(u2cl.calc_likeness())
		self.assertTrue(u2cl.calc_likeness() > 0.97 and u2cl.calc_likeness() < 1)

	def test_age_and_location(self):
		self.second_user.user_info.polit_coordinates=None
		self.second_user.user_info.personality=None
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=55.093752, lon=38.768862)
		self.second_user.user_prefs.location = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("Start")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.57 and u1cl.calc_likeness() < 0.61)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.9 and u2cl.calc_likeness() < 0.94)
		# print(u2cl.calc_likeness())
		# print("Finish")

	def test_good_pers_long_dist(self):
		self.second_user.user_info.interests = ['music', 'reading', 'sport', 'guns', 'philosophy']
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=52.993004, lon=78.638656)
		self.second_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=0, cult=0)
		self.second_user.user_info.personality=Personality.objects.create(extraversion=0.4, agreeableness=0.6, openness=0.7, conscientiousness=0.9, neuroticism=0.7)
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.second_user.user_prefs.polit = True
		self.second_user.user_prefs.interests = True
		self.second_user.user_prefs.location = True
		self.second_user.user_prefs.personality = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("gpld")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.65 and u1cl.calc_likeness() < 0.68)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.65 and u2cl.calc_likeness() < 0.68)
		# print(u2cl.calc_likeness())
		# print("Finish")

	def test_bad_pers_close_dist(self):
		self.second_user.user_info.interests = ['boxing', 'reading', 'sport', 'guns', 'psychology']
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=55.751244, lon=37.618423)
		self.second_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=-0.6, cult=0.8)
		self.second_user.user_info.personality=Personality.objects.create(extraversion=0.8, agreeableness=0.3, openness=0.3, conscientiousness=0.3, neuroticism=0.1)
		self.second_user.user_info.age = 27
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.second_user.user_prefs.polit = True
		self.second_user.user_prefs.interests = True
		self.second_user.user_prefs.location = True
		self.second_user.user_prefs.personality = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("bpcd")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.62 and u1cl.calc_likeness() < 0.65)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.63 and u2cl.calc_likeness() < 0.66)
		# print(u2cl.calc_likeness())
		# print("Finish")

	def test_good_pers_bad_age(self):
		self.second_user.user_info.interests = ['music', 'reading', 'sport', 'guns', 'philosophy']
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=55.751244, lon=37.618423)
		self.second_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=0, cult=0)
		self.second_user.user_info.personality=Personality.objects.create(extraversion=0.4, agreeableness=0.6, openness=0.7, conscientiousness=0.9, neuroticism=0.7)
		self.second_user.user_info.age = 28
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.second_user.user_prefs.polit = True
		self.second_user.user_prefs.interests = True
		self.second_user.user_prefs.location = True
		self.second_user.user_prefs.personality = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("Start")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.83 and u1cl.calc_likeness() < 0.86)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.85 and u2cl.calc_likeness() < 0.88)
		# print(u2cl.calc_likeness())
		# print("Finish")

	def test_good_everything(self):
		self.second_user.user_info.interests = ['music', 'reading', 'hiking', 'guns', 'philosophy']
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=55.7981904, lon=37.9679)
		self.second_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=0, cult=0)
		self.second_user.user_info.personality=Personality.objects.create(extraversion=0.4, agreeableness=0.5, openness=0.8, conscientiousness=0.8, neuroticism=0.8)
		self.second_user.user_info.age = 24
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=28, optimal_age=25)
		self.second_user.user_prefs.polit = True
		self.second_user.user_prefs.interests = True
		self.second_user.user_prefs.location = True
		self.second_user.user_prefs.personality = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("Start")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.91 and u1cl.calc_likeness() < 0.94)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.91 and u2cl.calc_likeness() < 0.94)
		# print(u2cl.calc_likeness())
		# print("Finish")

	def test_bad_everything(self):
		self.second_user.user_info.interests = ['boxing', 'reading', 'sport', 'guns', 'psychology']
		self.second_user.user_info.location = GeoCoordinates.objects.create(lat=52.993004, lon=78.638656)
		self.second_user.user_info.polit_coordinates=PolitCoordinates.objects.create(eco=-0.8, cult=0.8)
		self.second_user.user_info.personality=Personality.objects.create(extraversion=0.8, agreeableness=0.3, openness=0.3, conscientiousness=0.3, neuroticism=0.1)
		self.second_user.user_info.age = 28
		self.second_user.user_prefs.age = AgePref.objects.create(min_age=23, max_age=32, optimal_age=32)
		self.second_user.user_prefs.polit = True
		self.second_user.user_prefs.interests = True
		self.second_user.user_prefs.location = True
		self.second_user.user_prefs.personality = True
		u1cl = LikenessCalculator(main_user=self.first_user, target_user=self.second_user)
		# print("Start")
		# print(u1cl.calc_likeness())
		self.assertTrue(u1cl.calc_likeness() > 0.39 and u1cl.calc_likeness() < 0.42)
		u2cl = LikenessCalculator(main_user=self.second_user, target_user=self.first_user)
		self.assertTrue(u2cl.calc_likeness() > 0.36 and u2cl.calc_likeness() < 0.39)
		# print(u2cl.calc_likeness())
		# print("Finish")

class UserApiTestCase(TestCase):
	maxDiff = None
	def test_empty_chat_user(self):
		c = Client()
		json_data = json.dumps({"registration": True, "user": {"username": 'test_user', "email": "test@gmail.com", "password": "123"}})
		response = c.post("/chat/api/users/", json_data, content_type="application/json")

		user_id = response.json()['id']
		self.assertEqual(response.status_code, 201)

		response = c.get("/chat/api/users/" + str(user_id) + "/")
		self.assertEqual(response.status_code, 200)
		expected_data = json.dumps({'id': user_id,
			'registration': False,
			'name': 'anon',
			'user': {
				'id': response.json()['user']['id'],
				'username': 'test_user',
				'email': 'test@gmail.com',
				'password': response.json()['user']['password']
				},
			'user_info': {
				'description': '',
				'country': None,
				'languages': None,
				'interests': None,
				'polit_coordinates': None,
				'age': None,
				'location': None,
				'gender': 'M',
				'personality': None
				}, 
			'user_prefs': {
				'age': {'min_age': 18, 'max_age': 100, 'optimal_age': 25},
				'polit': False,
				'interests': False,
				'location': False,
				'personality': False,
				'area_restrict': False,
				'loc_area': 10,
				'goals': 'AN',
				'gender': 'A'
				}
			})
		self.assertJSONEqual(json.dumps(response.json()), expected_data)

		patch_data = json.dumps({
			'name': 'anon',
			'user_info': {
				'description': 'Hello',
				'country': None,
				'languages': None,
				'interests': ['.net', '3d-modeling', '3d-printing'],
				"polit_coordinates": {
	                "eco": 0.5,
	                "cult": 0.5
	            },
	            "age": 24,
	            "location": {
	                "lat": 33.3597,
	                "lon": 33.758
	            },
	            "gender": "M",
	            "personality": {
	                "extraversion": 0.9,
	                "agreeableness": 0.9,
	                "openness": 0.9,
	                "conscientiousness": 0.9,
	                "neuroticism": 0.9
	            }
			}, 
			'user_prefs': {
				'age': {'min_age': 18, 'max_age': 27, 'optimal_age': 25},
				'polit': True,
				'interests': True,
				'location': True,
				'personality': True,
				'area_restrict': True,
				'loc_area': 10,
				'goals': 'AN',
				'gender': 'A'
				}
			})
		response = c.put("/chat/api/users/" + str(user_id) + "/", patch_data, content_type="application/json")
		self.assertEqual(response.status_code, 200)
		expected_data = json.dumps({'id': user_id,
			'registration': False,
			'name': 'anon',
			'user': {
				'id': response.json()['user']['id'],
				'username': 'test_user',
				'email': 'test@gmail.com',
				'password': response.json()['user']['password']
				},
			'user_info': {
				'description': 'Hello',
				'country': None,
				'languages': None,
				'interests': ['.net', '3d-modeling', '3d-printing'],
				"polit_coordinates": {
	                "eco": 0.5,
	                "cult": 0.5
	            },
	            "age": 24,
	            "location": {
	                "lat": 33.3597,
	                "lon": 33.758
	            },
	            "gender": "M",
	            "personality": {
	                "extraversion": 0.9,
	                "agreeableness": 0.9,
	                "openness": 0.9,
	                "conscientiousness": 0.9,
	                "neuroticism": 0.9
	            }
			}, 
			'user_prefs': {
				'age': {'min_age': 18, 'max_age': 27, 'optimal_age': 25},
				'polit': True,
				'interests': True,
				'location': True,
				'personality': True,
				'area_restrict': True,
				'loc_area': 10,
				'goals': 'AN',
				'gender': 'A'
				}
			})
		response = c.get("/chat/api/users/" + str(user_id) + "/")
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(json.dumps(response.json()), expected_data)

	def test_post_online_user(self):
		c = Client()
		json_data = json.dumps({
			'registration': False,
			'name': 'test user',
			'user_info': {
				'description': 'Hello',
				'country': None,
				'languages': None,
				'interests': ['.net', '3d-modeling', '3d-printing'],
				"polit_coordinates": {
	                "eco": 0,
	                "cult": 0
	            },
	            "age": 24,
	            "location": {
	                "lat": 0,
	                "lon": 0
	            },
	            "gender": "F",
	            "personality": {
	                "extraversion": 0.5,
	                "agreeableness": 0.5,
	                "openness": 0.5,
	                "conscientiousness": 0.5,
	                "neuroticism": 0.5
	            }
			}, 
			'user_prefs': {
				'age': {'min_age': 24, 'max_age': 28, 'optimal_age': 25},
				'polit': True,
				'interests': True,
				'location': True,
				'personality': True,
				'area_restrict': True,
				'loc_area': 10,
				'goals': 'FR',
				'gender': 'F'
				}
			})
		response = c.post("/chat/api/users/", json_data, content_type="application/json")
		self.assertEqual(response.status_code, 201)
		user_id = response.json()['id']
		profile = CustomUser.objects.get(pk=user_id)
		self.assertEqual(profile.user_info.age, 24)
		self.assertEqual(profile.user_info.description, "Hello")
		self.assertEqual(profile.user_info.gender, Gender.FEMALE)
		self.assertEqual(profile.user_info.interests, ['.net', '3d-modeling', '3d-printing'])
		self.assertEqual(profile.user_info.location.lon, 0)
		self.assertEqual(profile.user_info.polit_coordinates.eco, 0)
		self.assertEqual(profile.user_info.polit_coordinates.cult, 0)
		self.assertEqual(profile.user_info.personality.extraversion, 0.5)
		self.assertEqual(profile.user_info.personality.agreeableness, 0.5)
		self.assertEqual(profile.user_info.personality.openness, 0.5)
		self.assertEqual(profile.user_info.personality.conscientiousness, 0.5)
		self.assertEqual(profile.user_info.personality.neuroticism, 0.5)
		self.assertTrue(profile.user_prefs.polit)
		self.assertTrue(profile.user_prefs.interests)
		self.assertTrue(profile.user_prefs.location)
		self.assertTrue(profile.user_prefs.personality)
		self.assertTrue(profile.user_prefs.area_restrict)
		self.assertEqual(profile.user_prefs.loc_area, 10)
		self.assertEqual(profile.user_prefs.goals, ChatGoal.FRIENDSHIP)
		self.assertEqual(profile.user_prefs.gender, Gender.FEMALE)
		self.assertEqual(profile.user_prefs.age.min_age, 24)
		self.assertEqual(profile.user_prefs.age.max_age, 28)
		self.assertEqual(profile.user_prefs.age.optimal_age, 25)

class UserRegistrationTestCase(TestCase):
	def test_user_registration(self):
		c = Client()
		json_data = json.dumps({"registration": True, "user": {"username": 'test_user', "email": "test@gmail.com", "password": "123"}})
		response = c.post("/chat/api/users/", json_data, content_type="application/json")
		self.assertEqual(response.status_code, 201)

		json_data = json.dumps({"registration": True, "user": {"username": 'test_user', "email": "test@gmail.com", "password": "123"}})
		response = c.post("/chat/api/users/", json_data, content_type="application/json")
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['user']['non_field_errors'][0], 'A user with this name already exists.')
		
		json_data = json.dumps({"registration": True, "user": {"username": 'test_user1', "email": "test@gmail.com", "password": "123"}})
		response = c.post("/chat/api/users/", json_data, content_type="application/json")
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['user']['non_field_errors'][0], 'A user with this email already exists.')


'''
class ChattingTest(TestCase):
	async def test_room_search(self):
		user = await sync_to_async(create_empty_user)()
		user_id = user.id
		# application = URLRouter([
		# 	re_path(r'ws/chat_search/(?P<room_name>\w+)/$', ChatSearchConsumer.as_asgi()),
		# ])
		# communicator = WebsocketCommunicator(application, f'/ws/chat_search/'+str(user_id)+"/")
		application = URLRouter([
			re_path(r'ws/chat_search/(?P<room_name>\w+)/$', ChatSearchConsumer.as_asgi()),
		])
		# communicator = WebsocketCommunicator(application, f'/ws/chat_search/1/')
		print(user_id)
		communicator = WebsocketCommunicator(application, f'/ws/chat_search/'+str(user_id)+"/")
		connected, subprotocol = await communicator.connect()
		assert connected
		await communicator.send_to(json.dumps({
              "type": "message",
              "message": "Start searching",
              "name": "name"
            }))
		# response = await communicator.receive_from()
		# assert response == "hello"
		# # Close
		await communicator.disconnect()
'''