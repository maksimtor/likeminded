from chat.models import User, UserInfo, Gender, ChatGoal
from math import sin, cos, sqrt, atan2, radians
import pycountry_convert as pc

def flatten(t):
    return [item for sublist in t for item in sublist]

class AcceptanceCalculator:
	def __init__(self, main_user, target_user):
		self.main_prefs = main_user.user_prefs
		self.main_info = main_user.user_info
		self.target_prefs = target_user.user_prefs
		self.target_info = target_user.user_info
		self.accepted = True
		self.error = ""

	def users_match(self):
		return True if (self.areas_match() and self.goals_match() and self.ages_match() and self.genders_match()) else False

	def areas_match(self):
		main_location = self.main_info.location
		target_location = self.target_info.location
		if self.main_prefs.area_restrict or self.target_prefs.area_restrict:
			if main_location and target_location:
				R = 6373.0

				lat1 = radians(main_location.lat)
				lon1 = radians(main_location.lon)
				lat2 = radians(target_location.lat)
				lon2 = radians(target_location.lon)

				dlon = lon2 - lon1
				dlat = lat2 - lat1

				a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
				c = 2 * atan2(sqrt(a), sqrt(1 - a))

				distance = R * c
				if distance > self.main_prefs.loc_area or distance > self.target_prefs.loc_area:
					self.error = 'Distance is too big for at least one of the parties'
					return False
				else:
					return True
			else:
				self.error = 'Locations are not available, though needed for restriction check'
				return False
		else:
			return True

	def goals_match(self):
		if (self.main_prefs.goals == ChatGoal.ANYTHING) or (self.target_prefs.goals == ChatGoal.ANYTHING):
			return True
		elif (self.main_prefs.goals == self.target_prefs.goals):
			return True
		else:
			self.error = 'Goals don\'t match'
			return False

	def ages_match(self):
		target_age_prefs = self.target_prefs.age
		main_age_prefs = self.main_prefs.age
		target_age = self.target_info.age
		main_age = self.main_info.age
		if target_age_prefs and main_age:
			if (int(main_age) < int(target_age_prefs.min_age) or int(main_age) > int(target_age_prefs.max_age)):
				self.error = 'Age prefs don\'t match'
				return False
		if main_age_prefs and target_age:
			if (int(target_age) < int(main_age_prefs.min_age) or int(target_age) > int(main_age_prefs.max_age)):
				self.error = 'Age prefs don\'t match'
				return False
		return True

	def genders_match(self):
		if (self.target_prefs.gender != Gender.ANYTHING):
			if self.target_prefs.gender != self.main_info.gender:
				self.error = 'Gender 1 prefs don\'t match'
				return False

		if (self.main_prefs.gender != Gender.ANYTHING):
			if self.main_prefs.gender != self.target_info.gender:
				self.error = 'Gender 2 prefs don\'t match'
				return False
		return True


