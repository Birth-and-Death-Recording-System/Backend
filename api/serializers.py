from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'role', 'gender']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'username', 'last_name', 'email', 'profile_pic', 'phone_number', 'gender',
                  'profile_pic', 'phone_number', 'gender', 'birth_date')
