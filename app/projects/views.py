from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Organization, CooperatorProfile
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
                               mixins.ListModelMixin,):
    """Manage Cooperators in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CooperatorProfile.objects.all().order_by('-name')
    serializer_class = serializers.CooperatorProfileSerializer
