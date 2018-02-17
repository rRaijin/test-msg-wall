from django import forms
from .models import Message, Comment


class AddMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']