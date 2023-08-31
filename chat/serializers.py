from rest_framework import serializers, validators
from .models import CustomUser, Chat, UserInfo, PolitCoordinates, GeoCoordinates, Personality, Preferences, AgePref
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        allow_null = True
        extra_kwargs= {'username': {'validators': []}, 'email': {'validators': []}}

    def validate(self, data):
        if self.context['request']._request.method == 'POST':
           if self.Meta.model.objects.filter(username=data['username']).exists():
               raise ValidationError('A user with this name already exists.')
           if self.Meta.model.objects.filter(email=data['email']).exists():
               raise ValidationError('A user with this email already exists.')
        return data

class PolitCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolitCoordinates
        fields = ['eco', 'cult']
    def update(self, instance, validated_data):
        if validated_data:
            return super().update(instance, validated_data)
        else:
            instance.delete()
            return None

class GeoCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoCoordinates
        fields = ['lat', 'lon']
    def update(self, instance, validated_data):
        if validated_data:
            return super().update(instance, validated_data)
        else:
            instance.delete()
            return None

class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = ['extraversion', 'agreeableness', 'openness', 'conscientiousness', 'neuroticism']
    def update(self, instance, validated_data):
        if validated_data:
            return super().update(instance, validated_data)
        else:
            instance.delete()
            return None

class UserInfoSerializer(serializers.ModelSerializer):
    polit_coordinates = PolitCoordinatesSerializer(allow_null=True)
    location = GeoCoordinatesSerializer(allow_null=True)
    personality = PersonalitySerializer(allow_null=True)
    class Meta:
        model = UserInfo
        fields = ['description', 'country', 'languages',
                    'interests', 'polit_coordinates',
                    'age', 'location', 'gender',
                    'personality']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        polit_coordinates_created = None
        if validated_data['polit_coordinates']:
            polit_coordinates=PolitCoordinatesSerializer()
            polit_coordinates_created = polit_coordinates.create(validated_data['polit_coordinates'])
        personality_created = None
        if validated_data['personality']:
            personality=PersonalitySerializer()
            personality_created = personality.create(validated_data['personality'])
        location_created = None
        if validated_data['location']:
            location=GeoCoordinatesSerializer()
            location_created = location.create(validated_data['location'])
        return UserInfo.objects.create(description=validated_data['description'],
            country=validated_data['country'],
            languages=validated_data.get('languages', None),
            interests=validated_data.get('interests', None),
            polit_coordinates=polit_coordinates_created,
            age=validated_data['age'],
            gender=validated_data['gender'],
            personality=personality_created,
            location=location_created)
    def update(self, instance, validated_data):
        if validated_data:
            instance.description = validated_data.get('description', None)
            instance.interests = validated_data.get('interests', [])
            instance.age = validated_data.get('age', None)
            instance.gender = validated_data.get('gender', None)
            # updating polit_coordinates
            if instance.polit_coordinates:
                polit_coordinates_serializer = PolitCoordinatesSerializer()
                res = polit_coordinates_serializer.update(
                    instance.polit_coordinates,
                    validated_data.get('polit_coordinates', None)
                    )
                if not res:
                    instance.polit_coordinates = None
            elif validated_data['polit_coordinates']:
                polit_coordinates_serializer=PolitCoordinatesSerializer()
                polit_coordinates = polit_coordinates_serializer.create(validated_data['polit_coordinates'])
                instance.polit_coordinates = polit_coordinates
            # updating location
            if instance.location:
                location_serializer = GeoCoordinatesSerializer()
                res = location_serializer.update(
                    instance.location,
                    validated_data.get('location', None)
                    )
                if not res:
                    instance.location = None
            elif validated_data['location']:
                location_serializer=GeoCoordinatesSerializer()
                location = location_serializer.create(validated_data['location'])
                instance.location = location
            # updating personality
            if instance.personality:
                personality_serializer = PersonalitySerializer()
                res = personality_serializer.update(
                    instance.personality,
                    validated_data.get('personality', None)
                    )
                if not res:
                    instance.personality = None
            elif validated_data['personality']:
                personality_serializer=PersonalitySerializer()
                personality = personality_serializer.create(validated_data['personality'])
                instance.personality = personality
            instance.save()
        else:
            instance.delete()
            return None


class AgePrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgePref
        fields = ['min_age', 'max_age', 'optimal_age']
    def update(self, instance, validated_data):
        if validated_data:
            return super().update(instance, validated_data)
        else:
            instance.delete()
            return None

class PreferencesSerializer(serializers.ModelSerializer):
    age = AgePrefSerializer(allow_null=True)
    class Meta:
        model = Preferences
        fields = ['age', 'polit', 'interests', 'location',
                    'personality', 'area_restrict',
                    'loc_area', 'goals', 'gender']

    def create(self, validated_data):
        age = AgePrefSerializer()
        age_created = age.create(validated_data['age'])
        return Preferences.objects.create(
            age = age_created,
            polit = validated_data['polit'],
            interests = validated_data['interests'],
            location = validated_data['location'],
            personality = validated_data['personality'],
            area_restrict = validated_data['area_restrict'],
            loc_area = validated_data['loc_area'],
            goals = validated_data['goals'],
            gender = validated_data['gender'])

    def update(self, instance, validated_data):
        if validated_data:
            instance.polit = validated_data.get('polit', False)
            instance.interests = validated_data.get('interests', False)
            instance.location = validated_data.get('location', False)
            instance.personality = validated_data.get('personality', False)
            instance.area_restrict = validated_data.get('area_restrict', False)
            instance.loc_area = validated_data.get('loc_area', None)
            instance.goals = validated_data.get('goals', None)
            instance.gender = validated_data.get('gender', None)
            if instance.age:
                age_serializer = AgePrefSerializer()
                age_serializer.update(
                    instance.age,
                    validated_data.get('age', None)
                    )
            elif validated_data['age']:
                age_serializer=PolitCoordinatesSerializer()
                age = age_serializer.create(validated_data['age'])
                instance.age = age
            instance.save()
        else:
            instance.delete()
            return None
        

class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, required=False)
    user_info = UserInfoSerializer(allow_null=True, required=False)
    user_prefs = PreferencesSerializer(allow_null=True, required=False)
    registration = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'registration', 'name', 'user', 'user_info', 'user_prefs']

    def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            if validated_data['registration']:
                hu = User.objects.create_user(username=validated_data['user']['username'], email=validated_data['user']['email'], password=validated_data['user']['password'])
                hu.save()
                info = UserInfo.objects.create()
                info.save()
                ap = AgePref.objects.create(min_age=18, max_age=100, optimal_age=25)
                ap.save()
                prefs = Preferences.objects.create(age=ap)
                prefs.save()
                return CustomUser.objects.create(user=hu, user_info=info, user_prefs=prefs)
            else:
                name = validated_data['name']
                user_info = UserInfoSerializer()
                user_info_created = user_info.create(validated_data['user_info'])
                user_prefs = PreferencesSerializer()
                user_prefs_created = user_prefs.create(validated_data['user_prefs'])
                return CustomUser.objects.create(name=name, user_info=user_info_created, user_prefs=user_prefs_created)

    def update(self, instance, validated_data):
        print("hi")
        instance.name = validated_data['name']
        if instance.user_info:
            user_info_serializer = UserInfoSerializer()
            user_info = user_info_serializer.update(
                instance.user_info, 
                validated_data.get('user_info', None)
                )
        elif validated_data['user_info']:
            user_info_serializer = UserInfoSerializer()
            user_info = user_info_serializer.create(validated_data['user_info'])
            instance.user_info = user_info
        if instance.user_prefs:
            user_prefs_serializer = PreferencesSerializer()
            user_prefs = user_prefs_serializer.update(
                instance.user_prefs, 
                validated_data.get('user_prefs', None)
                )
        elif validated_data['user_prefs']:
            user_prefs_serializer = PreferencesSerializer()
            user_prefs = user_prefs_serializer.create(validated_data['user_prefs'])
            instance.user_prefs = user_prefs
        instance.save()
        return instance