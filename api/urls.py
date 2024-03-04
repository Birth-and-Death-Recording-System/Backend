from django.urls import path

from api import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset-password/confirm/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
    path('count-items/', views.count_items, name='count_items'),
]



