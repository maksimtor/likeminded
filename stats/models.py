from django.db import models
from chat.models import CustomUser

class ChatStatistics(models.Model):
    user = models.ForeignKey(CustomUser, related_name='chat_stats', on_delete=models.CASCADE, null=True)
    talked_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    seconds_to_find = models.IntegerField(null = True)
    seconds_spend = models.IntegerField(null = True)
    messages_shared = models.IntegerField(null = True)

    def __str__(self):
        return 'User {} spend {} seconds to find a match and talked for {} seconds.'.\
    format(self.user.name, self.seconds_to_find, self.seconds_spend)