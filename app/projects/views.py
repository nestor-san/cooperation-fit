from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated

from core.models import Organization, CooperatorProfile, Project, \
    PortfolioItem, Cooperation, Review

from projects import serializers


class BaseProjectsAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Base vieset for projects attributes"""
    authentication_classes = (TokenAuthentication,)


class OrganizationViewSet(BaseProjectsAttrViewSet):

    """Manage Organizations in the database"""
    queryset = Organization.objects.all().order_by('-id')
    serializer_class = serializers.OrganizationSerializer

    def perform_create(self, serializer):
        """Create a new organization"""
        serializer.save(user=self.request.user)


class CooperatorProfileViewSet(BaseProjectsAttrViewSet):
    """Manage Cooperators in the database"""
    queryset = CooperatorProfile.objects.all().order_by('-name')
    serializer_class = serializers.CooperatorProfileSerializer

    def perform_create(self, serializer):
        """Create a new cooperator profile"""
        serializer.save(user=self.request.user)


class ProjectViewSet(BaseProjectsAttrViewSet):
    """Manage Projects in the database"""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all().order_by('-id')

    def perform_create(self, serializer):
        """Create a new project"""
        serializer.save(user=self.request.user)


class PortfolioItemViewSet(BaseProjectsAttrViewSet):
    """Manage Portfolio Items in the database"""
    serializer_class = serializers.PortfolioItemSerializer
    queryset = PortfolioItem.objects.all().order_by('-name')

    def perform_create(self, serializer):
        """Create a new Portfolio Item"""
        serializer.save(user=self.request.user)


class CooperationViewSet(BaseProjectsAttrViewSet):
    """Manage cooperations in the database"""
    serializer_class = serializers.CooperationSerializer
    queryset = Cooperation.objects.all()

    def get_queryset(self):
        """Retrieve the cooperations which aren't private"""
        return self.queryset.filter(is_private=False).order_by('-id')


class ReviewViewSet(BaseProjectsAttrViewSet):
    """Manage Reviews in the database"""
    queryset = Review.objects.all().order_by('-id')
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        """Create a new Portfolio Item"""
        serializer.save(reviewer=self.request.user)
