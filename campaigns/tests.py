import datetime
import random
import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from . import models


class CampaignsTestCase(TestCase):
    def test_user(self):
        n = 10
        for i in range(n):
            u = User.objects.create_user(
                "user@{}".format(i + 1))
            u.full_clean()
            u.save()
            # print(u)
        self.assertEquals(User.objects.count(), n)

    def test_profile_user(self):
        n = 10
        for i in range(n):
            u = User.objects.create_user(
                "user@{}".format(i + 1))
            u.full_clean()
            u.save()
            pu = models.ProfileUser(user=u,
                                    gender=models.Gender.FEMALE,
                                    dob=datetime.date(1980, i + 1, i + 1))
            pu.full_clean()
            pu.save()
            # print(pu.user)
            # print(pu)
        self.assertEquals(models.ProfileUser.objects.count(), n)

    def test_campaign_user(self):
        n = 10
        for i in range(n):
            u = User.objects.create_user(
                "user@{}".format(i + 1))
            u.full_clean()
            u.save()

            pu = models.ProfileUser(user=u,
                                    gender=models.Gender.FEMALE,
                                    dob=datetime.date(1980, i + 1, i + 1))
            pu.full_clean()
            pu.save()

            cu = models.CampaignUser(campaign_user=pu, )
            cu.full_clean()
            cu.save()
        self.assertEquals(models.CampaignUser.objects.count(), n)

    def test_add_campaign(self):
        # TODO ADD DETAILS FOR USER (E.G. MAIL ETC.)

        n = 12
        for i in range(n):
            u = User.objects.create_user(
                "user@{}".format(i + 1))
            u.full_clean()
            u.save()

            pu = models.ProfileUser(user=u,
                                    gender=models.Gender.FEMALE,
                                    dob=datetime.date(1980, i + 1, i + 1))
            pu.full_clean()
            pu.save()

            cu = models.CampaignUser(campaign_user=pu, )
            cu.full_clean()
            cu.save()

            c = models.Campaign(
                owner=cu,
                title="Campaign #{}".format(i + 1),
                description="gnbstghtrbdtfd  cjybbtbc j6 udr6uybd xycbjhd jry",
                link="https://facebook.com",
                due_date=datetime.date(2016, i + 1, i + 1),
                replies_num=int(i + 1),
            )
            c.full_clean()
            c.save()

        self.assertEquals(models.Campaign.objects.count(), n)

    def test_add_reply(self):
        # TODO ADD DETAILS FOR USER (E.G. MAIL ETC.)

        n = 12
        for i in range(n):
            u = User.objects.create_user(
                "user@{}".format(i + 1))
            u.full_clean()
            u.save()

            pu = models.ProfileUser(user=u,
                                    gender=models.Gender.FEMALE,
                                    dob=datetime.date(1980, i + 1, i + 1))
            pu.full_clean()
            pu.save()

            cu = models.CampaignUser(campaign_user=pu, )
            cu.full_clean()
            cu.save()

            c = models.Campaign(
                owner=cu,
                title="Campaign #{}".format(i + 1),
                description="gnbstghtrbdtfd  cjybbtbc j6 udr6uybd xycbjhd jry",
                link="https://facebook.com",
                due_date=datetime.date(2016, i + 1, i + 1),
                replies_num=int(i + 1),
            )
            c.full_clean()
            c.save()

            wu = models.WriterUser(writer_user=pu, )
            wu.full_clean()
            wu.save()

            r = models.Reply(
                writer=wu,
                campaign=c,
                reply_text="jhgjcg iugcvgkugku vgiugvi uvgiuvt vii",
                reply_link="http://stackoverflow.com/questions/3759{}".format(random.randint(1000, 9999)),
            )
            r.full_clean()
            r.save()

        self.assertEquals(models.Reply.objects.count(), n)
