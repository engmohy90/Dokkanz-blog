from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from .views import PostsViewSet, UsersView

router = DefaultRouter()
router.register(prefix='post', viewset=PostsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^createUser/', UsersView.as_view()),
]
