from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    from django.utils import timezone
    from datetime import timedelta
    from .models import Profile

    # Calculate active users (seen in last 5 minutes)
    five_min_ago = timezone.now() - timedelta(minutes=5)
    online_count = Profile.objects.filter(last_seen__gte=five_min_ago).count()

@login_required
@never_cache
def dashboard(request):
    from django.utils import timezone
    from datetime import timedelta
    from .models import Profile
    from .context_processors import inbox_count # Ensure we have access implies settings correct

    # Calculate active users (seen in last 5 minutes)
    five_min_ago = timezone.now() - timedelta(minutes=5)
    online_count = Profile.objects.filter(last_seen__gte=five_min_ago).count()

    return render(request, 'users/dashboard.html', {'online_count': online_count})

from django.http import JsonResponse
import pycountry

def get_states(request):
    country_code = request.GET.get('country')
    if not country_code:
        return JsonResponse({'states': []})
    
    try:
        # Get subdivisions (states) for the country
        subdivisions = pycountry.subdivisions.get(country_code=country_code)
        if subdivisions:
            states = [{'code': sub.code, 'name': sub.name} for sub in subdivisions]
            # Sort by name
            states.sort(key=lambda x: x['name'])
            return JsonResponse({'states': states})
    except Exception as e:
        print(f"Error fetching states: {e}")
        
    return JsonResponse({'states': []})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
        else:
            print(p_form.errors) # DEBUG
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)