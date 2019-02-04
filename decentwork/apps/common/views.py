from typing import Any, Dict, Optional

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import authentication, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from decentwork.apps.common.models import User
from decentwork.apps.common.serializers import (UserLoginSerializer,
                                                GoogleTokenSerializer)


class UserApiLogin(APIView):
    authentication_classes = ()

    def post(self, request, format=None) -> Response:
        """Tries to authenticate user."""
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not password or not email:
            return Response(_("No password or email"), status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(
            email=email).first()

        if user is not None:
            user = authenticate(
                username=user.username,
                password=password
            )

            if user is not None:
                serializer = UserLoginSerializer(data=request.data)

                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(_("No authorization"), status=status.HTTP_401_UNAUTHORIZED)


class TokenSignIn(APIView):
    """Handle user sign in from mobile device."""
    authentication_classes = ()

    def post(self, request, format=None) -> Response:
        """Creates user with data from Google oauth2 token when email doesn't exist in database.

        Returns:
            Response with UserLoginSerializer data and status code equal 200 if everything went okay.
            Response with status code equal 400 when user didn't send idToken with request.
            Response with status code equal 401 when token is invalid.
        """
        token = request.data.get('idToken', None)

        if token:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return Response(_("Token is wrong"), status=status.HTTP_401_UNAUTHORIZED)

            email = idinfo['email']
            user = User.objects.filter(email=email).first()

            if user is None:
                new_user = self._create_user(idinfo)

                SocialAccount.objects.create(
                    user=new_user,
                    provider='google',
                    uid=idinfo['sub'],
                    extra_data=idinfo
                )

                EmailAddress.objects.create(
                    user=new_user,
                    email=email,
                    primary=True,
                    verified=idinfo['email_verified']
                )

                return self._prepare_response(new_user)
            else:
                return self._prepare_response(user)

        return Response(_("No token"), status=status.HTTP_400_BAD_REQUEST)

    def _prepare_response(self, user: User) -> Optional[Dict[str, Any]]:
        """Serializes user data and prepares response for token sign in.

        Args:
            user: User to serialize.

        Returns:
            Response with status 200 when serializer data is valid
            Response with status 400 when serializer data is invalid
        """
        try:
            data = self._serialize_user_data(user)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError:
            return Response("Błąd serializacji", status=status.HTTP_400_BAD_REQUEST)

    def _serialize_user_data(self, user: User) -> GoogleTokenSerializer:
        """Serializes user data.

        Args:
            user: User object to serialize.

        Raises:
            ValueError: When serializer has not valid data

        Returns:
            Serialized data.
        """
        serializer = GoogleTokenSerializer(data={'email': user.email})

        if serializer.is_valid():
            return serializer.data

        raise ValueError

    def _create_user(self, idinfo: Dict[str, Any]) -> User:
        """Creates new User.

        Args:
            ididnfo: Information from Google about user.

        Returns:
            Saved new user.
        """
        user = User()
        # mark user to have no password
        user.set_unusable_password()
        user.email = idinfo['email']
        user.username = idinfo['email']
        user.save()

        return user


class PasswordChange(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def post(self, request, format=None):
        if not self.request.user.check_password(self.request.data.get("oldpassword")):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            new_password = self.request.data.get('password1', None)
            password_validation.validate_password(new_password)
            self.request.user.set_password(new_password)
            self.request.user.save()
            return Response(status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)