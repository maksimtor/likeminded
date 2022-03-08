from chat.models import User, UserInfo, ChatGoal, Gender
from math import sin, cos, sqrt, atan2, radians
import pycountry_convert as pc

def flatten(t):
    return [item for sublist in t for item in sublist]

def calcAcceptance(mainUser, targetUser):
	# filtering part

	# collecting main info and strict prefs
	mainGoals = mainUser.userPrefs.goals
	mainLanguages = mainUser.userInfo.languages
	mainCountry = mainUser.userInfo.country
	mainAge = mainUser.userInfo.age
	mainGender = mainUser.userInfo.gender
	mainAgePrefs = mainUser.userPrefs.age
	mainGenderPrefs = mainUser.userPrefs.gender
	mainAreaPrefs = mainUser.userPrefs.loc_area

	# collecting target user info and strict prefs
	targetGoals = targetUser.userPrefs.goals
	targetLanguages = targetUser.userInfo.languages
	targetCountry = targetUser.userInfo.country
	targetAge = targetUser.userInfo.age
	targetGender = targetUser.userInfo.gender
	targetAgePrefs = targetUser.userPrefs.age
	targetGenderPrefs = targetUser.userPrefs.gender
	targetAreaPrefs = targetUser.userPrefs.loc_area
	# goal checking
	if (mainGoals == ChatGoal.ANYTHING) or (targetGoals == ChatGoal.ANYTHING):
		pass
	elif (mainGoals == targetGoals):
		pass
	else:
		return 'Goals don\'t match'

	# lang checking
	# a = flatten(mainLanguages)
	# b = flatten(targetLanguages)
	# common_elements = list(set(mainLanguages).intersection(targetLanguages))
	# if common_elements == []:
	# 	return 'No common languages'

	if targetAgePrefs and mainAge:
		if (int(mainAge) < int(targetAgePrefs.min_age) or int(mainAge) > int(targetAgePrefs.max_age)):
			return 'Age prefs don\'t match'
	if mainAgePrefs and targetAge:
		if (int(targetAge) < int(mainAgePrefs.min_age) or int(targetAge) > int(mainAgePrefs.max_age)):
			return 'Age prefs don\'t match'

	# gender checking

	if (targetGenderPrefs != Gender.ANYTHING):
		if targetGenderPrefs != mainGender:
			return 'Gender 1 prefs don\'t match'

	if (mainGenderPrefs != Gender.ANYTHING):
		if mainGenderPrefs != targetGender:
			return 'Gender 2 prefs don\'t match'

	# # loc area checking
	# match = True
	# if (mainAreaPrefs != [] and mainAreaPrefs != None):
	# 	match=False
	# 	for area in mainAreaPrefs:
	# 		if area == targetCountry or area == pc.country_alpha2_to_continent_code(targetCountry):
	# 			match = True
	# if (not match):
	# 	return 'Areas don\'t match'

	# match = True
	# if (targetAreaPrefs != [] and targetAreaPrefs != None):
	# 	match = False
	# 	for area in targetAreaPrefs:
	# 		if area == mainCountry or area == pc.country_alpha2_to_continent_code(mainCountry):
	# 			match = True
	# if (not match):
	# 	return 'Areas don\'t match'
	return 1

def calcLikeness(mainUser, targetUser):
	print('_________________________')
	mainInfo = mainUser.userInfo

	prefs = mainUser.userPrefs

	targetData = targetUser.userInfo

	score = 0

	# scoring pol

	uni_weight = 0
	if prefs.polit == True:
		uni_weight += 1

	if prefs.location == True:
		uni_weight += 1

	if prefs.interests == True:
		uni_weight += 1

	if prefs.age:
		uni_weight += 1

	if prefs.personality == True:
		uni_weight += 1

	uni_weight = (10/uni_weight)/10


	if prefs.polit == True:
		if targetData.polit_coordinates == None:
			score += uni_weight*0.4
		else:
			dist = sqrt( (targetData.polit_coordinates.eco - mainInfo.polit_coordinates.eco)**2 + (targetData.polit_coordinates.cult - mainInfo.polit_coordinates.cult)**2 )
			res = 1-dist/2.8284271247461903
			score += res*uni_weight
			# print('')
			# print('polit res' + str(res))
			# print('polit ' + str(score))

	# scoring loc
	if prefs.location == True:
		if targetData.location == None:
			score += uni_weight*0.4
		else:
			# approximate radius of earth in km
			R = 6373.0

			lat1 = radians(mainInfo.location.lat)
			lon1 = radians(mainInfo.location.lon)
			lat2 = radians(targetData.location.lat)
			lon2 = radians(targetData.location.lon)

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = R * c

			res = 1 - distance/20000
			score += (res ** 6)*uni_weight
			# print('')
			# print('loc res' + str(res ** 6))
			# print('loc ' + str(score))

	# scoring interests
	if prefs.interests == True:
		if targetData.interests == None:
			score += uni_weight*0.4
		else:
			l = len(mainInfo.interests)
			a = flatten(mainInfo.interests)
			b = flatten(targetData.interests)
			# common_elements = list(set(a).intersection(set(b)))
			common_elements = list(set(mainInfo.interests).intersection(targetData.interests))
			res = len(common_elements)/l
			score += res*uni_weight
			# print('')
			# print('int res' + str(res))
			# print('int ' + str(score))

	# scoring age

	if prefs.age:
		if targetData.age == None:
			score += uni_weight*0.4
		else:
			optimal_age = int(prefs.age.optimal_age)
			min_age = int(prefs.age.min_age)
			max_age = int(prefs.age.max_age)

			targetAge = int(targetData.age)

			max_dist = max(optimal_age-min_age, max_age-optimal_age)
			act_dist = abs(targetAge-optimal_age)
			res = 1-(act_dist/max_dist)
			score+= res*uni_weight
			# print('')
			# print('age res' + str(res))
			# print('age ' + str(score))
			# print('')

	# scoring personality

	if prefs.personality:
		if targetData.personality == None:
			score += uni_weight*0.4
		else:
			result = 0
			# scoring extraversion
			main_points = mainInfo.personality.extraversion
			target_points = targetData.personality.extraversion
			max_dist = max(1-main_points, main_points)
			act_dist = abs(target_points-main_points)
			r_score = 1-(act_dist/max_dist)
			result+=r_score*0.2

			# scoring agreeableness
			main_points = mainInfo.personality.agreeableness
			target_points = targetData.personality.agreeableness
			max_dist = max(1-main_points, main_points)
			act_dist = abs(target_points-main_points)
			r_score = 1-(act_dist/max_dist)
			result+=r_score*0.2

			# scoring openness
			main_points = mainInfo.personality.openness
			target_points = targetData.personality.openness
			max_dist = max(1-main_points, main_points)
			act_dist = abs(target_points-main_points)
			r_score = 1-(act_dist/max_dist)
			result+=r_score*0.2

			# scoring conscientiousness
			main_points = mainInfo.personality.conscientiousness
			target_points = targetData.personality.conscientiousness
			max_dist = max(1-main_points, main_points)
			act_dist = abs(target_points-main_points)
			r_score = 1-(act_dist/max_dist)
			result+=r_score*0.2

			# scoring neuroticism
			main_points = mainInfo.personality.neuroticism
			target_points = targetData.personality.neuroticism
			max_dist = max(1-main_points, main_points)
			act_dist = abs(target_points-main_points)
			r_score = 1-(act_dist/max_dist)
			result+=r_score*0.2
			score+= result*uni_weight
			# print('')
			# print('personality res' + str(result))
			# print('personality ' + str(score))

	print('fs ' + str(score))
	print('_________________________')

	return score
