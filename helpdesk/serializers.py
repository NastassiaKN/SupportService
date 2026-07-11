from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    status = serializers.CharField(
        source='get_status_display',
        read_only=True,
    )
    priority = serializers.CharField(
        source='get_priority_display',
        read_only=True,
    )

    class Meta:
        model = Ticket
        fields = ['id',
                  'title',
                  'description',
                  'attachment',
                  'status',
                  'status_updated_at',
                  'created_at',
                  'priority',
                  'assigned_to',
                  ]
