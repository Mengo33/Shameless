import datetime
import random

from django.contrib.auth.models import User
from django.test import TestCase

from . import models


class CampaignsTestCase(TestCase):
    def test_add_campaign(self):
        users = [User.objects.create_user(
            "user #{}".format(i + 1)) for i in range(5)]

        n = 12
        for i in range(n):
            c = models.Campaign(
                # user=User.objects.create_user("Dani", "aa@gmail.com", "dani1234"),
                user=random.choice(users),
                title="Campaign #{}".format(i + 1),
                description="gnbstghtrbdtfd  cjybbtbc j6 udr6uybd xycbjhd jry",
                link="https://facebook.com",
                due_date=datetime.date(2016, 1, i + 1),
                replies_num=int(i + 1),
            )
            c.full_clean()
            c.save()

        self.assertEquals(models.Campaign.objects.count(), n)

    def test_add_user(self):
        n = 10
        for i in range(n):
            u = User(
                username="Menahem Godick{}".format(i + 1),
                first_name="Menahem",
                last_name="Godick",
                email="m{}@gmail.com".format(i + 1),
                date_joined=datetime.date(2016, 1, 1),
            )
            u.full_clean()
            u.save()

        self.assertEquals(User.objects.count(), n)
