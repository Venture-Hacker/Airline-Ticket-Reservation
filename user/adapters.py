import logging
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from allauth.exceptions import ImmediateHttpResponse

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        logger.debug("pre_social_login called") 

        user_email = sociallogin.account.extra_data.get('email')

        if user_email:
            try:
                existing_user = User.objects.get(email=user_email)
                if existing_user and existing_user.has_usable_password():
                    messages.error(
                        request,
                        'This email is already registered with a local account. Please log in using your username and password.'
                    )
                    raise ImmediateHttpResponse(redirect(reverse('login')))
            except User.DoesNotExist:
                pass

        super().pre_social_login(request, sociallogin)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        email = user.email or sociallogin.account.extra_data.get('email')
        if email and User.objects.filter(email=email).exists():
            existing_user = User.objects.get(email=email)
            if existing_user.has_usable_password():
                messages.error(
                    request,
                    'This email is already registered with a local account. Please log in using your username and password.'
                )
                raise ImmediateHttpResponse(redirect(reverse('login')))
        return user
