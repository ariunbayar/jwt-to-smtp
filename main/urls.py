from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import secure.views
import user.views
import api.views


urlpatterns = [

    path('login/', secure.views.login, name='login'),
    path('login/token/sent/', secure.views.login_token_sent, name='login-token-sent'),
    path('login/<str:token>/', secure.views.login_token, name='login-token'),
    path('login/token/failed/', secure.views.login_token_failed, name='login-token-failed'),
    path('logout/', secure.views.logout, name='logout'),

    path('u/profile/', user.views.profile, name='user-profile'),

    path('api/send-email/', api.views.email_send, name='api-email-send'),

]


if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
