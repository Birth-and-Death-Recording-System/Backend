from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import User, Birth, Death, DeathRecord, BirthRecord
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    ResetPasswordConfirmSerializer, BirthSerializer, DeathSerializer, DeathRecordSerializer, BirthRecordSerializer, \
    UserLoginSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from .models import ActionLog
from .serializers import ActionLogSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response(data={
                    'token': token.key,
                    'status': status.HTTP_200_OK,
                    'userData': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
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
@authentication_classes([TokenAuthentication])
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
        return Response({'count': item_count})


@api_view(['GET'])
def count_deaths(request):
    if request.method == 'GET':
        # Count the number of items in the database for YourModel
        item_count = Death.objects.count()

        # Return the count as JSON response
        return Response({'count': item_count})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
def birth_list(request):
    """
    List all births or create a new birth.
    """
    if request.method == 'GET':
        births = Birth.objects.all()
        serializer = BirthSerializer(births, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        try:
            if not request.data:
                return Response({'error': 'No births data provided'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = BirthSerializer(data=request.data)
            if serializer.is_valid():
                # Decide whether to use request.user or data provided in request
                user = request.user if request.user.is_authenticated else None
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
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
# @permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
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
@authentication_classes([TokenAuthentication])
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


@api_view(['GET'])
def birth_chart(request):
    births_data = Birth.objects.values('date').annotate(count=Count('date'))
    return JsonResponse(list(births_data), safe=False)


@api_view(['GET'])
def death_chart(request):
    deaths_data = Death.objects.values('date').annotate(count=Count('date'))
    return JsonResponse(list(deaths_data), safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.session.flush()

    # Invalidate token (if using token authentication)
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except Token.DoesNotExist:
        pass

    return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
