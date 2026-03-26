from django.contrib import admin

from helpdesk.models import Ticket, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ('author', 'text', 'created_at', 'attachment')
    readonly_fields = ('created_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at', 'assigned_to', 'status', 'updated_at', 'attachment')
    search_fields = ('title', 'assigned_to__username', 'created_by__username')
    list_filter = ('status', 'assigned_to__username', 'created_at')
    ordering = ('-created_at',)
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket__title', 'author', 'created_at', 'attachment')
    search_fields = ('ticket__title', 'text', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)








