import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
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


class CampaignerOutMixin:
    def dispatch(self, request, *args, **kwargs):
        if not models.CampaignUser.objects.filter(campaign_user=request.user.pk).exists():
            url = reverse("/") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    page_title = "Login"
    template_name = "login.html"
    form_class = forms.LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():  # and models.CampaignUser.objects.filter(pk=request.user.pk).exists():
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

        # check if User is_campaigner or is_writer
        # if isinstance(models.CampaignUser(user), models.CampaignUser):
        #     self.request.session['is_campaigner'] = True
        # if isinstance(models.WriterUser(user), models.WriterUser):
        #     self.request.session['is_writer'] = True

        return redirect('campaigns:list')


class ListCampaignView(LoggedInMixin, ListView):
    page_title = "Campaign list"
    model = models.Campaign
    paginate_by = 5

    def get_queryset(self):
        if not models.CampaignUser.objects.filter(campaign_user_id=self.request.user.pk).exists():
            return super().get_queryset().all()
        else:
            return super().get_queryset().filter(
                owner=models.CampaignUser.objects.get(campaign_user_id=self.request.user.pk))


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
        pupk = models.ProfileUser.objects.get(profile_user_id=self.request.user.pk).pk
        if models.CampaignUser.objects.filter(campaign_user_id=pupk).exists():
            form.instance.owner = models.CampaignUser.objects.filter(campaign_user_id=pupk)
        else:
            form.instance.owner = models.CampaignUser(campaign_user=models.ProfileUser())
        resp = super().form_valid(form)
        # messages.SUCCESS(self.request, "Campaign added successfully.") #TODO formating
        return resp


class CampaignDetailView(LoggedInMixin, DetailView):
    page_title = "Campaign Details"
    model = models.Campaign

    def dispatch(self, request, *args, **kwargs):
        self.request.session['campaign_id'] = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)


class ReplyDetailView(LoggedInMixin, DetailView):
    page_title = "Reply Details"
    model = models.Reply


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

        is_campaigner, is_writer = form.cleaned_data.pop('is_campaigner'), form.cleaned_data.pop('is_writer')
        if is_campaigner == is_writer:
            form.add_error(None, "User must be a campaigner or writer (not both).")
            return self.form_invalid(form)

        # Add new user instance
        user = User.objects.create_user(**form.cleaned_data)
        user = authenticate(**form.cleaned_data)

        # Add new user to ProfileUser
        pu = models.ProfileUser(profile_user=user, )
        pu.full_clean()
        pu.save()

        # Add new user to CampaignUser Or WriterUser
        if is_campaigner:
            cu = models.CampaignUser(campaign_user=pu, )
            cu.full_clean()
            cu.save()
            # self.request.session['is_campaigner'] = True
            # TODO - add a line to log
        if is_writer:
            wu = models.WriterUser(writer_user=pu, )
            wu.full_clean()
            wu.save()
            # self.request.session['is_writer'] = True
            # TODO - add a line to log

        # Login
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


class CreateReplyView(CampaignerOutMixin, LoggedInMixin, CreateView):
    page_title = "Reply to campaign "
    campaign = None
    model = models.Reply
    fields = (
        'reply_text',
    )

    success_url = reverse_lazy('campaigns:list')

    def form_valid(self, form):
        form.instance.writer = models.WriterUser.objects.get(
            writer_user_id=self.request.user.pk)
        form.instance.campaign = self.campaign
        resp = super().form_valid(form)
        c = models.Campaign.objects.get(pk=self.request.session['campaign_id'])
        if c.replies_left:
            c.replies_left -= 1
            c.full_clean()
            c.save()
        elif c.replies_left == 0:
            resp = super().form_invalid(form)
            form.add_error(None, "No more reply option left.")
            # TODO check if no replies left before to try adding one..

        # messages.SUCCESS(self.request, "Campaign added successfully.") #TODO formating
        return resp

    def dispatch(self, request, *args, **kwargs):
        self.request.session['campaign_id'] = kwargs['pk']

        if models.CampaignUser.objects.filter(campaign_user_id=request.user.pk).exists():
            redirect("campaigns:campaign_details", args=(self.request.session['campaign_id'],))

        campaign_name = (models.Campaign.objects.get(pk=self.request.session['campaign_id'])).title
        self.page_title += '"{}"'.format(campaign_name)
        self.campaign = (models.Campaign.objects.get(pk=self.request.session['campaign_id']))

        return super().dispatch(request, *args, **kwargs)


class ListRepliesView(LoggedInMixin, ListView):
    page_title = "Replies list"
    model = models.Reply
    paginate_by = 5

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         campaign=models.Campaign.objects.get(pk=self.request.session['campaign_id']))

    def get_queryset(self):
        if not models.CampaignUser.objects.filter(campaign_user_id=self.request.user.pk).exists():
            return super().get_queryset().filter(
                writer=models.WriterUser.objects.filter(writer_user_id=self.request.user.pk),
                campaign=models.Campaign.objects.get(pk=self.request.session['campaign_id']),
            )
        else:
            return super().get_queryset().filter(
                campaign=models.Campaign.objects.get(pk=self.request.session['campaign_id']))

# class CreateProfileUserView(LoggedInMixin, CreateView):
#     page_title = "Edit Profile Details"
#     model = models.ProfileUser
#     fields = (
#         'email'
#         'phone'
#     )
#
#     def get_initial(self):
#         f = super().get_initial()
#         f['']
