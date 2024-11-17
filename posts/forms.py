# posts/forms.py
from django import forms
from .models import Post
from .models import Comment
from. models import Tag
from. models import Category

choices = [('coding', 'coding'), ('entertainment', 'entertainment'), ('music', 'music')]
# choices = Category.objects.all().values_list('name','name')
class PostForm(forms.ModelForm):
    category = forms.Select(choices= choices, attrs={'class': 'form-control'}),
    tags = forms.CharField(
        max_length=255,
        required=False,
        label="Tags",
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags, separated by commas'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']
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
