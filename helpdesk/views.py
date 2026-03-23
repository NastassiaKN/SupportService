from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Ticket, Comment

from helpdesk.forms import TicketForm, CommentForm

User = get_user_model()

def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = 'new'
            ticket.save()
            return redirect('/')
    else:
        form = TicketForm()

    return render(request, 'ticket_create.html', {'form': form})

def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'ticket_list.html', {'tickets': tickets})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comments = Comment.objects.filter(ticket_id=ticket_id)
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.ticket = ticket
            comment.save()
            return redirect(referer)

    else:
        form = CommentForm()

    context = {
        'ticket': ticket,
        'comments': comments,
        'form': form,
    }

    return render(request, 'ticket_detail.html', context)






