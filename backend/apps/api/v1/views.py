from django.db.models import Count, Prefetch
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from db.chats.models import Thread, Message
from db.users.models import User
from .serializers import UserSerializer, ReadThreadSerializer, WriteThreadSerializer, WriteMessageSerializer
from ..base.views import BaseApiViewSet


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint for read users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def threads(self, request, pk=None):
        """Get all threads for user"""
        user = self.get_object()
        threads = Thread.objects.filter(participants=user)
        serializer = ReadThreadSerializer(instance=threads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def unread_messages(self, request, pk=None):
        """Get count of unread messages for user"""
        user = self.get_object()
        unread = Thread.objects.filter(
            participants=user,
            messages__is_read=False
        )
        return Response({"count": unread.count()})

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data)


class MessagesViewSet(mixins.CreateModelMixin, BaseApiViewSet):
    """Endpoint for read/write messages"""
    queryset = Message.objects.all()
    serializer_class = WriteMessageSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response(status=status.HTTP_201_CREATED)


class ThreadsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    BaseApiViewSet
):
    """Endpoint for read/write threads"""
    queryset = (
        Thread.objects
        .prefetch_related(
            Prefetch("messages", queryset=Message.objects.order_by("-created_at"))
        )
    )
    permission_classes = [IsAuthenticated]
    serializer_classes = {
        "list": ReadThreadSerializer,
        "retrieve": ReadThreadSerializer,
        "create": WriteThreadSerializer,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ReadThreadSerializer(instance=instance).data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Add user to thread"""
        thread = self.get_object()
        if request.user in thread.participants.all():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "User is already a participant"})

        if thread.participants.count() >= 2:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Thread is full"})

        thread.participants.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Remove user from thread"""
        thread = self.get_object()
        if request.user not in thread.participants.all():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "User is not a participant"})

        thread.participants.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all threads with less than 2 participants"""
        qs = (
            self.get_queryset()
            .annotate(participants_count=Count('participants'))
            .filter(participants_count__lt=2)
        )
        serializer = ReadThreadSerializer(instance=qs, many=True)
        return Response(serializer.data)
