from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PortfolioItem

from projects.serializers import PortfolioItemSerializer


PORTFOLIO_URL = reverse('projects:portfolioitem-list')


def detail_url(portfolio_id):
    """Return the detail URL of a portfolio item"""
    return reverse('projects:portfolioitem-detail', args=[portfolio_id])


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

    def test_create_portfolio_item_invalid(self):
        """Test creating a portfolio item with invalid payload"""
        payload = {'name': '', 'user': self.user.id}
        res = self.client.post(PORTFOLIO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_portfolio_update_successfully(self):
        """Test partial updating a project by owner is successful"""
        portfolio_item = PortfolioItem.objects.create(user=self.user,
                                                      name='Portfolio Item 1')
        payload = {'name': 'Alt portfolio item'}
        url = detail_url(portfolio_item.id)
        res = self.client.patch(url, payload)

        portfolio_item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(portfolio_item.name, payload['name'])

    def test_partial_portfolio_update_invalid(self):
        """Test updating a portfolio item by not owner is invalid"""
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        portfolio_item = PortfolioItem.objects.create(user=self.user2,
                                                      name='Portfolio Item 1')
        payload = {'name': 'Alt portfolio item'}
        url = detail_url(portfolio_item.id)
        res = self.client.patch(url, payload)

        portfolio_item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(portfolio_item.name, payload['name'])

    def test_full_portfolio_update_successful(self):
        """Test updating a portfolio item by owner is successful with PUT"""
        portfolio_item = PortfolioItem.objects.create(user=self.user,
                                                      name='Portfolio Item 1')
        payload = {'user': self.user.id, 'name': 'Alt portfolio item'}
        url = detail_url(portfolio_item.id)
        res = self.client.put(url, payload)

        portfolio_item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(portfolio_item.name, payload['name'])

    def test_full_portfolio_update_invalid(self):
        """Test updateing a portfolio item by not owner is invalid with PUT"""
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )
        portfolio_item = PortfolioItem.objects.create(user=self.user2,
                                                      name='Portfolio Item 1')
        payload = {'user': self.user.id, 'name': 'Alt portfolio item'}
        url = detail_url(portfolio_item.id)
        res = self.client.put(url, payload)

        portfolio_item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(portfolio_item.name, payload['name'])
