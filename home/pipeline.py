from django.shortcuts import redirect
from django.contrib import messages

def validate_admin_email(strategy, details, backend, *args, **kwargs):
    from django.contrib.auth.models import User

    email = details.get('email')
    request = strategy.request  # get the current request

    if not User.objects.filter(email=email, is_staff=True).exists():
        messages.error(request, "Unauthorized Google account")
        return redirect("admin")  # redirects to your custom login page

    return
