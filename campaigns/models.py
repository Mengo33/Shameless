from django.conf import settings
from django.db import models


class Campaign(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    link = models.CharField(max_length=50)  # TODO replace CharField it to link field.
    due_date = models.DateField()
    replies_num = models.IntegerField(default=1)

