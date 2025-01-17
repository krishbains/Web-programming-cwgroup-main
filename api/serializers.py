from rest_framework import serializers
from .models import CustomUser, Hobby, FriendRequest

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    hobbies = HobbySerializer(many=True, read_only=True)  # Make hobbies read-only if not handling hobby updates
    similarity_score = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth', 'hobbies', 'current_password', 'new_password']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'date_of_birth': {'required': False}
        }

    def validate_email(self, value):
        # Check if email exists for other users
        if self.instance and value != self.instance.email:  # If email is being changed
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        # If user is trying to change password
        if 'new_password' in data:
            if not data.get('current_password'):
                raise serializers.ValidationError(
                    {'current_password': 'Current password is required to set new password'}
                )
            if not self.instance.check_password(data['current_password']):
                raise serializers.ValidationError(
                    {'current_password': 'Wrong password'}
                )

        return data


    def update(self, instance, validated_data):
        # Handle password update if provided
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])
            # Remove password fields from validated_data
            validated_data.pop('new_password', None)
            validated_data.pop('current_password', None)
            instance.save()

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def get_similarity_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.similarity_score(obj)
        return 0

class FriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'sender_username', 'receiver_username', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']