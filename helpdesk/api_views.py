from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .autoassign_manager import get_available_manager
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer, TicketDetailSerializer, TicketCreateSerializer, MessageCreateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ticket_list_api(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ticket_detail_api(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    serializer = TicketDetailSerializer(ticket)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ticket_create_api(request):
    serializer = TicketCreateSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save(created_by=request.user, assigned_to=get_available_manager())
        response_serializer = TicketSerializer(ticket)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def message_create_api(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    if ticket.status == 'closed':
        return Response({"error" : "You cannot add messages to a closed ticket."},
                        status=status.HTTP_400_BAD_REQUEST,)
    serializer = MessageCreateSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save(ticket=ticket, author=request.user)
        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ticket_confirm_api(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    if ticket.status == 'resolved':
        ticket.status = 'closed'
        ticket.save()
    else:
        return Response({"error" : "Only resolved tickets can be confirmed."}, status=status.HTTP_400_BAD_REQUEST,)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ticket_close_api(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    if ticket.status in ['new', 'in_progress']:
        ticket.status = 'closed'
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if ticket.status == 'resolved':
        return Response({"error" : "Resolved tickets must be confirmed, not closed.",
                         "current_status": ticket.status}, status=status.HTTP_400_BAD_REQUEST,)

    if ticket.status == 'closed':
        return Response({"error" : "Ticket is already closed.", "current_status": ticket.status},
                        status=status.HTTP_400_BAD_REQUEST,)







