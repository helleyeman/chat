from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
# Create your views here.

@login_required
def rooms(request, room_name):
    room = Room.objects.filter(name=room_name).first()
    partner_name = "Unknown"
    
    if room:
        for user in room.users.all():
            if user != request.user:
                partner_name = user.username
                break
                
    is_caller = False
    if partner_name != "Unknown":
        # Deterministic rule: Alphabetically smaller username initiates the call
        if request.user.username < partner_name:
            is_caller = True
                
    return render(request, 'room/room.html', {
        'room_name': room_name,
        'partner_name': partner_name,
        'is_caller': is_caller
    })


