from django.shortcuts import render

def non_logged_home(request):
    return render(request, 'non-logged-home.html')
