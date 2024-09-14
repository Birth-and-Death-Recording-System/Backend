import logging

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .messages import INVALID_CREDENTIALS, UNEXPECTED_ERROR, PROFILE_NOT_FOUND, RESET_EMAIL_SENT, PASSWORD_CHANGED, \
    EMAIL_DOES_NOT_EXIST
from api.models import User, Birth, Death, DeathRecord, BirthRecord, Profile
from .models import ActionLog
from .serializers import ActionLogSerializer
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    ResetPasswordConfirmSerializer, BirthSerializer, DeathSerializer, DeathRecordSerializer, BirthRecordSerializer, \
    UserLoginSerializer

logger = logging.getLogger(__name__)


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
                # auth_login(request, user)
                Token.objects.filter(user=user).delete()
                token, _ = Token.objects.get_or_create(user=user)
                logger.info(f"User {user.username} logged in successfully.")
                return Response(data={
                    'token': token.key,
                    # 'status': status.HTTP_200_OK,
                    'userData': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Invalid login attempt for username: {username}")
                return Response({'error': INVALID_CREDENTIALS}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.warning("Login serializer validation failed.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        logger.error(f"ValidationError occurred: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return Response({'error': UNEXPECTED_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def signup(request):
    serializer = UserSerializer(data=request.data)
    logger.info(f"User {request.user.username} signing up.")
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"User {user.username} logged in successfully.")
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    logger.error(f"User {request.user.username} signup failed.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_profile(request):
    try:
        profile = request.user.profile  # Make sure the user model has a OneToOneField for the profile
    except Profile.DoesNotExist:
        logger.warning(f"User {request.user.username} has no profile.")
        return Response({'error': PROFILE_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        logger.info(f"User {request.user.username} profile: {serializer.data}")
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {request.user.username} profile: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"User {request.user.username} profile: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def change_password(request):
    logger.info(f"User {request.user.username} change password.")
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        logger.info(f"User {user.username} changed password.")
        return Response({'message': PASSWORD_CHANGED}, status=status.HTTP_200_OK)
    else:
        logger.warning(f"User {request.user.username} changed password.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    logger.info(f"User {request.user.username} reset password.")
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': EMAIL_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)

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
        logger.info(f"User {request.user.username} reset password email sent.")
        return Response({'message': RESET_EMAIL_SENT}, status=status.HTTP_200_OK)
    else:
        logger.error(f"User {request.user.username} reset password failed.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password_confirm(request, uidb64, token):
    logger.info("Password reset request received for UID: %s", uidb64)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        logger.info("User found for UID: %s", uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError) as e:
        user = None
        logger.warning("Error decoding UID or fetching user: %s", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if user and default_token_generator.check_token(user, token):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            logger.info("Password reset successfully for user: %s", user.username)
            return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            logger.warning("Password reset validation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.warning("Invalid password reset attempt for UID: %s", uidb64)
        return Response({'error': 'Invalid password reset link'}, status=status.HTTP_400_BAD_REQUEST)


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
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
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
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication])
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


@api_view(['GET'])
def search_records(request):
    search_query = request.query_params.get('search', '')

    # Filter Birth and Death records based on search query
    births = Birth.objects.filter(
        Q(First_Name__icontains=search_query) |
        Q(Last_Name__icontains=search_query) |
        Q(gender__icontains=search_query) |
        Q(date__icontains=search_query) |
        Q(Place_of_Birth__icontains=search_query) |
        Q(City__icontains=search_query)
    )

    deaths = Death.objects.filter(
        Q(surname__icontains=search_query) |
        Q(date__icontains=search_query) |
        Q(Place_of_Death__icontains=search_query)
    )

    # Serialize the filtered queryset
    birth_serializer = BirthSerializer(births, many=True)
    death_serializer = DeathSerializer(deaths, many=True)

    # Combine the serialized data from both models
    data = {
        'births': birth_serializer.data,
        'deaths': death_serializer.data
    }

    return Response(data)
