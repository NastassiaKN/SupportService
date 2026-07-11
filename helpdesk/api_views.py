from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ticket_list_api(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

