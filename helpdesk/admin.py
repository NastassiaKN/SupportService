from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html_join, format_html
from typing import Any

from helpdesk.models import Ticket, Message
from django.contrib.auth.models import Group, User
from helpdesk.forms import TicketAdminForm

class SupportManagerFilter(admin.SimpleListFilter):
    title = 'Support managers'
    parameter_name = 'assigned_to'

    def lookups(self, request, model_admin):
        support_group = Group.objects.get(name='Support Managers')
        managers = support_group.user_set.filter(is_active=True)
        return [(manager.id, manager.username) for manager in managers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(assigned_to=self.value())
        return queryset

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'priority', 'status', 'assigned_to', 'created_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('status', 'priority', 'assigned_to__username', 'created_at')
    ordering = ('-created_at',)
    form = TicketAdminForm
    readonly_fields = ('created_at', 'updated_at', 'status_updated_at', 'chat_history', 'attachment_preview', 'created_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(Q(assigned_to=request.user))

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        if obj:
            readonly.append('created_by')

        if not request.user.is_superuser:
            readonly.append('assigned_to')

        if obj and not obj.created_by.is_staff:
            readonly.extend(['title', 'description', 'attachment'])

        return readonly

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return 'status', 'priority', SupportManagerFilter, 'created_at'
        return 'status', 'priority', 'created_at'

    def get_exclude(self, request, obj=None):
        exclude = list(super().get_exclude(request, obj) or [])
        if obj is None:
            exclude.append('created_by')
        return exclude

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user

        if not obj.pk and not request.user.is_superuser:
            obj.assigned_to = request.user

        super().save_model(request, obj, form, change)

        new_message_text = form.cleaned_data.get('new_message_text')
        new_message_attachment = form.cleaned_data.get('new_message_attachment')

        if obj.status != 'closed' and (new_message_text or new_message_attachment):
            Message.objects.create(
                ticket=obj,
                author=request.user,
                text=new_message_text or '',
                attachment=new_message_attachment
            )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assigned_to':
            try:
                support_group = Group.objects.get(name='Support Managers')
                kwargs['queryset'] = User.objects.filter(groups=support_group, is_active=True)
            except Group.DoesNotExist:
                kwargs['queryset'] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets : list[tuple[str, dict[str, Any]]] = [
            ('Ticket information', {
                'fields': (
                    'title',
                    'description',
                    'attachment',
                    'attachment_preview',
                    'created_at',
                    'created_by',
                    'status',
                    'priority',
                    'status_updated_at',
                    'assigned_to',
                    'updated_at',
                )
            }),
            ('Chat history', {
                'fields': (
                    'chat_history',
                )
            }),
        ]
        if not obj or obj.status != 'closed':
            fieldsets.append(
                ('Add new message', {
                    'fields': (
                        'new_message_text',
                        'new_message_attachment',
                    )
                }),
            )
        return fieldsets

    def chat_history(self, obj):
        messages = obj.messages.all().order_by('created_at')

        if not messages:
            return 'No messages yet'

        return format_html_join(
            '',
            '''
                    <div style="width: 100%;max-width: 100%;min-height: 70px;margin-bottom:12px; padding:12px; 
                        border:1px solid #e2e8f0; border-radius:8px;box-sizing: border-box;">
                        <strong>{}</strong><br>
                        <small>{}</small>
                        <div style="margin-top:8px; white-space:pre-wrap;overflow-wrap: break-word;
                            word-break: break-word;">{}</div>
                        {}
                    </div>
                    ''',
            (
            (
                message.author.username,
                message.created_at.strftime('%d.%m.%Y %H:%M'),
                message.text or '',
                self.message_attachment_preview(message)
            )
                for message in messages
            )
        )
    chat_history.short_description = 'Chat history'

    def attachment_preview(self, obj):
        if not obj.attachment:
            return '-'

        url = obj.attachment.url
        name = obj.attachment.name.lower()

        if name.endswith(('.jpg', '.jpeg', '.png')):
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width:160px; max-height:160px; border-radius:8px;">'
                '</a>',
                url, url
            )

        if name.endswith(('.mp4',)):
            return format_html(
                '<video controls style="max-width:240px; max-height:160px; border-radius:8px;">'
                '<source src="{}">'
                'Your browser does not support the video tag.'
                '</video>',
                url
            )

        return '-'

    attachment_preview.short_description = 'Attachment preview'

    def message_attachment_preview(self, message):
        if not message.attachment:
            return ''

        url = message.attachment.url
        name = message.attachment.name.lower()

        if name.endswith(('.jpg', '.jpeg', '.png')):
            return format_html(
                '<br><a href="{}" target="_blank">'
                '<img src="{}" style="max-width:160px; max-height:160px; border-radius:8px; margin-top:8px;">'
                '</a>',
                url, url
            )

        if name.endswith(('.mp4',)):
            return format_html(
                '<br><video controls style="max-width:240px; max-height:160px; border-radius:8px; margin-top:8px;">'
                '<source src="{}">'
                '</video>',
                url
            )

        return format_html(
            '<br><a href="{}" target="_blank" style="margin-top:8px; display:inline-block;">📄 {}</a>',
        url,
        name
        )