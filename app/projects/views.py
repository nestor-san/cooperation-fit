from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly

from core.models import Organization, CooperatorProfile, Project, \
    PortfolioItem, Cooperation, Review, Message

from projects import serializers


class BaseProjectsAttrViewSet(viewsets.ModelViewSet):
    """Base vieset for projects attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """Create a new Portfolio Item"""
        if serializer.is_valid():
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

    def validate_user(self, value):
        """Validate that the user in the request field user is the same
        who makes the POST request"""
        if value != self.request.user.id:
            raise ValidationError("""You'0re trying to edit objects from
        another user. You only can edit your own objects. Please, login
        and try again""")
        return value


class ReviewViewSet(BaseProjectsAttrViewSet):
    """Manage Reviews in the database"""
    queryset = Review.objects.all().order_by('-id')
    serializer_class = serializers.ReviewSerializer


class MessageViewSet(BaseProjectsAttrViewSet):
    """Manage messages in the database"""
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all().order_by('-date')
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        """Retrieve the messages where the user is involved"""
        return self.queryset.filter(
            Q(user=self.request.user) | Q(recipient=self.request.user)
        ).order_by('-date')
