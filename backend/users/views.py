from rest_framework.decorators import action
from rest_framework import permissions
from api.permissions import IsAuthorOrAdminOrReadOnly

from djoser.views import UserViewSet
from users.models import User
from users.serializers import UserSerializer
from users.pagination import UsersPagination


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UsersPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)
