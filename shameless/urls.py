from django.conf.urls import url, include
from django.contrib import admin

import campaigns.views

urlpatterns = [
    url(r'', include('campaigns.urls')),
    url(r'^login/$', campaigns.views.LoginView.as_view(), name='login'),
    url(r'^signup/$', campaigns.views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', campaigns.views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
]
