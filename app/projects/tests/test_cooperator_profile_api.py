from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import CooperatorProfile

from projects.serializers import CooperatorProfileSerializer


COOPERATOR_PROFILE_URL = reverse('projects:cooperatorprofile-list')


def detail_url(cooperator_id):
    """Return the detail URL of a cooperator"""
    return reverse('projects:cooperatorprofile-detail', args=[cooperator_id])


class PublicCooperatorApiTests(TestCase):
    """Test the publicly available Cooperators API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_not_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(COOPERATOR_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateCooperatorApiTests(TestCase):
    """Test the private Coperator API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_cooperators_list(self):
        """Test retrieving a list of cooperators"""
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        CooperatorProfile.objects.create(user=self.user,
                                         name='Nestor',
                                         description="""
                             I\'m a super web designer.""")

        CooperatorProfile.objects.create(user=self.user2,
                                         name='Pablo',
                                         description="""
                             I\'m a super video producer""")

        res = self.client.get(COOPERATOR_PROFILE_URL)

        cooperators = CooperatorProfile.objects.all().order_by('-name')
        serializer = CooperatorProfileSerializer(cooperators, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_cooperator_profile_successful(self):
        """Test creating a new cooperator profile"""
        payload = {'user': self.user.id,
                   'name': 'Nestor',
                   'description': "I'm a super web designer."}
        self.client.post(COOPERATOR_PROFILE_URL, payload)

        exists = CooperatorProfile.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_cooperator_profile_invalid(self):
        """Create a new coopeartor with invalid payload"""
        payload = {'name': '', 'description': 'A supernob man.'}
        res = self.client.post(COOPERATOR_PROFILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_cooperator_successful(self):
        """Test partial update of cooperator by owner is successful"""
        cooperator = CooperatorProfile.objects.create(user=self.user,
                                                      name='Nestor',
                                                      description="""
                                            I\'m a super web designer.""")
        payload = {'name': 'dumb'}
        url = detail_url(cooperator.user.id)
        res = self.client.patch(url, payload)

        cooperator.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(cooperator.name, payload['name'])

    def test_partial_update_by_not_owner_invalid(self):
        """Test updating an item by not owner return not authorized"""
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        cooperator = CooperatorProfile.objects.create(user=self.user2,
                                                      name='Nestor',
                                                      description="""
                                        I\'m a super web designer.""")
        payload = {'name': 'dumb'}
        url = detail_url(cooperator.user.id)
        res = self.client.patch(url, payload)

        cooperator.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(cooperator.name, payload['name'])

    def test_full_update_cooperator_successful(self):
        """Test partial update of cooperator by owner is successful"""
        cooperator = CooperatorProfile.objects.create(user=self.user,
                                                      name='Nestor',
                                                      description="""
                                            I\'m a super web designer.""")
        payload = {'user': self.user.id,
                   'name': 'dumb',
                   'description': 'dumbass'}
        url = detail_url(cooperator.user.id)
        res = self.client.put(url, payload)

        cooperator.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(cooperator.name, payload['name'])
        self.assertEqual(cooperator.description, payload['description'])

    def test_full_update_by_not_owner_invalid(self):
        """Test updating an item by not owner return not authorized"""
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        cooperator = CooperatorProfile.objects.create(user=self.user2,
                                                      name='Nestor',
                                                      description="""
                                        I\'m a super web designer.""")
        payload = {'name': 'dumb', 'description': 'dumbass'}
        url = detail_url(cooperator.user.id)
        res = self.client.put(url, payload)

        cooperator.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(cooperator.name, payload['name'])
        self.assertNotEqual(cooperator.name, payload['description'])