class LikenessCalculator:
	def __init__(self, main_user, target_user):
		self.main_info = main_user.user_info
		self.prefs = main_user.user_prefs
		self.target_data = target_user.user_info
		self.score = 0
		self.uni_weight = self.calc_uni_weight()

	def calc_uni_weight(self):
		uni_weight = 0
		if self.prefs.polit == True:
			uni_weight += 1

		if self.prefs.location == True:
			uni_weight += 1

		if self.prefs.interests == True:
			uni_weight += 1

		if self.prefs.age:
			uni_weight += 1

		if self.prefs.personality == True:
			uni_weight += 1

		return (10/uni_weight)/10

	def calc_polit_likeness(self):
		if self.prefs.polit == True:
			if self.target_data.polit_coordinates == None:
				return 0.4
			else:
				dist = sqrt( (self.target_data.polit_coordinates.eco - self.main_info.polit_coordinates.eco)**2 + (self.target_data.polit_coordinates.cult - self.main_info.polit_coordinates.cult)**2 )
				return 1-dist/2.8284271247461903
		else:
			return 0

	def calc_location_likeness(self):
		if self.prefs.location == True:
			if self.target_data.location == None:
				return 0.4
			else:
				# approximate radius of earth in km
				R = 6373.0

				lat1 = radians(self.main_info.location.lat)
				lon1 = radians(self.main_info.location.lon)
				lat2 = radians(self.target_data.location.lat)
				lon2 = radians(self.target_data.location.lon)

				dlon = lon2 - lon1
				dlat = lat2 - lat1

				a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
				c = 2 * atan2(sqrt(a), sqrt(1 - a))

				distance = R * c

				res = 1 - distance/20000
				return (res ** 6)
		else:
			return 0

	def calc_intererests_likeness(self):
		if self.prefs.interests == True:
			if self.target_data.interests == None:
				return 0.4
			else:
				l = len(self.main_info.interests)
				a = flatten(self.main_info.interests)
				b = flatten(self.target_data.interests)
				common_elements = list(set(self.main_info.interests).intersection(self.target_data.interests))
				return len(common_elements)/l
		else:
			return 0

	def calc_age_likeness(self):
		if self.prefs.age:
			if self.target_data.age == None:
				return 0.4
			else:
				optimal_age = int(self.prefs.age.optimal_age)
				min_age = int(self.prefs.age.min_age)
				max_age = int(self.prefs.age.max_age)

				targetAge = int(self.target_data.age)

				max_dist = max(optimal_age-min_age, max_age-optimal_age)
				act_dist = abs(targetAge-optimal_age)
				return 1-(act_dist/max_dist)
		else:
			return 0

	def calc_personality_likeness(self):
		if self.prefs.personality:
			if self.target_data.personality == None:
				return 0.4
			else:
				result = 0
				# scoring extraversion
				main_points = self.main_info.personality.extraversion
				target_points = self.target_data.personality.extraversion
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring agreeableness
				main_points = self.main_info.personality.agreeableness
				target_points = self.target_data.personality.agreeableness
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring openness
				main_points = self.main_info.personality.openness
				target_points = self.target_data.personality.openness
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring conscientiousness
				main_points = self.main_info.personality.conscientiousness
				target_points = self.target_data.personality.conscientiousness
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring neuroticism
				main_points = self.main_info.personality.neuroticism
				target_points = self.target_data.personality.neuroticism
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2
				return result
		else:
			return 0

	def calc_likeness(self):
		return self.uni_weight*(self.calc_polit_likeness() + self.calc_location_likeness() + self.calc_intererests_likeness() + self.calc_age_likeness() + self.calc_personality_likeness())


def calcAcceptance(mainUser, targetUser):
	# filtering part

	# collecting main info and strict prefs
	mainGoals = mainUser.user_prefs.goals
	mainLanguages = mainUser.user_info.languages
	mainCountry = mainUser.user_info.country
	mainAge = mainUser.user_info.age
	mainGender = mainUser.user_info.gender
	mainAgePrefs = mainUser.user_prefs.age
	mainGenderPrefs = mainUser.user_prefs.gender
	mainAreaPrefs = mainUser.user_prefs.loc_area
	mainAreaRestrictionOn = mainUser.user_prefs.area_restrict
	mainAreaRestrictionValue = mainUser.user_prefs.loc_area
	mainLocation = mainUser.user_info.location

	# collecting target user info and strict prefs
	targetGoals = targetUser.user_prefs.goals
	targetLanguages = targetUser.user_info.languages
	targetCountry = targetUser.user_info.country
	targetAge = targetUser.user_info.age
	targetGender = targetUser.user_info.gender
	targetAgePrefs = targetUser.user_prefs.age
	targetGenderPrefs = targetUser.user_prefs.gender
	targetAreaPrefs = targetUser.user_prefs.loc_area
	targetAreaRestrictionOn = targetUser.user_prefs.area_restrict
	targetAreaRestrictionValue = targetUser.user_prefs.loc_area
	targetLocation = targetUser.user_info.location

	# area checking

	if mainAreaRestrictionOn or targetAreaRestrictionOn:
		if mainLocation and targetLocation:
			R = 6373.0

			lat1 = radians(mainLocation.lat)
			lon1 = radians(mainLocation.lon)
			lat2 = radians(targetLocation.lat)
			lon2 = radians(targetLocation.lon)

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = R * c
			if distance > mainAreaRestrictionValue or distance > targetAreaRestrictionValue:
				return 'Distance is too big for at least one of the parties'
			else:
				pass
		else:
			return 'Locations are not available, though needed for restriction check'

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
	mainInfo = mainUser.user_info

	prefs = mainUser.user_prefs

	targetData = targetUser.user_info

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
