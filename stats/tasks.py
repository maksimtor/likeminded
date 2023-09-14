from stats.models import ChatStatistics

from celery import shared_task

@shared_task
def add_chat_stats(user_id, total_time):
    ChatStatistics.objects.create(user_id = user_id, seconds_to_find = total_time)

@shared_task
def update_chat_stats_time(user_id, session_time):
    stat = ChatStatistics.objects.filter(user_id=user_id).latest('id')
    stat.seconds_spend = session_time
    stat.save()