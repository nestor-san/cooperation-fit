from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PortfolioItem

from projects.serializers import PortfolioItemSerializer


PORTFOLIO_URL = reverse('projects:portfolioitem-list')


class PublicPortfolioApiTests(TestCase):
    """Test the publicly available projects API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_not_required(self):
        """Test that login is not required to access the endpoint"""
        res = self.client.get(PORTFOLIO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_portfolio_list(self):
        """Test retrieving a list of portfolio items"""
        sample_user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        PortfolioItem.objects.create(user=sample_user,
                                     name='Portfolio Item 1')
        PortfolioItem.objects.create(user=sample_user,
                                     name='Portfolio Item 2')
        res = self.client.get(PORTFOLIO_URL)

        portfolio_items = PortfolioItem.objects.all().order_by('-name')
        serializer = PortfolioItemSerializer(portfolio_items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivatePortfolioApiTests(TestCase):
    """Test the private portfolio API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_create_portfolio_item_successfully(self):
        """Test creating a new portfolio item"""
        payload = {'name': 'New portfolio item', 'user': self.user.id}
        self.client.post(PORTFOLIO_URL, payload)

        exists = PortfolioItem.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
