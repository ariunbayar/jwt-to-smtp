### Usage

```
#!/usr/bin/env python3

from authlib.jose import jwt
import urllib.request
from django.conf import settings


payload = {
        'emails': [
            {
                'recipients': ['john@example.com'],
                'subject': 'Test email subject',
                'body_plain': 'Test plain body',
            },
        ]
    }

message = jwt.encode(settings.JWT['headers'], payload, settings.JWT['key'])

message = urllib.request.urlopen("http://localhost:8000/api/send-email/", message).read()

try:
    claims = jwt.decode(message, settings.JWT['key'])
    print(claims['success'])
except:
    print('ERROR: Cannot decode response')

```
