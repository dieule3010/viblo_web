from django.shortcuts import render
from .models import Notification

def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-create_at')
    return render(request, 'notifications.html', {'notifications': notifications})
