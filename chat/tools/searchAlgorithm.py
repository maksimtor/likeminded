import time
import json
from chat.models import CustomUser as User
from chat.models import Chat
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness, AcceptanceCalculator, LikenessCalculator

def waiting_for_invite(consumer, user, wait_time):
	for i in range (0, wait_time):
		print(i)
		time.sleep(1)
		if User.objects.get(pk=user.pk).status == 'Invited':
			print ("User " + user.name + " is invited to " + str(User.objects.get(pk=user.pk).room_to_join))
			consumer.send(text_data=json.dumps({
					'type': 'chat_message',
					'message': User.objects.get(pk=user.pk).room_to_join,
					'name': 'name'
				}))
			return 1
		if User.objects.get(pk=user.pk).status == 'Stopped':
			return 1

def search_to_invite(consumer, user):
	while User.objects.get(pk=user.pk).status == 'Searching':
		searching_users = User.objects.filter(status="Searching").select_related('user_info').select_related('user_prefs')
		(best_user, best_score) = find_most_like_minded(user, searching_users, consumer)
		if best_score > 0 and User.objects.get(pk=best_user).status == "Searching":
			join_the_room(user, best_user, consumer)
			return 1

def find_most_like_minded(user, searching_users, consumer):
	best_user = None
	best_score = 0
	for target_user in searching_users:
		main_accepts_target = AcceptanceCalculator(main_user=user, target_user=target_user)
		target_accepts_main = AcceptanceCalculator(main_user=target_user, target_user=user)
		users_match = main_accepts_target.users_match() and target_accepts_main.users_match()
		if (users_match and user.id != target_user.id and target_user not in user.ignored_users.all() and target_user not in user.usersIgnoredBy.all()):
			l1m = LikenessCalculator(main_user=user, target_user=target_user)
			l2m = LikenessCalculator(main_user=target_user, target_user=user)
			l1 = l1m.calc_likeness()
			l2 = l2m.calc_likeness()
			result = (l1+l2)/2
			if result>best_score:
				best_score = result
				best_user = target_user.pk
		if User.objects.get(pk=user.pk).status == 'Invited':
			print ("User " + user.name + " is invited to " + str(User.objects.get(pk=user.pk).room_to_join))
			consumer.send(text_data=json.dumps({
				'type': 'chat_message',
				'message': User.objects.get(pk=user.pk).room_to_join,
				'name': 'name'
			}))
			return 1
		if User.objects.get(pk=user.pk).status == 'Stopped':
			return 1
	return (best_user, best_score)

def join_the_room(user, best_user, consumer):
	print("Getting to the room")
	chat = Chat()
	chat.save()
	matching_user = User.objects.get(pk=best_user)
	matching_user.room_to_join = chat.id
	matching_user.status = "Invited"
	matching_user.save()
	myself = User.objects.get(pk=user.pk)
	myself.status="Inactive"
	myself.save()
	# User.objects.get(pk=user.pk).status = "Inactive"
	print ("User " + str(user.name) + " created chat " + str(chat.id))
	consumer.send(text_data=json.dumps({
		'type': 'chat_message',
		'message': chat.id,
		'name': 'name'
	}))