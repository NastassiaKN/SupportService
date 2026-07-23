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

class TicketListAPITest(APITestCase):
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

    def test_list_tickets(self):
        another_user = User.objects.create_user(
            username="another_user1",
            password="password123",
        )

        ticket = self.create_ticket(
            status="new",
        )
        second_ticket = self.create_ticket(
            status="new",
        )

        ticket_from_another_user = self.create_ticket(
            status="new",
            created_by=another_user,
        )

        response = self.client.get(f"/api/tickets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket_ids = [ticket["id"] for ticket in response.data]
        self.assertIn(ticket.id, ticket_ids)
        self.assertIn(second_ticket.id, ticket_ids)
        self.assertNotIn(ticket_from_another_user.id, ticket_ids)

    def test_list_unauthorized_user(self):
        ticket = self.create_ticket(
            status="new",
        )

        self.client.logout()
        response = self.client.get(f"/api/tickets/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

class TicketDetailAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser1",
            password="password123",
        )

        self.client.login(username="testuser1", password="password123")

    def create_ticket(self, **kwargs):
        data = {
            "title": "test title detail",
            "description": "test description detail",
            "created_by": self.user,
            "status": "new",
        }

        data.update(kwargs)
        return Ticket.objects.create(**data)

    def test_detail_ticket(self):
        ticket = self.create_ticket()

        response = self.client.get(f"/api/tickets/{ticket.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ticket.id, response.data["id"])
        self.assertEqual(ticket.title, response.data["title"])
        self.assertEqual(ticket.description, response.data["description"])

    def test_detail_from_another_user(self):
        another_user = User.objects.create_user(
            username="another_user1",
            password="password123",
        )
        ticket = self.create_ticket()

        self.client.login(username="another_user1", password="password123")
        response = self.client.get(f"/api/tickets/{ticket.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_non_existent_ticket(self):
        ticket = self.create_ticket()
        nonexistent_ticket_id = ticket.id + 1
        response = self.client.get(f"/api/tickets/{nonexistent_ticket_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_detail_unauthorized_user(self):
        ticket = self.create_ticket()
        self.client.logout()
        response = self.client.get(f"/api/tickets/{ticket.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)







