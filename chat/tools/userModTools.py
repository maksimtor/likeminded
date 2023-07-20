from django.http import JsonResponse
from django.contrib.auth.models import User
from chat.models import CustomUser, Gender, ChatGoal, AgePref, Personality, PolitCoordinates, GeoCoordinates, UserInfo, Preferences

def convert_user_to_json(user):
	custom_user = user.profile
	print(custom_user)
	photo = 'None'
	if (custom_user.user_info.photo):
		photo = custom_user.user_info.photo.url
	user_data = {
		'name': user.username,
		'age': custom_user.user_info.age,
		'gender': custom_user.user_info.gender,
		'interests': custom_user.user_info.interests,
		'locToggle': custom_user.user_info.location != None,
		'geoLat': None if custom_user.user_info.location == None else custom_user.user_info.location.lat,
		'geoLon': None if custom_user.user_info.location == None else custom_user.user_info.location.lon,
		'polToggle': custom_user.user_info.polit_coordinates != None,
		'polEco': None if custom_user.user_info.polit_coordinates == None else custom_user.user_info.polit_coordinates.eco*10,
		'polGov': None if custom_user.user_info.polit_coordinates == None else custom_user.user_info.polit_coordinates.cult*10,
		'persToggle': custom_user.user_info.personality != None,
		'personalityExtraversion': None if custom_user.user_info.personality == None else custom_user.user_info.personality.extraversion*10,
		'personalityAgreeableness': None if custom_user.user_info.personality == None else custom_user.user_info.personality.agreeableness*10,
		'personalityOpenness': None if custom_user.user_info.personality == None else custom_user.user_info.personality.openness*10,
		'personalityConscientiousness': None if custom_user.user_info.personality == None else custom_user.user_info.personality.conscientiousness*10,
		'personalityNeuroticism': None if custom_user.user_info.personality == None else custom_user.user_info.personality.neuroticism*10,
		'politPref': custom_user.user_prefs.polit,
		'intPref': custom_user.user_prefs.interests,
		'locPref': custom_user.user_prefs.location,
		'areaPref': custom_user.user_prefs.loc_area,
		'areaRestrictToggle': custom_user.user_prefs.area_restrict,
		'persPref': custom_user.user_prefs.personality,
		'goals': custom_user.user_prefs.goals,
		'genderPref': custom_user.user_prefs.gender,
		'ageRange': [custom_user.user_prefs.age.min_age, custom_user.user_prefs.age.max_age],
		'ageOptimal': custom_user.user_prefs.age.optimal_age,
		'description': custom_user.user_info.description,
		'photo': photo,
	}
	print(user_data)
	return JsonResponse(user_data)

def create_empty_user(data):
	username = data['username']
	email = data['email']
	password = data['password']
	hu = User.objects.create_user(username=username, email=email, password=password)
	hu.save()
	info = UserInfo.objects.create()
	info.save()
	ap = AgePref.objects.create(min_age=18, max_age=100, optimal_age=25)
	ap.save()
	prefs = Preferences.objects.create(age=ap)
	prefs.save()
	u = CustomUser.objects.create(user=hu, user_info=info, user_prefs=prefs)
	u.save()
	return u

