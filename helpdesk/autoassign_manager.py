from django.contrib.auth.models import Group, User
from django.db.models import Q, Count

def get_available_manager():
    try:
        support_group = Group.objects.get(name='Support Managers')
    except Group.DoesNotExist:
        return None

    managers = User.objects.filter(groups=support_group,
                                   is_active=True,
                                   is_staff=True,
    ).annotate(active_tickets_count=Count('assigned_tickets',
                                          filter=Q(assigned_tickets__status__in=['new', 'in_progress']))
    ).order_by('active_tickets_count', 'id')

    return managers.first()