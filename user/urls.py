from django.urls import path
from user.views import sign_up , activate_user,dashboard_redirect, CustomLoginView, AssignRoleView, CreateGroupView, GroupListView, DeleteGroupView, BookEvent, UserDashboardView, ProfileView, EditProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

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
    path('profile/',ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit-profile'),
    path('password-change/', ChangePassword.as_view(
        template_name = 'accounts/password_change.html'), name = 'password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name = 'accounts/password_change_done.html'), name = 'password_change_done'),
    path('password-reset', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
