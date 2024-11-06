from django.urls import path
from .views import create_post
from .views import post_list
from .views import post_detail
from .views import delete_post
from .views import add_comment
from .views import react_post
from .views import add_reply
from .views import delete_comment



urlpatterns = [
    path('create/', create_post, name='create_post'),  # URL cho chức năng viết bài
    path('post_list/', post_list, name='post_list'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('post_detail/<int:post_id>/comment', add_comment, name='add_comment'),
    path('post_detail/<int:post_id>/react', react_post, name='react_post'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/add_reply', add_reply, name='add_reply'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/delete_comment', delete_comment, name='delete_comment'),
 
]
