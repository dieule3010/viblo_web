from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post
from .models import Category
from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'scheduled_date', 'view_post_link')
    list_filter = ('scheduled_date',) #lọc các bài viết theo lịch
    actions = ['approve_posts']  # Thêm hành động phê duyệt bài viết

    def get_queryset(self, request):
        queryset = super().get_queryset(request) #lấy dữ liệu từ csdl
        self.total_posts = queryset.count() #tính tổng bài viết tổng cộng
        self.approved_posts = queryset.filter(is_approved=True).count() #tính tổng bài đã duyệt
        self.pending_posts = queryset.filter(is_approved=False).count() # tính tổng bài chờ duyệt
        return queryset

    def changelist_view(self, request, extra_context=None):
        if not hasattr(self, 'total_posts'): # KIỂM TRA XEM POSTADMIN CÓ TOTALS POSTS HAY KH
            self.total_posts = 0
            self.approved_posts = 0
            self.pending_posts = 0

        extra_context = extra_context or {} # TRUYỀN DỮ LIỆU BỔ SUNG
        extra_context['total_posts'] = self.total_posts
        extra_context['approved_posts'] = self.approved_posts
        extra_context['pending_posts'] = self.pending_posts
        return super().changelist_view(request, extra_context=extra_context)

    def approve_posts(self, request, queryset):
        """ Phê duyệt các bài viết đã chọn """
        queryset.update(is_approved=True)
        self.message_user(request, "Các bài viết đã được phê duyệt.")

    approve_posts.short_description = "Phê duyệt các bài viết đã chọn"

    def view_post_link(self, obj):
        """ Tạo liên kết đến trang chi tiết bài viết """
        url = reverse('post_detail', args=[obj.id])
        return format_html('<a href="{}">Xem bài viết</a>', url)

    view_post_link.short_description = "Xem bài viết"

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
