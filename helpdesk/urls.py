from django.urls import path
from .views import (ticket_create, ticket_list, ticket_detail, ticket_confirm_resolved, ticket_closed)
from .api_views import (ticket_list_api, ticket_detail_api, ticket_create_api, message_create_api, ticket_confirm_api,
                        ticket_close_api)

urlpatterns = [
    path('ticket_create/', ticket_create, name='ticket_create'),
    path('tickets/', ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>',ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/confirm-resolved/', ticket_confirm_resolved, name='ticket_confirm_resolved'),
    path('ticket/<int:ticket_id>/closed/', ticket_closed, name='ticket_closed'),
    path('api/tickets/', ticket_list_api, name='ticket_list_api'),
    path('api/tickets/<int:ticket_id>/',ticket_detail_api, name='ticket_detail_api'),
    path('api/tickets/create/', ticket_create_api, name='ticket_create_api'),
    path('api/tickets/<int:ticket_id>/messages/', message_create_api, name='message_create_api'),
    path('api/tickets/<int:ticket_id>/confirm/', ticket_confirm_api, name='ticket_confirm_api'),
    path('api/tickets/<int:ticket_id>/close/', ticket_close_api, name='ticket_close_api'),
]