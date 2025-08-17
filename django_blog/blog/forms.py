from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from taggit.forms import TagField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

class TagWidget(forms.TextInput):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'tag-widget', 'placeholder': 'Add tags...'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

class PostForm(forms.ModelForm):
    tags = TagField(
        widget=TagWidget(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write you content here ...'})
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
