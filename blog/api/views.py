from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import PostsSerializer
from .serializers import UsersSerializer
from ..models import Post


class Filter(rest_framework.FilterSet):
    class Meta:
        model = Post
        fields = {
            'published_date': ['lte', 'gte', 'lt', 'gt'],
            'created_date': ['lte', 'gte', 'lt', 'gt'],
            'title': ['exact'],
            'text': ['exact'],
            'author': ['exact']
        }


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    filter_class = Filter
    search_fields = ['title', 'text', 'author']


class UsersView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UsersSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO put method for update profile data
    # def put(self, request, pk):
    #     user = self.get_object(pk)
    #     serializer = UsersSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     user = self.get_object(pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
