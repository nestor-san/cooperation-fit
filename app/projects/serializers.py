from rest_framework import serializers

from core.models import Organization, CooperatorProfile, Project, \
    PortfolioItem, Cooperation, Review, Message


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializser for organization objects"""

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'website', 'address', 'country')
        read_only_fields = ('id',)


class CooperatorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Cooperator objects"""

    class Meta:
        model = CooperatorProfile
        fields = ('user', 'name', 'description', 'skills', 'website')
        read_only_fields = ('user',)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name', 'user', 'organization',
                  'description', 'ref_link')
        read_only_fields = ('id',)


class PortfolioItemSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio Items"""

    class Meta:
        model = PortfolioItem
        fields = ('id', 'user', 'name', 'description', 'link')
        read_only_fields = ('id',)


class CooperationSerializer(serializers.ModelSerializer):
    """Serialize a Cooperation"""

    class Meta:
        model = Cooperation
        fields = ('id', 'name', 'project', 'user', 'voluntary',
                  'start_date', 'end_date', 'is_private')
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize a review"""

    class Meta:
        model = Review
        fields = ('id', 'name', 'cooperation', 'reviewer', 'reviewed',
                  'review', 'comment')
        read_only_fields = ('id',)


class MessageSerializer(serializers.ModelSerializer):
    """Serialize a message"""

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'message', 'date')
        read_only_fields = ('id',)
