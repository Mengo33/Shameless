from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Gender:
    MALE = 1
    FEMALE = 2

    choices = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )


class ProfileUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,)

    gender = models.IntegerField(choices=Gender.choices, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    # TODO 1) add data members \ methods that aren't in models.User
    # TODO and should be in both CampaignUser & WriterUser
    # TODO 2) Ask Udi \ google about having to do this  class abstract while this is also a FK


class CampaignUser(models.Model):
    profile_user = models.OneToOneField(
        ProfileUser,
        on_delete=models.CASCADE,)
    # TODO


class WriterUser(models.Model):
    profile_user = models.OneToOneField(
        ProfileUser,
        on_delete=models.CASCADE, )
    # TODO


class Campaign(models.Model):
    owner = models.ForeignKey(CampaignUser)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    link = models.URLField()
    due_date = models.DateField()
    replies_num = models.IntegerField(default=1)
    replies_left = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("campaigns:campaign_details", args=(self.pk,))

    # def get_absolute_url(self):
    #     return reverse("campaigns:create_reply", args=(self.pk,))

    def __str__(self):
        return "Campaign {} ({} replies left)".format(
            self.title,
            self.replies_left,
        )


class Reply(models.Model):
    class Status:
        CREATED = 1
        CHECKING = 2
        REJECTED = 3
        APPROVED = 4
        POSTED = 5
        DISCARDED = 6

        choices = (
            (CREATED, 'Created'),
            (CHECKING, 'Checking'),
            (REJECTED, 'Rejected'),
            (APPROVED, 'Approved'),
            (POSTED, 'Posted'),
            (DISCARDED, 'Discarded'),
        )

    writer = models.ForeignKey(WriterUser)
    campaign = models.ForeignKey(Campaign, related_name="replies")
    reply_text = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    posted_at = models.DateField(null=True, blank=True)
    reply_link = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.CREATED)

    def __str__(self):
        return "Reply {} owner {} status {}".format(
            self.pk,
            self.user,
            self.status,
        )
