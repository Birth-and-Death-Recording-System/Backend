from django.urls import path

from api import views

urlpatterns = [
    path('signup/', views.signup, name='signup')
]
