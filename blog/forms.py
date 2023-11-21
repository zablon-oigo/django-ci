from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']

class SearchForm(forms.Form):
    query=forms.CharField()