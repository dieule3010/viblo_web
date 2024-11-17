from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField

class Category(models.Model):
  name = models.CharField(max_length=255, unique= True)
  description = models.TextField(blank= True, null = True)
  def __str__(self):
    return self.name
  def get_absolute_url(self):
    return reverse('home')

class Post(models.Model):
  CATEGORY_CHOICES = [
        ('coding', 'Coding'),
        ('entertainment', 'Entertainment'),
        ('music', 'Music'),
    ]
  title = models.CharField(max_length=200)  # Tiêu đề bài viết
  content =models.TextField()  # Nội dung bài viết
  author = models.ForeignKey(User, on_delete=models.CASCADE)  # Người viết bài
  created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo bài viết
  updated_at = models.DateTimeField(auto_now=True)  # Ngày cập nhật bài viết
  image = models.ImageField(upload_to='post_images/', blank=True, null=True)
  is_approved = models.BooleanField(default= False)
  scheduled_date = models.DateTimeField(null=True, blank=True)
  likes = models.IntegerField(default= 0)
  category = models.CharField(max_length= 255, default='coding')
  def __str__(self):
    return self.title  # Trả về tiêu đề bài viết

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
  content = models.TextField()
  parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
  create_at = models.DateTimeField(auto_now_add=True)
  parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
  def __str__(self):
    return f"Comment by {self.author} on {self.post}"
class Reply(models.Model):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name= 'replies')
  author = models.ForeignKey(User, on_delete = models.CASCADE)
  content = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)
class React(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  react_type = models.CharField(max_length=10, choices= [('like', 'Like'), ('dislike', 'Dislike')])
  create_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    unique_together = ('post', 'user') #mỗi người được react 1 lần