from rest_framework import authentication, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from decentwork.apps.profiles.models import Rating, UserProfile
from decentwork.apps.profiles.serializers import (
                                                  RatingSerializer,
                                                  UserNamesSerializer,
                                                  UserProfileSerializer,
                                                  UserProfileList)


class UserProfilePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserProfileSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model."""

    queryset = UserProfile.objects.exclude().order_by('?')
    serializer_class = UserProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = UserProfilePagination

    def get_permissions(self):
        actions = ['create', 'update', 'partial_update', 'rate']
        if self.action in actions:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        if pk is None:
            return Response(_('No user id passed'), status=status.HTTP_400_BAD_REQUEST)
        
        rating = request.data.get('rating', None)

        if rating:
            serializer = RatingSerializer(data={
                'rating': rating,
                'rated_user': pk,
                'rating_user': request.user.id
            })

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(_('No rating passed'), status=status.HTTP_400_BAD_REQUEST)


class ProfilesWithProfession(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.exclude(professions=None).order_by('?')
    serializer_class = UserProfileSerializer
    authentication_classes = []
    pagination_class = UserProfilePagination
