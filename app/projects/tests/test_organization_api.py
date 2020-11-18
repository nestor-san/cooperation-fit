from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Organization

from projects.serializers import OrganizationSerializer


ORGANIZATION_URL = reverse('projects:organization-list')


class PublicOrganizationApiTests(TestCase):
    """Test the publicly available organization API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_organization_listing(self):
        """Test that unauthenticated users can get a list of organizations"""
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123'
        )
        Organization.objects.create(user=self.user,
                                    name='NGO-1',
                                    country='Spain')
        Organization.objects.create(user=self.user,
                                    name='NGO-2',
                                    country='France')

        res = self.client.get(ORGANIZATION_URL)

        organizations = Organization.objects.all().order_by('-id')
        serializer = OrganizationSerializer(organizations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)


class PrivateOrganizationApiTests(TestCase):
    """Test the authorized user organization API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_organization_successful(self):
        """Test creating a new organization"""
        payload = {'name': 'NGO', 'country': 'Spain'}
        self.client.post(ORGANIZATION_URL, payload)

        exists = Organization.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_organization_invalid(self):
        """Create a new organization with invalid payload"""
        payload = {'name': '', 'country': 'Spain'}
        res = self.client.post(ORGANIZATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
