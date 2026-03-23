from django import forms
from .models import Ticket, Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'For example: Login page does not open',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the issue in detail...',
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Write your message...',
                'rows': 4,
            })
        }

