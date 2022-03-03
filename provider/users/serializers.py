# Source: https://www.django-rest-framework.org/tutorial/quickstart/

from django.contrib.auth.models import User, Group
from .models import Dog
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class DogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dog
        fields = ["id", "name", "breed", "age", "is_friendly"]