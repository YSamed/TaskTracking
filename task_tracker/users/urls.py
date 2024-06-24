from django.urls import path
from django.contrib.auth import views as auth_views
from.import views

app_name = 'users'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', views.signup, name='signup'), 
    path('profile/', views.view_profile, name='view_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),  
    path('profile/change-password/', views.change_password, name='change_password'), 
]
