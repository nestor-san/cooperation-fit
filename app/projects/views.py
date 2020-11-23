from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Organization, CooperatorProfile, Project, \
    PortfolioItem, Cooperation, Review

from projects import serializers


class BaseProjectsAttrViewSet(viewsets.ModelViewSet):
    """Base vieset for projects attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        """Create a new Portfolio Item"""
        serializer.save(user=self.request.user)


class OrganizationViewSet(BaseProjectsAttrViewSet):

    """Manage Organizations in the database"""
    queryset = Organization.objects.all().order_by('-id')
    serializer_class = serializers.OrganizationSerializer


class CooperatorProfileViewSet(BaseProjectsAttrViewSet):
    """Manage Cooperators in the database"""
    queryset = CooperatorProfile.objects.all().order_by('-name')
    serializer_class = serializers.CooperatorProfileSerializer


class ProjectViewSet(BaseProjectsAttrViewSet):
    """Manage Projects in the database"""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all().order_by('-id')


class PortfolioItemViewSet(BaseProjectsAttrViewSet):
    """Manage Portfolio Items in the database"""
    serializer_class = serializers.PortfolioItemSerializer
    queryset = PortfolioItem.objects.all().order_by('-name')


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
