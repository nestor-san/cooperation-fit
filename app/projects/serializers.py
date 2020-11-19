from rest_framework import serializers

from core.models import Organization, CooperatorProfile, Project


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


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name', 'user', 'organization',
                  'description', 'ref_link')
        ready_only_fields = ('id', 'user', 'organization')
