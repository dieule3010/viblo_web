from django.urls import path
from .import views
from .views import (
    create_post,
    post_list,
    post_detail,
    delete_post,
    add_comment,
    react_post,
    add_reply,
    delete_comment,
    delete_reply,
    edit_reply,
    edit_comment
)
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('create/', create_post, name='create_post'),  # URL cho chức năng viết bài
    path('post_list/', post_list, name='post_list'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('post_detail/<int:post_id>/comment', add_comment, name='add_comment'),
    path('post_detail/<int:post_id>/react', react_post, name='react_post'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/add_reply', add_reply, name='add_reply'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/add_reply', add_reply, name='add_reply'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/delete_comment', delete_comment, name='delete_comment'),
    path('post_detail/<int:post_id>/reply/<int:reply_id>/delete_reply', delete_reply, name='delete_reply'),
    path('post_detail/<int:post_id>/reply/<int:reply_id>/edit_reply', edit_reply, name='edit_reply'),
    path('post_detail/<int:post_id>/comment/<int:comment_id>/edit_comment', edit_comment, name='edit_comment'),

]
