from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Cooperation, Organization

from projects.serializers import CooperationSerializer

COOPERATION_URL = reverse('projects:cooperation-list')


class PublicCooperationApiTests(TestCase):
    """Test the publicly available cooperations API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_not_required(self):
        """Test that login is not required to access the endpoint"""
        res = self.client.get(COOPERATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_cooperation_list(self):
        """Test retrieving a list of cooperation items"""
        sample_user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        sample_user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        sample_org = Organization.objects.create(user=sample_user,
                                                 name='sample ngo',
                                                 country='spain')
        sample_project = Project.objects.create(user=sample_user,
                                                organization=sample_org,
                                                name='Sample Project')
        Cooperation.objects.create(name='Sample cooperation',
                                   project=sample_project,
                                   user=sample_user,
                                   voluntary=sample_user2)
        Cooperation.objects.create(name='Sample cooperation 2',
                                   project=sample_project,
                                   user=sample_user,
                                   voluntary=sample_user2)
        res = self.client.get(COOPERATION_URL)

        cooperation_items = Cooperation.objects.all().order_by('-id')
        serializer = CooperationSerializer(cooperation_items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_retrieve_private_cooperation(self):
        """Test that a private cooperation is not retrieved in the api"""
        sample_user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass')
        sample_user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass')
        sample_org = Organization.objects.create(user=sample_user,
                                                 name='sample ngo',
                                                 country='spain')
        sample_project = Project.objects.create(user=sample_user,
                                                organization=sample_org,
                                                name='Sample Project')
        Cooperation.objects.create(name='Private cooperation',
                                   project=sample_project,
                                   user=sample_user,
                                   voluntary=sample_user2,
                                   is_private=True)
        Cooperation.objects.create(name='Public cooperation 2',
                                   project=sample_project,
                                   user=sample_user,
                                   voluntary=sample_user2)
        res = self.client.get(COOPERATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('Private cooperation', res.data)
        self.assertEqual(len(res.data), 1)


class PrivateCooperationApiTests(TestCase):
    """Test the cooperation api for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.org = Organization.objects.create(user=self.user,
                                               name='Sample ngo',
                                               country='spain')
        self.project = Project.objects.create(user=self.user,
                                              organization=self.org,
                                              name='Sample Project')
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        self.org2 = Organization.objects.create(user=self.user2,
                                                name='User 2 ngo',
                                                country='Wonderland')
        self.project2 = Project.objects.create(user=self.user2,
                                               organization=self.org,
                                               name='Sample Project')

    def test_create_cooperation_successful(self):
        """Test create a new cooperation with valid payload"""
        payload = {'user': self.user.id,
                   'name': 'Cooperation sample',
                   'project': self.project.id}

        self.client.post(COOPERATION_URL, payload)

        exists = Cooperation.objects.filter(name=payload['name']).exists()

        self.assertTrue(exists)

    def test_create_cooperation_invalid(self):
        """Test creating invalid Cooperation fails"""
        payload = {'name': '', 'project': self.project}
        res = self.client.post(COOPERATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_cooperation_for_not_owned_project(self):
        """Test that the user is the owner of the project related with
        a coperation being created. If it's not the owner aise an error."""
        payload = {'user': self.user.id,
                   'name': 'Rapped Cooperation',
                   'project': self.project2.id}
        res = self.client.post(COOPERATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_cooperation_for_another_user_is_invalid(self):
        """Check that a user can't create a cooperation posting on
        behalf of another user"""
        payload = {'user': self.user2.id,
                   'name': 'Rapped Cooperation',
                   'project': self.project2.id}
        res = self.client.post(COOPERATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
