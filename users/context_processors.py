from matchmaking.models import CallRequest

def inbox_count(request):
    if request.user.is_authenticated:
        count = CallRequest.objects.filter(receiver=request.user, status='pending').count()
        return {'inbox_count': count}
    return {'inbox_count': 0}
