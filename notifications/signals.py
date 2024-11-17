from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification
from posts.models import Post
from users.models import User

def create_comment_notification(sender, instance, created, **kwargs):
  if created:
    post = instance.post
    author = post.author
    if author != instance.user:
      message = f"{instance.user.username} da binh luan bai viet cua ban!"
      Notification.objects.create(user = author, message = message)
def create_react_notification(sender, instance, created, **kwargs):
  if created:
    post = instance.post
    author = post.author
    if author != instance.user:
      message = f"{instance.user.username} da react bai viet cua ban!"
      Notification.objects.create(user=author, message = message)