from django import forms
from .models import Ticket, Message

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

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Write your message...',
                'rows': 2,
            })
        }




