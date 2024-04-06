from rest_framework import serializers
from .models import User, Profile, Birth, Death, DeathRecord, BirthRecord
from .models import ActionLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'role', 'gender']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'username', 'last_name', 'email', 'phone_number', 'gender',
                  'phone_number', 'gender', 'birth_date')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, max_length=255)
    repeat_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        repeat_password = attrs.get('repeat_password')
        new_password = attrs.get('new_password')
        if current_password and current_password != repeat_password:
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