def create_user_with_profile(data):
	print (data)
	userGender = data['gender']['value']
	if (userGender == 'M'):
		userGender = Gender.MALE
	elif (userGender == 'F'):
		userGender = Gender.FEMALE
	else:
		userGender = Gender.ANYTHING
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
	age_pref = AgePref.objects.create(min_age=data['ageRange'][0], max_age=data['ageRange'][1], optimal_age=data['ageOptimal'])
	age_pref.save()
	personality = None
	if data['persToggle']:
		personality = Personality.objects.create(
			extraversion=data['personalityExtraversion']/10,
			agreeableness=data['personalityAgreeableness']/10,
			openness=data['personalityOpenness']/10,
			conscientiousness=data['personalityConscientiousness']/10,
			neuroticism=data['personalityNeuroticism']/10
		)
		personality.save()
	pol = None
	if data['polToggle']:
		pol = PolitCoordinates.objects.create(eco=data['polEco']/10, cult=data['polGov']/10)
		pol.save()
	geo = None
	if (data['locToggle']):
		print('save geo')
		geo = GeoCoordinates.objects.create(lat=data['geoLat'], lon=data['geoLon'])
		geo.save()
	user_info = UserInfo.objects.create(
		description=data['description'],
		interests=[i['value'] for i in data['interests']] if 'interests' in data.keys() else [],
		polit_coordinates=pol,
		location=geo,
		age=data['age'] if isinstance(data['age'], int) else None,
		gender=userGender,
		personality=personality
		)
	user_info.save()
	user_pref = Preferences.objects.create(
		goals=userGoals,
		age=age_pref,
		polit=data['politPref'],
		interests=data['intPref'],
		location=data['locPref'],
		gender=userGenderPref,
		personality=data['persPref'],
		area_restrict=data['areaRestrictToggle'],
		loc_area=data['areaPref'],
		)
	user_pref.save()
	custom_user = CustomUser.objects.create(name=data['name'], user_info=user_info, user_prefs=user_pref)
	custom_user.save()
	return custom_user

def update_user(data):
	print(data)
	userGender = data['gender']['value']
	if (userGender == 'M'):
		userGender = Gender.MALE
	elif (userGender == 'F'):
		userGender = Gender.FEMALE
	else:
		userGender = Gender.ANYTHING
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
	user = User.objects.get(id=data['user_id'])
	user.username = data['name']
	profile = user.profile
	info = profile.user_info
	info.interests=[i['value'] for i in data['interests']] if 'interests' in data.keys() else []
	info.description=data['description']
	pol = info.polit_coordinates
	if pol:
		if data['polToggle']:
			pol.eco=data['polEco']/10
			pol.cult=data['polGov']/10
			pol.save()
		else:
			pol.delete()
			pol = None
	else:
		if data['polToggle']:
			pol = PolitCoordinates.objects.create(eco=data['polEco']/10, cult=data['polGov']/10)
			pol.save()
	info.polit_coordinates=pol
	geo = info.location
	if geo:
		if data['locToggle']:
			geo.lat=data['geoLat']
			geo.lon=data['geoLon']
			geo.save()
		else:
			geo.delete()
	else:
		if data['locToggle']:
			geo = GeoCoordinates.objects.create(lat = data['geoLat'], lon = data['geoLon'])
			geo.save()		
	info.location=geo
	info.age=data['age']
	info.gender=userGender
	personality=info.personality
	if personality:
		if data['persToggle']:
			personality.extraversion=data['personalityExtraversion']/10
			personality.agreeableness=data['personalityAgreeableness']/10
			personality.openness=data['personalityOpenness']/10
			personality.conscientiousness=data['personalityConscientiousness']/10
			personality.neuroticism=data['personalityNeuroticism']/10
			print(personality.extraversion)
			personality.save()
		else:
			personality.delete()
	else:
		if data['persToggle']:
			personality = Personality.objects.create(
				extraversion=data['personalityExtraversion']/10,
				agreeableness=data['personalityAgreeableness']/10,
				openness=data['personalityOpenness']/10,
				conscientiousness=data['personalityConscientiousness']/10,
				neuroticism=data['personalityNeuroticism']/10
			)
			personality.save()
	info.personality=personality
	info.save()

	prefs = profile.user_prefs
	prefs.goals=userGoals
	prefs.polit=data['politPref']
	prefs.interests=data['intPref']
	prefs.location=data['locPref']
	prefs.gender=userGenderPref
	prefs.personality=data['persPref']
	prefs.area_restrict=data['areaRestrictToggle']
	prefs.loc_area=data['areaPref']
	age_pref = prefs.age
	age_pref.min_age=data['ageRange'][0]
	age_pref.max_age=data['ageRange'][1]
	age_pref.optimal_age=data['ageOptimal']
	age_pref.save()
	prefs.age_pref = age_pref
	prefs.save()
	profile.user_info = info
	profile.user_prefs = prefs
	profile.save()
	user.save()