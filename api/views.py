from authlib.jose import jwt

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def _jwt_rsp(payload):
    message = jwt.encode(settings.JWT['headers'], payload, settings.JWT['key'])
    return HttpResponse(message, content_type='text/plain')


@require_POST
@csrf_exempt
def email_send(request):

    try:
        claims = jwt.decode(request.body, settings.JWT['key'])
    except:
        return _jwt_rsp({'success': False})


    is_success = False
    emails = claims.get('emails')

    try:
        for email in emails:
            recipients = email.get('recipients')
            for recipient in recipients:
                send_mail(
                    email.get('subject'),
                    email.get('body_plain'),
                    settings.EMAIL_FROM,
                    [recipient],
                    fail_silently=False,
                )
    except:
        is_success = False
    else:
        is_success = True

    ctx = {
            'success': is_success,
        }

    return _jwt_rsp(ctx)
