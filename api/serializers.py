from rest_framework import serializers
from .models import User, Profile, Birth, Death


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'role', 'gender']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'username', 'last_name', 'email', 'profile_pic', 'phone_number', 'gender',
                  'profile_pic', 'phone_number', 'gender', 'birth_date')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        repeat_password = attrs.get('repeat_password')
        new_password = attrs.get('new_password')
        if current_password:
            if current_password != repeat_password:
                raise serializers.ValidationError("Current password and repeat password do not match")

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class BirthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birth
        fields = '__all__'


class DeathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Death
        fields = '__all__'
