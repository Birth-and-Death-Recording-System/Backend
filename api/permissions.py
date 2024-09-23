from rest_framework.permissions import BasePermission


class IsDoctorOrNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Doctor', 'Nurse']


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Doctor']


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Nurse']
