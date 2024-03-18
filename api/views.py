from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import User, Birth, Death, DeathRecord, BirthRecord
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    ResetPasswordConfirmSerializer, BirthSerializer, DeathSerializer, DeathRecordSerializer, BirthRecordSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from .models import ActionLog
from .serializers import ActionLogSerializer


# Create your views here.
@api_view(['POST'])
def login_user(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    auth_login(request, user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile = request.user.profile
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        current_password = request.data['current_password']
        repeat_password = request.data['repeat_password']
        new_password = request.data['new_password']

        user = request.user
        if current_password != repeat_password:
            return Response({'message': 'Current password and repeat password do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(current_password):
            return Response({'message': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successful.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_password_link = reverse(reset_password_confirm, kwargs={'uidb64': uidb64, 'token': token})

        context = {'reset_password_link': request.build_absolute_uri(reset_password_link)}
        text_content = render_to_string('reset_password_email.txt', context)
        html_content = render_to_string('email.html', context)

        msg = EmailMultiAlternatives(
            subject='Password Reset Request',
            body=text_content,
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Send email
        # send_mail(
        #     subject='Password Reset Request',
        #     from_email='app.debugmail.io',
        #     message=text_content,
        #     recipient_list=[email],
        #     fail_silently=False,
        #     html_message=html_content
        # )

        return Response({'message': 'Password reset email has been sent'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None

    if user and default_token_generator.check_token(user, token):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'success': 'Password reset successfully'}, status=200)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Invalid password reset link'}, status=400)


@api_view(['GET'])
def count_births(request):
    if request.method == 'GET':
        # Count the number of items in the database for YourModel
        item_count = Birth.objects.count()

        # Return the count as JSON response
        return Response({'Total Number of Births': item_count})


@api_view(['GET'])
def count_deaths(request):
    if request.method == 'GET':
        # Count the number of items in the database for YourModel
        item_count = Death.objects.count()

        # Return the count as JSON response
        return Response({'Total Number of Deaths': item_count})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def birth_list(request):
    """
    List all births or create a new birth.
    """
    if request.method == 'GET':
        births = Birth.objects.all()
        serializer = BirthSerializer(births, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BirthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def birth_detail(request, pk):
    """
    Retrieve, update or delete a birth instance.
    """
    try:
        birth = Birth.objects.get(pk=pk)
    except Birth.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BirthSerializer(birth)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BirthSerializer(birth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        birth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def death_list(request):
    """
    List all births or create a new birth.
    """
    if request.method == 'GET':
        deaths = Death.objects.all()
        serializer = DeathSerializer(deaths, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DeathSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def death_detail(request, pk):
    """
    Retrieve, update or delete a birth instance.
    """
    try:
        death = Death.objects.get(pk=pk)
    except Death.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeathSerializer(death)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DeathSerializer(death, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        death.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActionLogViewSet(viewsets.ModelViewSet):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer


class DeathRecordListCreateAPIView(generics.ListCreateAPIView):
    queryset = DeathRecord.objects.all()
    serializer_class = DeathRecordSerializer


class BirthRecordListCreateAPIView(generics.ListCreateAPIView):
    queryset = BirthRecord.objects.all()
    serializer_class = BirthRecordSerializer
