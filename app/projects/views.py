from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Organization, CooperatorProfile, Project
from projects import serializers


class OrganizationViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    """Manage Organizations in the database"""
    queryset = Organization.objects.all().order_by('-id')
    serializer_class = serializers.OrganizationSerializer

    def perform_create(self, serializer):
        """Create a new organization"""
        serializer.save(user=self.request.user)


class CooperatorProfileViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin):
    """Manage Cooperators in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CooperatorProfile.objects.all().order_by('-name')
    serializer_class = serializers.CooperatorProfileSerializer

    def perform_create(self, serializer):
        """Create a new cooperator profile"""
        serializer.save(user=self.request.user)


class ProjectViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage Projects in the database"""
    queryset = Project.objects.all().order_by('-id')
    serializer_class = serializers.ProjectSerializer

    def perform_create(self, serializer):
        """Create a new project"""
        serializer.save(user=self.request.user)
