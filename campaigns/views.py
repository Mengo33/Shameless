import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from . import forms
from . import models


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    page_title = "Login"
    template_name = "login.html"
    form_class = forms.LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('campaigns:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None:
            if user.is_active:
                login(self.request, user)
                if self.request.GET.get('from'):
                    return redirect(
                        self.request.GET['from'])  # SECURITY: check path
            else:
                form.add_error(None, "User isn't active anymore - plz contact admin")
                return self.form_invalid(form)
        else:
            form.add_error(None, "username doesn't exist")
            return self.form_invalid(form)


class ListCampaignView(LoggedInMixin, ListView):
    page_title = "Campaign list"
    model = models.Campaign

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class CreateCampaignView(LoggedInMixin, CreateView):
    page_title = "Campaign Adding - Form"
    model = models.Campaign
    fields = (
        'title',
        'description',
        'link',
        'due_date',
        'replies_num',
    )

    success_url = reverse_lazy('campaigns:list')

    def get_initial(self):
        d = super().get_initial()
        d['due_date'] = datetime.date.today()
        return d

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CampaignDetailView(LoggedInMixin, DetailView):
    page_title = "Campaign Details"
    model = models.Campaign

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SignupView(FormView):
    page_title = "Signup"
    template_name = "signup.html"
    form_class = forms.SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('campaigns:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data.pop('password_recheck'):
            form.add_error(None, "Passwords do not match")
            return self.form_invalid(form)
        user = User.objects.create_user(**form.cleaned_data)
        user = authenticate(**form.cleaned_data)

        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                form.add_error(None, "Disabled account")
                return self.form_invalid(form)
            if self.request.GET.get('from'):
                return redirect(
                    self.request.GET['from'])  # SECURITY: check path
            return redirect('campaigns:list')
