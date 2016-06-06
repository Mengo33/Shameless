import datetime
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from campaigns import models


class Command(BaseCommand):
    help = "This script add  records to the DB" \
           "Usage: {} [OPTION]" \
           "<record_type>=<number_to_add> " \
           "u - User, c - Campaign, r - Reply, cu - CampaignUser, w - Writer " \
           "Example:" \
           "cu=8  u=3".format(os.path.basename(__file__))

    # def add_arguments(self, parser):
    #     # parser.add_argument('tst_id', nargs="+", type=int)
    #     parser.add_argument(u='0', c='0', r='0', cu='0', w='0')

    def handle(self, *args, **options):
        # print("args {}{}options {}".format(args, '\n', options))
        # u = User.objects.create_user(
        #     "user@7")
        # u.full_clean()
        # u.save()
        #
        # pu = models.ProfileUser(user=u,
        #                         gender=models.Gender.FEMALE,
        #                         dob=datetime.date(1980, 7, 7))
        # pu.full_clean()
        # pu.save()
        #
        # cu = models.CampaignUser(campaign_user=pu, )
        # cu.full_clean()
        # cu.save()
        #
        # o = models.Campaign.objects.create(owner=cu,
        #                                    title="Campaign #7",
        #                                    description="gnbstghtrbdtfd  cjybbtbc j6 udr6uybd xycbjhd jry",
        #                                    link="https://facebook.com",
        #                                    due_date=datetime.date(2016, 7, 7),
        #                                    replies_num=7, )
        assert False, "bla"
