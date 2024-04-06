from django.urls import path, include

from api import views
from rest_framework.routers import DefaultRouter
from .views import ActionLogViewSet, DeathRecordListCreateAPIView, BirthRecordListCreateAPIView

router = DefaultRouter()
router.register(r'action-logs', ActionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset-password/confirm/<uidb64>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
    path('count-births/', views.count_births, name='count_births'),
    path('count-deaths/', views.count_deaths, name='count_deaths'),
    path('births/', views.birth_list, name='births'),
    path('births/<int:pk>/', views.birth_detail, name='birth_detail'),
    path('deaths/', views.death_list, name='deaths'),
    path('deaths/<int:pk>/', views.death_detail, name='death_detail'),
    path('death-records/', DeathRecordListCreateAPIView.as_view(), name='death_record_list_create'),
    path('birth-records/', BirthRecordListCreateAPIView.as_view(), name='birth_record_list_create'),
    path('birth-chart/', views.birth_chart, name='birth_chart'),
    path('death-chart/', views.death_chart, name='death_chart'),
    path('logout/', views.logout, name='logout'),

]
