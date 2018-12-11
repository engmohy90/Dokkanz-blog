from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Post


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("__all__")


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(UsersSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = super(UsersSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user