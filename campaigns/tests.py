import datetime
from django.test import TestCase
from campaigns import models


class CampaignsTestCase(TestCase):
    def test_campaign(self):
        # users = [User.objects.create_user(
        #     "user #{}".format(i + 1)) for i in range(5)]


        n = 12
        for i in range(n):
            c = models.Campaign(
                # user_id=random.choice(users),
                title="Expense #{}".format(i + 1),
                description="gnbstghtrbdtfd  cjybbtbc j6 udr6uybd xycbjhd jry",
                link="https://facebook.com",
                due_date=datetime.date(2016, 1, i + 1),
                replies_num=int(i + 1),
            )
            c.full_clean()
            c.save()

        self.assertEquals(models.Campaign.objects.count(), n)
