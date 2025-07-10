from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from user.forms import CustomRegisterForm, LoginForm, AssignedRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch

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
    

def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users :
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'dashboard.html', {'users': users})


def assigned_role(request, id):
    form = AssignedRoleForm()
    user = get_object_or_404(User, id=id)  # safer than User.objects.get()

    if request.method == 'POST':
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'{user.username} has been assigned to the {role.name} role.')
            return redirect('dashboard')

    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {'form':form})

def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    return render(request,'admin/group_list.html',{'groups':groups})

def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group_name = group.name
    group.delete()
    messages.success(request, f'Group "{group_name}" has been deleted successfully.')
    return redirect('group-list')