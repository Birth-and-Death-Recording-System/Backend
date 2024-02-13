from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model


# Create your views here.
@api_view(['POST'])
def login(request):
    return Response()


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
