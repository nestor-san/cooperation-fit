from rest_framework import serializers

from core.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializser for organization objects"""

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'web', 'address', 'country')
        ready_only_fields = ('id',)
