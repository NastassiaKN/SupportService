import os

from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/tickets', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tickets', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    status_updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return self.title

    def status_ticket(self):
        return f'status-{self.status.replace('_', '-')}'

    def get_file_extension(self):
        if not self.attachment:
            return ''
        return os.path.splitext(self.attachment.name)[1].lower()

    def is_image(self):
        return self.get_file_extension() in ['.jpg', '.jpeg', '.png']

    def is_video(self):
        return self.get_file_extension() in ['.mp4']

    def is_document(self):
        return self.get_file_extension() in ['.pdf', '.doc', '.docx', '.txt']

    def attachment_filename(self):
        if not self.attachment:
            return ''
        return os.path.basename(self.attachment.name)

    def save(self, *args, **kwargs):
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            if old_ticket.status != self.status:
                self.status_updated_at = timezone.now()
        super().save(*args, **kwargs)

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True)
    attachment = models.FileField(upload_to='attachments/comments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.author.username} on ticket {self.ticket.title}'

    def get_file_extension(self):
        if not self.attachment:
            return ''
        return os.path.splitext(self.attachment.name)[1].lower()

    def is_image(self):
        return self.get_file_extension() in ['.jpg', '.jpeg', '.png']

    def is_video(self):
        return self.get_file_extension() in ['.mp4']

    def is_document(self):
        return self.get_file_extension() in ['.pdf', '.doc', '.docx', '.txt']

    def attachment_filename(self):
        if not self.attachment:
            return ''
        return os.path.basename(self.attachment.name)






