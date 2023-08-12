from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAuthorOrAdminOrReadOnly
from users.models import Follow, User
from users.pagination import UsersPagination
from users.serializers import FollowSerializer, UserSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(
            self.request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        follows = self.paginate_queryset(
            Follow.objects.filter(user=self.request.user))
        serializer = FollowSerializer(
            follows, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, id=self.kwargs.get('id'))
        follow_exists = Follow.objects.filter(
            author=following, user=follower).exists()
        if request.method == 'POST':
            if follow_exists:
                return Response(
                    {"errors": "Вы уже подписаны на этого автора!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if follower == following:
                return Response(
                    {"errors": "Нельзя подписаться на себя самого!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=follower, author=following)
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if not follow_exists:
            return Response(
                {"errors": "Вы не подписаны на этого автора!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.get(user=follower, author=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
