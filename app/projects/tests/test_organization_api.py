from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Organization

from projects.serializers import OrganizationSerializer


ORGANIZATION_URL = reverse('projects:organization-list')


def detail_url(organization_id):
    """Return the detail URL of an organization"""
    return reverse('projects:organization-detail', args=[organization_id])


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

    def test_partial_update_organization_successful(self):
        """Test updating a new organization"""
        org = Organization.objects.create(name='Test NGO',
                                          country='Spain',
                                          user=self.user)
        payload = {'name': 'NGO altered'}
        url = detail_url(org.id)
        self.client.patch(url, payload)

        org.refresh_from_db()
        self.assertEqual(org.name, payload['name'])

    def test_full_update_organization_successful(self):
        """Test updating a organization with PUT"""
        org = Organization.objects.create(name='Test NGO',
                                          country='Spain',
                                          user=self.user)
        payload = {'name': 'Ngo altered PUT', 'country': 'Wonderland'}
        url = detail_url(org.id)
        self.client.put(url, payload)

        org.refresh_from_db()
        self.assertEqual(org.name, payload['name'])
        self.assertEqual(org.country, payload['country'])

    # def test_partial_update_for_not_owner_invalid(self):
    #     """Test updating an organization for a not owner return error"""
    #     user2 = get_user_model().objects.create_user('other@xemob.com',
    #                                                  'password123')
    #     org = Organization.objects.create(name='Test NGO',
    #                                       country='Spain',
    #                                       user=user2)
    #     payload = {'name': 'Ngo altered PUT', 'country': 'Wonderland'}
    #     url = detail_url(org.id)
    #     res = self.client.put(url, payload)

    #     org.refresh_from_db()
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertNotEqual(org.name, payload['name'])
    #     self.assertNotEqual(org.country, payload['country'])
