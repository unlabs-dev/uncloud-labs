from django import forms
from .models import Issue, Comment


class IssueForm(forms.ModelForm):
    """Form for creating and editing issues."""

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to issues."""

    class Meta:
        model = Comment
        fields = ['author_name', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
