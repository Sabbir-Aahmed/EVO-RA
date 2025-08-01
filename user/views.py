from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from user.forms import CustomRegisterForm, LoginForm, AssignedRoleForm, CreateGroupForm, EditProfileForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from events.models import Event
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView, LoginView ,PasswordResetView, PasswordResetConfirmView
from django.views.generic import FormView, CreateView, ListView, DeleteView, TemplateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model

User = get_user_model()


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
            
'''
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request, 'registration/sign-in.html',{'form':form})
'''

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_rul(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
    

def activate_user(request, user_id, token):
    try:
        user = get_object_or_404(User, id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()

            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
    

'''
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
'''

class AssignRoleView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignedRoleForm

    def test_func(self):
        return is_admin(self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('participant_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user_obj = get_object_or_404(User, id=self.kwargs['id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user_obj
        return context
    
    def form_valid(self, form):
        group = form.cleaned_data['role']
        self.user_obj.groups.clear()
        self.user_obj.groups.add(group)
        messages.success(self.request, f'User {self.user_obj.username} has been assigned to the {group.name} role.')
        return super().form_valid(form)
'''
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
'''

class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model =Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')

    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Group {self.object.name} has been created successfully')
        return response
    

'''
@user_passes_test(is_admin)
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    return render(request,'admin/group_list.html',{'groups':groups})
'''


class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name ='admin/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        return is_admin(self.request.user)
    
    def get_queryset(self):
        queryset = Group.objects.prefetch_related('permissions').all()
        return queryset

'''
@user_passes_test(is_admin)
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group_name = group.name
    group.delete()
    messages.success(request, f'Group "{group_name}" has been deleted successfully.')
    return redirect('group-list')
'''

class DeleteGroupView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    context_object_name = 'group'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('group-list')

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        group_name = self.object.name
        self.object.delete()
        messages.success(request, f'Group "{group_name}" has been deleted successfully.')
        return redirect(self.success_url)

    
'''
@login_required
def user_dashboard(request):
    booked_events = (
        Event.objects
        .filter(participants=request.user)
        .prefetch_related('participants')
        .order_by('date')
    )
    return render(request, 'user_dashboard.html', {'booked_events': booked_events})
'''

class UserDashboardView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'user_dashboard.html'
    context_object_name = 'booked_events'

    def get_queryset(self):
        return (
            Event.objects
            .filter(participants=self.request.user)
            .prefetch_related('participants')
            .order_by('date')
        )
    
    
'''
@login_required
def book_event(request, id):
    event = get_object_or_404(Event, id=id)

    if not request.user.groups.filter(name='Participant').exists():
        messages.error(request, "Only participants are allowed to book events.")
        return redirect('home')

    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.info(request, "You have unbooked the event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "Event booked successfully.")

    return redirect('home')
'''


class BookEvent(LoginRequiredMixin, View):
    def post(self, request, id):
        event = get_object_or_404(Event, id=id)

        if not request.user.groups.filter(name='Participant').exists():
            messages.error(request, "Only participants are allowed to book events.")
            return redirect('home')

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

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name ='accounts/profile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['profile_image'] = user.profile_image
        context['phone_number'] = user.phone_number
        context['bio'] = user.bio
        context['location'] = user.location
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        return super().form_valid(form)


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm