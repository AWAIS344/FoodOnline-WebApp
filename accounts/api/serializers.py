# serializers.py

from rest_framework import serializers
from accounts.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password',
            'confirm_password', 'phone_number', 'email'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', User.CUSTOMER)  # 👈 Default is CUSTOMER
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = self.role  # 👈 Assign role dynamically
        user.save()
        return user
