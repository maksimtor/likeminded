from stats.models import ChatStatistics

from celery import shared_task

@shared_task
def add_chat_stats(user_id, total_time):
    ChatStatistics.objects.create(user_id = user_id, seconds_to_find = total_time)