from django.urls import path
from user.views import sign_up , activate_user,dashboard_redirect, CustomLoginView, AssignRoleView, CreateGroupView, GroupListView, DeleteGroupView, BookEvent, UserDashboardView, ProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('sign-up/',sign_up, name="sign-up"),
    path('sign-in/', CustomLoginView.as_view() , name='sign-in'),
    path('sign-out/',LogoutView.as_view(), name="sign-out"),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/delete/<int:id>/', DeleteGroupView.as_view(), name='delete-group'),
    path('participants/<int:id>/assign-role/', AssignRoleView.as_view(), name='assigned-role'),
    path('book/<int:id>/', BookEvent.as_view(), name='book_event'),
    path('dashboard-redirect/', dashboard_redirect, name='dashboard-redirect'),
    path('user-dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('profile/',ProfileView.as_view(), name='profile')
    
]
