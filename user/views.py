from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from user.forms import CustomRegisterForm, LoginForm, AssignedRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from events.models import Event
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()

            messages.success(request, 'A confirmation email was sent. Please check your email.')
            return redirect('sign-in')
    return render(request, 'registration/sign-up.html', {'form': form})
            

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request, 'registration/sign-in.html',{'form':form})

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect(sign_in)
    

def activate_user(request, user_id, token):
    try:
        user = get_object_or_404(User, id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
    


@user_passes_test(is_admin)
def assign_role(request, id):
    form = AssignedRoleForm()
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f'User {user.username} has been assigned to the {group.name} role.')
            return redirect('participant_list')
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})


@user_passes_test(is_admin)
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit = False)
            group.save()
            form.save_m2m()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form':form})

@user_passes_test(is_admin)
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    return render(request,'admin/group_list.html',{'groups':groups})

@user_passes_test(is_admin)
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group_name = group.name
    group.delete()
    messages.success(request, f'Group "{group_name}" has been deleted successfully.')
    return redirect('group-list')

@login_required
def user_dashboard(request):
    today = timezone.now().date()
    booked_events = Event.objects.filter(participants=request.user).order_by('date')
    return render(request, 'users/user_dashboard.html', {'booked_events': booked_events})

@login_required
def book_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.info(request, "You have unbooked the event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "Event booked successfully.")

    return redirect('home')

@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name='Organizer').exists():
        return redirect('dashboard')
    else:
        return redirect('user_dashboard')