from django.urls import path
from user.views import sign_up, sign_in, sign_out , activate_user,create_group,group_list,delete_group, assign_role ,book_event, user_dashboard,dashboard_redirect

urlpatterns = [
    path('sign-up/',sign_up, name="sign-up"),
    path('sign-in/',sign_in, name="sign-in"),
    path('sign-out/',sign_out, name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('create-group/', create_group, name='create-group'),
    path('groups/', group_list, name='group-list'),
    path('groups/delete/<int:id>/', delete_group, name='delete-group'),
    path('participants/<int:id>/assign-role/', assign_role, name='assigned-role'),
    path('book/<int:id>/', book_event, name='book_event'),
    path('dashboard-redirect/', dashboard_redirect, name='dashboard-redirect'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    
]
