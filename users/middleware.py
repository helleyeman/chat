from django.utils import timezone

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.profile.last_seen = timezone.now()
            request.user.profile.save(update_fields = ['last_seen'])
        return self.get_response(request)

from django.shortcuts import render
from django.contrib.auth import logout

class BanEnforcementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                if request.user.profile.is_banned:
                    # Force logout and show banned page
                    logout(request)
                    return render(request, 'users/banned.html')
            except:
                pass # Profile might not exist yet
                
        return self.get_response(request)