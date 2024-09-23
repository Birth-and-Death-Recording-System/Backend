from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Profile, Birth, Death, DeathRecord, BirthRecord
from .models import ActionLog
import re
from .messages import (
    PASSWORD_TOO_SHORT, PASSWORD_UPPERCASE, PASSWORD_LOWERCASE,
    PASSWORD_NUMBER, PASSWORD_SPECIAL, EMAIL_EXISTS, USERNAME_EXISTS,
    ROLE_REQUIRED, GENDER_REQUIRED
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password', 'email', 'username', 'role', 'gender']

    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError(PASSWORD_TOO_SHORT)
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(PASSWORD_UPPERCASE)
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(PASSWORD_LOWERCASE)
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(PASSWORD_NUMBER)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(PASSWORD_SPECIAL)
        return value

    def validate_email(self, value):
        """Ensure the email address is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_EXISTS)
        return value

    def validate_username(self, value):
        """Ensure the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(USERNAME_EXISTS)
        return value

    def validate(self, data):
        """Custom validation for the overall data."""
        if 'role' not in data:
            raise serializers.ValidationError(ROLE_REQUIRED)
        if 'gender' not in data:
            raise serializers.ValidationError(GENDER_REQUIRED)
        return data

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data['role'], gender=validated_data['gender']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'username', 'last_name', 'email', 'phone_number', 'gender',
                  'phone_number', 'gender', 'birth_date')

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        # Make all fields optional if it's an update (PUT request)
        if self.instance:
            for field in self.fields:
                self.fields[field].required = False


    def validate_phone_number(self, value):
        """
        Optionally, you can validate the phone number format to ensure it's valid.
        Here, we are assuming phone numbers start with a '0' and are numeric.
        """
        if not value.startswith('0'):
            raise serializers.ValidationError("Phone number should start with '0'.")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number should contain only digits.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, max_length=255)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):

        request = self.context.get('request')
        user = request.user

        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})

        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "New password cannot be the same as the current password."})

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
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

    def __init__(self, *args, **kwargs):
        super(DeathSerializer, self).__init__(*args, **kwargs)
        # Make all fields optional if it's an update (PUT request)
        if self.instance:
            for field in self.fields:
                self.fields[field].required = False


class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'


class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = ['id', 'recorder', 'recorded_at', 'action_type', 'details']


class BirthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = ['id', 'recorder', 'recorded_at', 'action_type', 'details']
