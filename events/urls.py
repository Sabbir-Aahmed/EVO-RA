from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from events.views import home,footer,base,dashboard,event_detail,event_list,event_create,event_update,event_delete,participant_create,category_create,category_list,participant_list
urlpatterns = [
    path('home/',home, name="home"),
    path('base/',base),
    path('footer/',footer),
    path('dashboard/',dashboard, name="dashboard"),
    path('events/<int:id>/', event_detail, name='event_detail'),
    path('events/',event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:id>/update/',event_update, name='event_update'),
    path('events/<int:id>/delete/',event_delete, name='event_delete'),
    path('participants/create/', participant_create, name='participant_create'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/', category_list, name='category_list'),
    path('participants/', participant_list, name='participant_list'),
    
]
