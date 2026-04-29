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
                'maxlength': 2000,
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
                'maxlength': 1000,
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        attachment = cleaned_data.get('attachment')

        if not text and not attachment:
            raise forms.ValidationError('You must enter either a text or an attachment')
        return cleaned_data

class TicketAdminForm(forms.ModelForm):
    new_message_text = forms.CharField(
        required=False,
        label='New message',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'style': 'width: 100%; min-height: 140px;',
            'placeholder': 'Write your message...'
        })
    )

    new_message_attachment = forms.FileField(
        required=False,
        label='Attachment',
    )

    class Meta:
        model = Ticket
        fields = '__all__'
