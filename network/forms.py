from django import forms
from .models import User, Post

class NewPostForm(forms.ModelForm):
    action = forms.CharField(initial='new_post', widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = ["post_text"]

        widgets = {
            'post_text': forms.Textarea(attrs={
                'class': 'form-post-textarea',
                'placeholder': "What's up?",
                'required': True,
                'rows': 4,
                'autofocus': True,
                'style': 'resize: none',
                'id': 'post-input-text'
            })
        }