from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from events.models import Event, Catagory 
from events.forms import EventForm, CatagoryForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from user.views import is_admin

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

@login_required
def home(request):
    upcoming_events = (
        Event.objects
        .filter(date__gte=timezone.now().date())
        .select_related('category') 
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants'))
        .order_by('date') 
    )

    is_participant = request.user.groups.filter(name='Participant').exists()

    return render(request, 'home.html', {
        'upcoming_events': upcoming_events,
        'is_participant': is_participant,
    })

def base(request):
    return render(request, "base.html")


def footer(request):
    return render(request, "footer.html")

@user_passes_test(is_admin_or_organizer)
def adminAndOrganizerDashboard(request):
    today = timezone.now().date()
    filter_option = request.GET.get('filter')

    events_data = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gt=today)),
        past_events=Count('id', filter=Q(date__lt=today))
    )

    total_participants = User.objects.filter(events__isnull=False).distinct().count()

    filtered_events = (
        Event.objects.select_related('category')
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
        'total_events': events_data['total_events'],
        'upcoming_events': events_data['upcoming_events'],
        'past_events': events_data['past_events'],
        'total_participants': total_participants,
        'filtered_events': filtered_events,
        'header': header,
    }
    return render(request, 'dashboard.html', context)

@login_required
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

@login_required
def event_detail(request, id):
    event = get_object_or_404(
        Event.objects.select_related('category')
        .prefetch_related('participants')
        .annotate(participant_count=Count('participants')),
        id=id
    )
    return render(request, 'event_detail.html', {'event': event})


@user_passes_test(is_admin_or_organizer)
def event_create(request):
    form = EventForm(request.POST, request.FILES)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()

        selected_participants = form.cleaned_data.get('participants', [])
        event.participants.set(selected_participants)

        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})


@user_passes_test(is_admin_or_organizer)
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        event = form.save(commit=False)
        event.save()

        selected_participants = form.cleaned_data.get('participants', [])
        event.participants.set(selected_participants)

        return redirect('event_detail', id=id)
    return render(request, 'events/event_form.html', {'form': form})



@user_passes_test(is_admin_or_organizer)
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        event.delete()

        messages.success(request, "Event deleted successfully.")
        return redirect('dashboard')


@user_passes_test(is_admin)
def participant_delete(request, id):
    participant = get_object_or_404(User, id=id)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
    return redirect('participant_list')


@user_passes_test(is_admin)
def participant_list(request):
    participants = User.objects.all()
    return render(request, 'participants/participant_list.html', {'participants': participants})


@user_passes_test(is_admin_or_organizer)
def category_create(request):
    form = CatagoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'categories/category_form.html', {'form': form})


@user_passes_test(is_admin_or_organizer)
def delete_catagory(request, id):
    cat = get_object_or_404(Catagory, id=id)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')


@user_passes_test(is_admin_or_organizer)
def category_list(request):
    categories = Catagory.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})