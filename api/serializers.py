from rest_framework import serializers
from .models import CustomUser, Hobby

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth', 'hobbies', 'current_password', 'new_password' 'similarity_score']

    def validate_email(self, value):
        # Check if email exists for other users
        if self.instance and value != self.instance.email:  # If email is being changed
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        # If user is trying to change password, validate current password
        if 'new_password' in data and not data.get('current_password'):
            raise serializers.ValidationError(
                {'current_password': 'Current password is required to set new password'}
            )

        if 'current_password' in data:
            if not self.instance.check_password(data['current_password']):
                raise serializers.ValidationError(
                    {'current_password': 'Wrong password'}
                )

        return data

    def update(self, instance, validated_data):
        # Handle password update if provided
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])
            validated_data.pop('new_password')
            validated_data.pop('current_password', None)

        return super().update(instance, validated_data)
    
    def get_similarity_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.similarity_score(obj)
        return 0