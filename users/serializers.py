from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(allow_null=False)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists!')


class ConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)