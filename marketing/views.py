from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .mixins import CsrfExemptMixin
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = "/settings/email/"
    success_message = 'Email Tercihlerin Güncellendi!'
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/accounts/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Email Tercihlerini Güncelle"
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj

"""
POST METHOD
data[ip_opt]: 88.230.137.38

data[email_type]: html

data[merges][LNAME]:

data[web_id]: 44945711

data[merges][PHONE]:

data[merges][ADDRESS]:

data[email]: tol_celik@hotmail.com

data[merges][FNAME]:

fired_at: 2018-12-16 22:43:20

data[list_id]: c8d5de933f

data[merges][BIRTHDAY]:

data[merges][EMAIL]: tol_celik@hotmail.com

type: subscribe

data[id]: 556f202264
"""
class MailchimpWebhookView(CsrfExemptMixin, View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Teşekkür Ederiz", status=200)


    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp().change_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))

        return HttpResponse("Teşekkür Ederiz", status=200)



# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get("type")
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().change_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == "subscribed":
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == "unsubscribed":
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
#
#     return HttpResponse("Teşekkür Ederiz", status=200)