from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class Category(models.Model):
  name = models.CharField(max_length=100, unique= True)
  description = models.TextField(blank= True, null = True)
  def __str__(self):
    return self.name

class Post(models.Model):
  title = models.CharField(max_length=200)  # Tiêu đề bài viết
  content = RichTextField()  # Nội dung bài viết
  author = models.ForeignKey(User, on_delete=models.CASCADE)  # Người viết bài
  created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo bài viết
  updated_at = models.DateTimeField(auto_now=True)  # Ngày cập nhật bài viết
  image = models.ImageField(upload_to='post_images/', blank=True, null=True)
  tags = TaggableManager()
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts' )

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

  def __str__(self):
    return f"Comment by {self.author} on {self.post}"
class React(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reacts')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  react_type = models.CharField(max_length=10, choices= [('like', 'Like'), ('dislike', 'Dislike')])
  create_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    unique_together = ('post', 'user') #mỗi người được react 1 lần