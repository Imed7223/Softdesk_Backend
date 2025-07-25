from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_age(self, value):
        if value is not None and value < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value

    def validate(self, data):
        if not data.get('can_data_be_shared', False):
            raise serializers.ValidationError("Le consentement sur le partage des données est requis (RGPD).")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            age=validated_data.get('age'),
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
            is_active=True  # ⚠️ Nécessaire !
        )
        user.set_password(validated_data['password'])  # Hash correct du mot de passe
        user.save()
        return user
