from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('use-access-key/', views.use_access_key, name='use_access_key'),
    path('activity/', views.user_activity, name='activity'),
    path('reset-device/', views.reset_device_binding, name='reset_device'),
]