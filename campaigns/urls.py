from django.conf.urls import url

from . import views

app_name = "campaigns"
urlpatterns = [
    url(r'^$', views.ListCampaignView.as_view(), name="list"),
    url(r'^add-campaign/$', views.CreateCampaignView.as_view(), name="create_campaign"),
    url(r'^(?P<pk>\d+)/$', views.CampaignDetailView.as_view(), name="campaign_details"),
    url(r'^(?P<pk>\d+)/add-reply/$', views.CreateReplyView.as_view(), name="create_reply"),
    url(r'^(?P<pk>\d+)/reply_details/$', views.ReplyDetailView.as_view(), name="reply_details"),
    url(r'^view-replies/$', views.ListRepliesView.as_view(), name="replies_list"),
]
