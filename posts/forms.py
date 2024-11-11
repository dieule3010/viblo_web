# posts/forms.py
from django import forms
from .models import Post
from .models import Comment
from. models import Tag
from. models import Category


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Chọn danh mục",
        label="Danh mục"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']  # Bao gồm trường image
class CategoryForm(forms.ModelForm):
    pass
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter your comment...',
        'rows': 3,
        'class': 'form-control',
    }))

    class Meta:
        model = Comment
        fields = ['content']
