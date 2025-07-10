from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q, Prefetch, Sum
from django.utils import timezone
from events.models import Event, Participant, Catagory
from events.forms import EventForm, ParticipantForm, CatagoryForm
from django.contrib import messages
from django.db import models

def home(request):
    upcoming_events = (
        Event.objects.filter(date__gte=timezone.now().date())
        .select_related('category')
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants'))
        .order_by('date')
    )
    return render(request, 'home.html', {
        'upcoming_events': upcoming_events,
    })

def base(request):
    return render(request, "base.html")

def footer(request):
    return render(request, "footer.html")

def dashboard(request):
    today = timezone.now().date()
    filter_option = request.GET.get('filter')

    events_data = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gt=today)),
        past_events=Count('id', filter=Q(date__lt=today))
    )

    filtered_events = (Event.objects.select_related('category')
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants'))
    )

    filter_map = {
        'all': (filtered_events, 'All Events'),
        'upcoming': (filtered_events.filter(date__gt=today), 'Upcoming Events'),
        'past': (filtered_events.filter(date__lt=today), 'Past Events'),
    }
    filtered_events, header = filter_map.get(filter_option, (filtered_events.filter(date=today), "Today’s Events"))

    context = {
        'total_participants': Participant.objects.count(),
        'total_events': events_data['total_events'],
        'upcoming_events': events_data['upcoming_events'],
        'past_events': events_data['past_events'],
        'filtered_events': filtered_events,
        'header': header,
    }
    return render(request, 'dashboard.html', context)

def event_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    events = (
        Event.objects.select_related('category')
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants'))
    )

    if query:
        events = events.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

    if category_id:
        events = events.filter(category__id=category_id)

    if date_from and date_to:
        events = events.filter(date__range=[date_from, date_to])

    categories = Catagory.objects.all()

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'query': query,
    })

def event_detail(request, id):
    event = get_object_or_404(
        Event.objects.select_related('category')
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants')),
        id=id
    )
    return render(request, 'event_detail.html', {'event': event})

def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()

        selected_participants = form.cleaned_data.get('participants', [])
        current_participants = Participant.objects.filter(events=event)

        for participant in current_participants:
            if participant not in selected_participants:
                participant.events.remove(event)

        for participant in selected_participants:
            if participant not in current_participants:
                participant.events.add(event)

        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})


def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()

        selected_participants = form.cleaned_data.get('participants', [])
        current_participants = Participant.objects.filter(events=event)

        for participant in current_participants:
            if participant not in selected_participants:
                participant.events.remove(event)

        for participant in selected_participants:
            if participant not in current_participants:
                participant.events.add(event)

        return redirect('event_detail', id=id)
    return render(request, 'events/event_form.html', {'form': form})



def event_delete(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        event.delete()

        messages.success(request, "Event deleted successfully.")
        return redirect('dashboard')

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('participant_list')
    return render(request, 'participants/participant_form.html', {'form': form})

def participant_delete(request, id):
    if request.method == "POST":
        participant = get_object_or_404(Participant, id=id)
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
    return redirect('participant_list')

def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participants/participant_list.html', {'participants': participants})

def category_create(request):
    form = CatagoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'categories/category_form.html', {'form': form})

def delete_catagory(request, id):
    cat = get_object_or_404(Catagory, id=id)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')

def category_list(request):
    categories = Catagory.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})