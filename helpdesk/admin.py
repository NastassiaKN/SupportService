from django.contrib import admin

from helpdesk.models import Ticket, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('author', 'text', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at', 'assigned_to', 'status', 'updated_at')
    search_fields = ('title', 'assigned_to__username', 'created_by__username')
    list_filter = ('status', 'assigned_to__username', 'created_at')
    ordering = ('-created_at',)
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket__title', 'author', 'created_at')
    search_fields = ('ticket__title', 'text', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)








