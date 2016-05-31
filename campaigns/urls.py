from django.conf.urls import url

from . import views

app_name = "campaigns"
urlpatterns = [
    url(r'^$', views.ListCampaignView.as_view(), name="list"),
    # url(r'^$', views.list_campaigns, name="list"),
    url(r'^add-campaign/$', views.CreateCampaignView.as_view(), name="create_campaign"),
]
