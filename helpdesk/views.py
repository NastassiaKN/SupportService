from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from .models import Ticket, Message

from .forms import TicketForm, MessageForm
from .autoassign_manager import *

User = get_user_model()

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.assigned_to = get_available_manager()
            ticket.status = 'new'
            ticket.save()
            return redirect('/tickets/')
    else:
        form = TicketForm()

    return render(request, 'ticket_create.html', {'form': form})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    messages = Message.objects.filter(ticket_id=ticket_id)
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        if ticket.status == 'closed':
            return redirect(referer)

        form = MessageForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.ticket = ticket
            message.save()
            return redirect(referer)

    else:
        form = MessageForm()

    context = {
        'ticket': ticket,
        'messages': messages,
        'form': form,
    }

    return render(request, 'ticket_detail.html', context)

@login_required
@require_POST
def ticket_confirm_resolved(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    if ticket.status == 'resolved':
        ticket.status = 'closed'
        ticket.save()
    return redirect(f'/ticket/{ticket_id}')

@login_required
@require_POST
def ticket_closed(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    if ticket.status == 'new' or ticket.status == 'in_progress':
        ticket.status = 'closed'
        ticket.save()
    return redirect(f'/ticket/{ticket_id}')

def home_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('/login/')

    if user.is_staff:
        return redirect('/admin/')

    return redirect('/tickets/')



