from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Ticket

class TicketConfirmAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="123qaz321zxc",
        )

        self.client.login(username="testuser", password="123qaz321zxc")

    def create_ticket(self, **kwargs):
        data = {
            "title": "test title",
            "description": "test description",
            "created_by": self.user,
            "status": "new",
        }
        data.update(kwargs)
        return Ticket.objects.create(**data)

    def test_confirm_resolved_ticket(self):
        ticket = self.create_ticket(
            status="resolved",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Closed")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

    def test_confirm_new_ticket(self):
        ticket = self.create_ticket(
            status="new",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Only resolved tickets can be confirmed.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "new")

    def test_confirm_in_progress_ticket(self):
        ticket = self.create_ticket(
            status="in_progress",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Only resolved tickets can be confirmed.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "in_progress")

    def test_confirm_closed_ticket(self):
        ticket = self.create_ticket(
            status="closed",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/confirm/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Only resolved tickets can be confirmed.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

class TicketCloseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser1",
            password="123qaz321wsx",
        )

        self.client.login(username="testuser1", password="123qaz321wsx")

    def create_ticket(self, **kwargs):
        data = {
            "title": "test title",
            "description": "test description",
            "created_by": self.user,
            "status": "new",
        }
        data.update(kwargs)
        return Ticket.objects.create(**data)

    def test_close_new_ticket(self):
        ticket = self.create_ticket(
            status="new",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Closed")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

    def test_close_in_progress_ticket(self):
        ticket = self.create_ticket(
            status="in_progress",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Closed")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

    def test_close_resolved_ticket(self):
        ticket = self.create_ticket(
            status="resolved",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Resolved tickets must be confirmed, not closed.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "resolved")

    def test_close_closed_ticket(self):
        ticket = self.create_ticket(
            status="closed",
        )

        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Ticket is already closed.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

    def test_close_ticket_from_another_user(self):
        User.objects.create_user(
            username="testuser2",
            password="123qaz321wsx123",
        )

        ticket = self.create_ticket(
            status="new",
        )

        self.client.login(username="testuser2", password="123qaz321wsx123")

        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "new")

    def test_close_ticket_unauthorized_user(self):
        ticket = self.create_ticket(
            status="new",
        )

        self.client.logout()
        response = self.client.post(f"/api/tickets/{ticket.id}/close/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "new")




