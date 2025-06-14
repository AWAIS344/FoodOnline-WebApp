# serializers.py

from rest_framework import serializers
from vendor.models import Vendor
from accounts.models import User
from accounts.models import UserProfile
from accounts.api.serializers import UserRegistrationSerializer


class VendorSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Vendor
        fields = ['user', 'vendor_name', 'vendor_license']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user_serializer = UserRegistrationSerializer(data=user_data, role=User.VENDOR)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        vendor = Vendor.objects.create(
            user=user,
            user_profile=user_profile,
            **validated_data
        )
        return vendor