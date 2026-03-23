from django.urls import path
from .views import (ticket_create, ticket_list, ticket_detail)

urlpatterns = [
    path('ticket_create/', ticket_create, name='ticket_create'),
    path('', ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>',ticket_detail, name='ticket_detail'),
]