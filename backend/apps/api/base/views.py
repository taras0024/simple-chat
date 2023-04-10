from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .pagination import WebLimitOffsetPagination


class BaseApiViewSet(GenericViewSet):
    pagination_class = WebLimitOffsetPagination
    serializer_classes = {}
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.serializer_class

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "user": self.request.user}
