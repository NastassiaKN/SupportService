from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

from helpdesk.models import Ticket, Message
from django.urls import reverse

class TicketTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123!@',
        )

    def test_create_ticket(self):
        ticket = Ticket.objects.create(
            title='create ticket',
            description='description create ticket',
            created_by=self.user,
        )

        self.assertEqual(ticket.title, 'create ticket')
        self.assertEqual(ticket.description, 'description create ticket')
        self.assertEqual(ticket.created_by, self.user)

    def test_create_message(self):
        ticket = Ticket.objects.create(
            title='for create message',
            description='for create message',
            created_by=self.user,
        )

        message = Message.objects.create(
            ticket=ticket,
            author=self.user,
            text='Hello world!',
        )

        self.assertEqual(message.text, 'Hello world!')
        self.assertEqual(message.ticket, ticket)
        self.assertEqual(message.author, self.user)

    def test_no_message_for_closed_ticket(self):
        ticket = Ticket.objects.create(
            title='for closed ticket',
            description='for closed ticket',
            created_by=self.user,
            status='closed',
        )

        if ticket.status != 'closed':
            Message.objects.create(
                ticket=ticket,
                author=self.user,
                text='Can not be created',
            )

        messages = Message.objects.filter(ticket=ticket)
        self.assertEqual(messages.count(), 0)


class TicketManagerTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser2',
            password='tester2!@',
        )

        self.client.login(username='testuser2', password='tester2!@')

        group = Group.objects.create(name='Support Managers')
        self.manager = User.objects.create_user(
            username='manager1',
            password='manager1!@',
            is_staff=True,
        )
        self.manager.groups.add(group)

    def test_auto_assign_manager(self):
        self.client.post(
            reverse('ticket_create'),
            data={
                'title': 'create ticket',
                'description': 'description create ticket',
            },
            created_by=self.user,
        )

        ticket = Ticket.objects.first()

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.assigned_to, self.manager)

class TicketAdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123!@',
        )

    def test_admin_assign_manager(self):
        manager = User.objects.create_user(
            username='manager2',
            password='manager2!@',
            is_staff=True,
        )

        ticket = Ticket.objects.create(
            title='for assign manager by admin',
            description='description assign manager by admin',
            created_by=self.user,
            assigned_to=manager,
        )

        self.assertEqual(ticket.assigned_to, manager)