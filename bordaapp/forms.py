from django import forms
from django.forms import widgets

from .models import Post, Submission

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

class PostSubmitForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['options','preferences']