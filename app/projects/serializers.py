from rest_framework import serializers

from core.models import Organization, CooperatorProfile


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializser for organization objects"""

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'website', 'address', 'country')
        ready_only_fields = ('id',)


class CooperatorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Cooperator objects"""

    class Meta:
        model = CooperatorProfile
        fields = ('id', 'name', 'description', 'skills', 'website')
        ready_only_fields = ('id',)
