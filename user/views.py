from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    ctx = {
            'user': request.user,
        }
    return render(request, 'user/profile.html', ctx)

