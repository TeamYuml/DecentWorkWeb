from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from decentwork.apps.common.models import User
from decentwork.apps.common.serializers import UserRegisterSerializer, UserLoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User common model."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        """Create user."""
        password = self.request.data['password']

        serializer.save(password=password)


class UserApiLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.filter(email=request.data['email'])

            if user is not None:
                user = authenticate(
                    username=user.username,
                    password=request.data['password']
                )

                if user is not None:
                    return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)    

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)