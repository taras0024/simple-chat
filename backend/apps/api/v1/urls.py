from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, ThreadsViewSet, MessagesViewSet

router = SimpleRouter()
router.register(r"users", UsersViewSet, basename="users")
router.register(r"threads", ThreadsViewSet, basename="threads")
router.register(r"messages", MessagesViewSet, basename="messages")

urlpatterns = router.urls
