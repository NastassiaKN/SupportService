from django.contrib import admin
from django.db.models import Q

from helpdesk.models import Ticket, Message
from django.contrib.auth.models import Group, User

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

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)
    exclude = ('author',)
    can_delete = False

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'priority', 'status', 'assigned_to', 'created_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('status', 'priority', 'assigned_to__username', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'status_updated_at')
    inlines = [MessageInline]

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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            if not instance.pk:
                instance.author = request.user
            instance.save()
        formset.save_m2m()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assigned_to':
            try:
                support_group = Group.objects.get(name='Support Managers')
                kwargs['queryset'] = User.objects.filter(groups=support_group, is_active=True)
            except Group.DoesNotExist:
                kwargs['queryset'] = User.objects.none()
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
