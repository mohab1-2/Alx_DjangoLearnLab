from django import forms
from django.contrib.auth.models import User
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
                'required': True
            })
        }
        labels = {
            'content': 'Your Comment'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters long.")
        return content
