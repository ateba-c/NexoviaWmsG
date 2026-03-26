from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    role_code = serializers.CharField(source="role.code", read_only=True)
    tenant_schema = serializers.CharField(source="tenant.schema_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "preferred_language",
            "role_code",
            "tenant_schema",
            "is_floor_user",
        )


class NexoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["language"] = user.preferred_language
        token["role"] = user.role.code if user.role else None
        token["tenant"] = user.tenant.schema_name
        return token
