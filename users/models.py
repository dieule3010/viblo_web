
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms

class Profile(models.Model):
  # tạo để lưu trữ các thông tin bổ sung về người dùng mà model User mặc định của Django không có.
  #Tạo mối quan hệ một-một với model User. Khi người dùng bị xóa, profile cũng sẽ bị xóa.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null = True)
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
   if created:
      user_profile = Profile(user=instance)
      user_profile.save()
post_save.connect(create_profile, sender=User)
# Category of product
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
      return self.name #Trả về tên của danh mục khi in ra
    class Meta:
      #to right grammar
      verbose_name_plural = 'categories'
