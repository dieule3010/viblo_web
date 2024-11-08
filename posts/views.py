# posts/views.py
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment
from .models import React
from .models import Category
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q


@login_required #chỉ đăng nhập rồi mới được thực hiện
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Gán tác giả là người dùng hiện tại
            post.save()
            return redirect('post_list')  # Chuyển hướng về trang chủ hoặc trang bài viết vừa tạo
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
def post_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    # Filter posts by search query and category
    posts = Post.objects.all()
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    if category_id:
        posts = posts.filter(category_id=category_id)

    # Initialize paginator only if posts exist
    if posts.exists():
        paginator = Paginator(posts, 5)  # Hiển thị 5 bài viết mỗi trang
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    else:
        posts = None  # Nếu không có bài viết, gán posts là None

    # Pass categories to the template for the filter dropdown
    categories = Category.objects.all()

    return render(request, 'post_list.html', {
        'posts': posts,
        'categories': categories
    })
def post_detail(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    comments = post.comments.filter(parent=None)
    like_count = post.reacts.filter(react_type='like').count()
    dislike_count = post.reacts.filter(react_type='dislike').count()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'like_count': like_count,
        'dislike_count': dislike_count,
    })
    return render(request, 'post_detail.html', {'post': post})
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request,  "Bài viết đã được xóa thành công.")
        return redirect('post_list')
    return render (request, 'delete_confirm.html', {'post': post})
def add_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(post = post, author = request.user, content = content)
    return redirect('post_detail', post_id = post.id)
def react_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    react_type = request.POST.get('react_type') #lấy nội dung từ cơ sở dữ liệu
    #kiểm tra người dùng react trước đó
    react, created = React.objects.get_or_create(post = post, user = request.user, defaults = {'react_type': react_type})
    #nếu đã react thì cập nhật lại react
    if not created:
        if react.react_type == react_type:
            react.delete()
        else:
            react.react_type = react_type
            react.save()
    return redirect('post_detail', post_id = post.id)
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, id=comment_id)
    content = request.POST.get('content')
    if content:
        # Lưu reply với comment cha
        Comment.objects.create(post=post, author=request.user, content=content, parent=parent_comment)
    return redirect('post_detail', post_id=post.id)
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id = comment_id, post_id = post_id)
    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Comment xoa thanh cong!")
    else:
        messages.error(request, "Ban khong co quyen xoa!")
    return redirect ('post_detail', post_id = post_id)
# def category_posts(request, category_id):
#     category = get_object_or_404(Category, id = category_id)
