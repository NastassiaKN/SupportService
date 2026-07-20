from rest_framework import serializers
from .models import Ticket, Message


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

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Message
        fields = ['id',
                  'author',
                  'text',
                  'attachment',
                  'created_at',]

class TicketDetailSerializer(serializers.ModelSerializer):
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
    messages = MessageSerializer(read_only=True, many=True)

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
                  'messages',]

class TicketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['title',
                  'description',
                  'attachment',]

class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['text',
                  'attachment',]

