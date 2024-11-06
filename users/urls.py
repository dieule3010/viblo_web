from django.urls import path
from .import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about.html', views.about, name='about'),
    path('login.html', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('register/',views.user_register, name='register'),
    path('update_info/',views.update_info, name='update_info'),
    path('post/', include('posts.urls')),
]