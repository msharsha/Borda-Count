from django import forms

from .models import Post

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'options', 'allowed_users', 'deadline']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
            'deadline': DateInput()
        }
