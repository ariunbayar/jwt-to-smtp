from django.db import models


class LoginToken(models.Model):

    email = models.CharField(max_length=250)
    token = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
