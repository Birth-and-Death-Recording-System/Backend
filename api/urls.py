from django.urls import path

from api import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.user_profile, name='profile'),
]
