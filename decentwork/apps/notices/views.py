from django.utils.translation import gettext as _
from rest_framework import authentication, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from decentwork.apps.notices.models import Notice, UserAssigned
from decentwork.apps.notices.serializers import (AssignNoticeSerializer,
                                                    CheckAssignSerializer,
                                                    NoticeSerializer)


class NoticePagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NoticesViewSet(viewsets.ModelViewSet):
    """ViewSet for `Notice` model."""
    queryset = Notice.objects.filter(is_done=False).order_by('created')
    serializer_class = NoticeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = NoticePagination

    def get_permissions(self):
        actions = ['create', 'update', 'partial_update', 'set_notice_done']
        if self.action in actions:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: NoticeSerializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer: NoticeSerializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def set_notice_done(self, request, pk=None):
        if pk is None:
            return Response(_('No id notice passed'), status=status.HTTP_400_BAD_REQUEST)
        
        Notice.objects.filter(pk=pk, owner=request.user).update(is_done=True)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        pass


class UserNoticesListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List of notices which user created."""
    serializer_class = NoticeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = NoticePagination

    def get_queryset(self):
        """Selects notices created by user."""
        user = self.request.user
        return Notice.objects.filter(owner=user, is_done=False)


class AssignUserViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Create assign between user and notice or delete it."""
    serializer_class = AssignNoticeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'notice_id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Selects user's assigned notices to perform delete."""
        user = self.request.user
        return UserAssigned.objects.filter(user=user)


class ListAssigment(generics.ListAPIView):
    """List all assigned users to single notice"""
    serializer_class = AssignNoticeSerializer
    authentication_classes = []

    def get_queryset(self):
        notice = self.request.query_params.get('notice', None)

        if notice is None:
            raise ParseError(_('No notice passed'))

        return UserAssigned.objects.filter(notice=notice)


class CheckAssign(APIView):
    """Check if user is assigned to notice already."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None) -> Response:
        user = self.request.user
        notice = self.request.query_params.get('notice', None)

        if notice is None:
            return Response(_('No notice passed'), status=status.HTTP_400_BAD_REQUEST)
        
        assign = UserAssigned.objects.filter(user=user, notice=notice).first()

        if assign:
            serializer = CheckAssignSerializer({'is_assigned': True})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = CheckAssignSerializer()
            return Response(serializer.data, status=status.HTTP_200_OK)
