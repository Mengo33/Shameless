from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Campaign(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    link = models.CharField(max_length=100)
    due_date = models.DateField()
    replies_num = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("campaigns:campaign_details", args=(self.pk,))


class CampaignUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    is_customr = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
