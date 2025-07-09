from django.shortcuts import render, redirect
from user.forms import CustomRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login,logout

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
