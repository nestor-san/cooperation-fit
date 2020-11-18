from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import CooperatorProfile

from projects.serializers import CooperatorProfileSerializer


COOPERATOR_PROFILE_URL = reverse('projects:cooperatorprofile-list')


class PublicCooperatorApiTests(TestCase):
    """Test the publicly available Cooperators API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(COOPERATOR_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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
