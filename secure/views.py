from datetime import timedelta
import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.utils.timezone import localtime, now
from django.contrib.auth import get_user_model

from .models import LoginToken
from .forms import LoginTokenForm


@csrf_protect
def login(request):

    if request.method == 'POST':

        form = LoginTokenForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')

            login_token = LoginToken()
            login_token.token = uuid.uuid4().hex
            login_token.expires_at = now() + timedelta(minutes=20)
            login_token.email = email
            login_token.is_used = False
            login_token.save()

            url = request.build_absolute_uri(reverse('login-token', args=[login_token.token]))
            send_mail(
                'Authentication to Resource Manager',
                'Доорхи линк дээр дарж нэвтэрнэ үү!\n%s' % url,
                settings.EMAIL_FROM,
                [email],
                fail_silently=False,
            )
            return redirect(reverse('login-token-sent') + '?email=' + email)

    else:
        form = LoginTokenForm()

    context = {
            'form': form,
        }
    return render(request, 'secure/login.html', context)


def login_token_sent(request):
    ctx = {
            'email': request.GET.get('email'),
        }
    return render(request, 'secure/login_token_sent.html', ctx)


def login_token(request, token):

    login_token = LoginToken.objects.filter(token=token, expires_at__gt=localtime(now()), is_used=False).first()
    User = get_user_model()

    if login_token:
        login_token.is_used = True
        login_token.save()

        user = User.objects.filter(email=login_token.email).first()
        if not user:
            user = User()
            user.username = login_token.email
            user.email = login_token.email
            user.password = ''
            user.save()
        auth.login(request, user)

        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect('login-token-failed')


def login_token_failed(request):
    return render(request, 'secure/login-token-failed.html', {})


@require_GET
@login_required
def logout(request):
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
