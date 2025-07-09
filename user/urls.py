from django.urls import path
from django.views.generic import RedirectView
from user.views import sign_up, sign_in
urlpatterns = [
    path('sign-up/',sign_up, name="sign-up"),
    path('sign-in/',sign_in, name="sign-in"),
    
    
]
