# posts/views.py
from django.shortcuts import render, redirect
from .forms import PostForm
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment
from .models import React
from .models import Category
from .models import Reply
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden

@login_required #chỉ đăng nhập rồi mới được thực hiện
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) #không cam kết lưu ngay vào cơ sở dữ liệu, cho phép thiết lập thêm các trường
            post.author = request.user  # Gán tác giả là người dùng hiện tại
            post.save()
            return redirect('post_list')  # Chuyển hướng về trang chủ hoặc trang bài viết vừa tạo
    else:
        form = PostForm() #nếu yêu cầu không phải là Post thì sẽ tạo một form trống cho người dùng điền vào
    return render(request, 'create_post.html', {'form': form})
def post_list(request):
    search_query = request.GET.get('search', '') # lấy giá trị tìm kiếm của user
    category_id = request.GET.get('category', '') # lấy thông tin lọc của danh mục

    # Filter posts by search query and category
    posts = Post.objects.all()
    if search_query: #Dùng Q để kết hợp các điều kiện tìm kiếm cho cả title và content
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    if category_id:
        posts = posts.filter(category_id=category_id) #Nếu có category_id, bài viết được lọc theo danh mục.

    # Initialize paginator only if posts exist
    if posts.exists():
        paginator = Paginator(posts, 4)  # Hiển thị 5 bài viết mỗi trang
        page_number = request.GET.get('page', 1)
        posts = paginator.get_page(page_number) #dùng để lấy các bài viết của trang hiện tại, page_number là số trang cần nhập, nếu số trang nhập lớn hơn hiện có, thì trả về trang cuối cùng
    else:
        posts = None  # Nếu không có bài viết, gán posts là None

    # Pass categories to the template for the filter dropdown
    categories = Category.objects.all() # lấy tất cả các danh mục

    return render(request, 'post_list.html', {
        'posts': posts,
        'categories': categories
    })
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent__isnull=True)  # Chỉ lấy các comments chính, không bao gồm reply
    like_count = post.reactions.filter(react_type='like').count()
    dislike_count = post.reactions.filter(react_type='dislike').count()
    context = {
        'post': post,
        'comments': comments,
        'like_count': like_count,
        'dislike_count': dislike_count,
    }
    return render(request, 'post_detail.html', context)
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
        Comment.objects.create(post = post, author = request.user, content = content) # hàm tạo một đối tượng Comment và lưu vào cơ sở dữ liệu.
    return redirect('post_detail', post_id = post.id)
def react_post(request, post_id):
    post = get_object_or_404(Post, id = post_id) #lấy bài viết
    react_type = request.POST.get('react_type') #lấy loại phản ứng từ form gửi lên
    #kiểm tra người dùng react trước đó, kiểm tra xem đã react bài viết chưa
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
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.parent = parent_comment
            # Thêm @username vào nội dung
            reply.content = f"@{parent_comment.author.username} {form.cleaned_data['content']}"
            reply.save()
            return redirect('post_detail', post_id=post.id)
    return redirect('post_detail', post_id=post.id)
def delete_reply(request, post_id, reply_id):
    reply = get_object_or_404(Reply, id = reply_id)
    if request.user != reply.author:
        return HttpResponseForbidden("Ban khong co quyen xoa")
    reply.delete()
    return redirect('post_detail', post_id = post_id)
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id = comment_id, post_id = post_id)
    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Comment xoa thanh cong!")
    else:
        messages.error(request, "Ban khong co quyen xoa!")
    return redirect ('post_detail', post_id = post_id)
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id = comment_id, author = request.user)
    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            comment.content = new_content
            comment.save()
        return redirect("post_detail", post_id= post_id)
def edit_reply(request, post_id, reply_id):
    reply = get_object_or_404(Reply, id = reply_id, comment__post_id=post_id, author = request.user)
    if request.method == 'POST':
        new_reply = request.POST.get('content')
        if new_reply:
            reply.content = new_reply
            reply.save()
        return redirect("post_detail", post_id = post_id)


