from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class ChatGoal(models.TextChoices):
    FRIENDSHIP = 'FR', ('Friendship')
    ROMANTIC = 'RO', ('Romantic')
    ANYTHING = 'AN', ('Anything')

class Gender(models.TextChoices):
    MALE = 'M', ('Male')
    FEMALE = 'F', ('Female')
    ANYTHING = 'A', ('Anything')

class PolitCoordinates(models.Model):
    eco = models.FloatField(null=True)
    cult = models.FloatField(null=True)

    def __str__(self):
        return str(self.eco)+":"+str(self.cult)


class GeoCoordinates(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    def __str__(self):
        return str(self.lat)+":"+str(self.lon)


class AgePref(models.Model):
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    optimal_age = models.IntegerField(null=True)
    def __str__(self):
        return str(self.min_age)+":"+str(self.optimal_age)+":"+str(self.max_age)

class Personality(models.Model):
    extraversion = models.FloatField(null=True)
    agreeableness = models.FloatField(null=True)
    openness = models.FloatField(null=True)
    conscientiousness = models.FloatField(null=True)
    neuroticism = models.FloatField(null=True)

    def __str__(self):
        return str(self.extraversion)+":"+str(self.agreeableness)+":"+str(self.openness)+":"+str(self.conscientiousness)+":"+str(self.neuroticism)


class UserInfo(models.Model):
    # filtering
    description = models.CharField(max_length=1000, default="")
    country = models.CharField(max_length=200, null=True)

    languages = ArrayField(models.CharField(max_length=200), null=True)

    # data

    interests = ArrayField(models.CharField(max_length=200), null=True)

    polit_coordinates = models.OneToOneField(
        PolitCoordinates, 
        null=True, 
        on_delete=models.SET_NULL
    )

    age = models.IntegerField(null=True)

    location = models.OneToOneField(
        GeoCoordinates, 
        null=True, 
        on_delete=models.SET_NULL
    )

    gender = models.CharField(max_length=2,
        choices=Gender.choices,
        default=Gender.MALE,
    )

    personality = models.OneToOneField(
        Personality, 
        null=True, 
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return 'Info\ncountry:{}, langs: {}, interests: {}, pol_coords: {}, age: {}, location: {}, gender: {}, personality: {}'.format(self.country, self.languages, self.interests, self.polit_coordinates, self.age, self.location, self.gender, self.personality)

class Preferences(models.Model):
    # filtering + calc
    age = models.OneToOneField(
        AgePref, 
        null=True, 
        on_delete=models.SET_NULL
    )

    # calculating

    polit = models.BooleanField(max_length=200, default=False)

    interests = models.BooleanField(max_length=200, default=False)

    location = models.BooleanField(max_length=200, default=False)

    personality = models.BooleanField(max_length=200, default=False)

    area_restrict = models.BooleanField(max_length=200, default=False)

    loc_area = models.IntegerField(null=True, default=10)

    goals = models.CharField(max_length=2,
        choices=ChatGoal.choices,
        default=ChatGoal.ANYTHING,
    )

    gender = models.CharField(max_length=2,
        choices=Gender.choices,
        default=Gender.ANYTHING,
    )

    def __str__(self):
        return 'Prefs:\nage: {}, polit: {}, interests: {}, location: {}, goals: {}, gender: {}, personality: {}, loc_area: {}'.format(self.age, self.polit, self.interests, self.location, self.goals, self.gender, self.personality, self.loc_area)

class HistoricalChat(models.Model):
    chattedWith = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField('date started talking', auto_now_add=True)

class CustomUser(models.Model):
    name = models.CharField(max_length=200, default='anon')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    status = models.CharField(max_length=200, default='Inactive')
    room_to_join = models.IntegerField(null=True)
    userInfo = models.ForeignKey(UserInfo, related_name='user_info', on_delete=models.CASCADE, null=True)
    userPrefs = models.ForeignKey(Preferences, related_name='user_prefs', on_delete=models.CASCADE, null=True)
    sentFriendRequests = models.ManyToManyField('CustomUser', related_name='receivedFriendRequests')
    ignoredUsers = models.ManyToManyField('CustomUser', related_name='usersIgnoredBy')
    friends = models.ManyToManyField('CustomUser')
    historicalChats = models.ManyToManyField('HistoricalChat')

    def __str__(self):
        return 'Name: {}\n{}\n{}'.format(self.user, self.userInfo, self.userPrefs)

class Message(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # change to custom user
    timestamp = models.DateTimeField('date sent', auto_now_add=True)
    read = models.BooleanField(default=False)

class ChatRoom(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message)

class Chat(models.Model):
    #user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE, null=True)
    #user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE, null=True)
    user_1 = models.CharField(max_length=200, null=True)
    user_2 = models.CharField(max_length=200, null=True)

class SearchingInstance(models.Model):
    is_done = models.BooleanField(max_length=200, default=False)
    room_to_join = models.IntegerField(null=True)