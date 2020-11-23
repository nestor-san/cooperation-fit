from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Cooperation, Organization, Review

from projects.serializers import ReviewSerializer

REVIEW_URL = reverse('projects:review-list')


def sample_user(email='test@xemob.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicReviewApiTests(TestCase):
    """Test the publicly available reviews API"""

    def setUp(self):
        self.client = APIClient()

        self.user = sample_user()
        self.user2 = sample_user(email='other@xemob.com')
        self.organization = Organization.objects.create(
            user=self.user, name='Sample Ngo', country='Spain')
        self.project = Project.objects.create(
            user=self.user,
            name='Test project',
            organization=self.organization,
            description='Project description'
        )
        self.cooperation_name = f"""
        Cooperation between {self.user.name} and {self.user2.name},
        for the project {self.project.name}"""
        self.cooperation = Cooperation.objects.create(
            name=self.cooperation_name[:255],
            project=self.project,
            org_staff=self.user,
            voluntary=self.user2
        )

    def test_login_not_required(self):
        """Test that login is not required to access the endpoint"""
        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_cooperation_list(self):
        """Test retrieving a list of reviews items"""
        Review.objects.create(
            name='Title of sample review',
            cooperation=self.cooperation,
            reviewer=self.user,
            reviewed=self.user2,
            review='This is a sample review'
        )
        Review.objects.create(
            name='Title of sample review 2',
            cooperation=self.cooperation,
            reviewer=self.user2,
            reviewed=self.user,
            review='This is a sample review 2'
        )
        res = self.client.get(REVIEW_URL)

        reviews_items = Review.objects.all().order_by('-id')
        serializer = ReviewSerializer(reviews_items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateReviewApiTests(TestCase):
    """Test the Review API for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'testpass'
        )

    def test_create_review_successful(self):
        """Test create a review with valid payload"""
        sample_org = Organization.objects.create(user=self.user,
                                                 name='Sample ngo',
                                                 country='spain')
        sample_project = Project.objects.create(user=self.user,
                                                organization=sample_org,
                                                name='Sample Project')
        sample_cooperation = Cooperation.objects.create(
            name='Sample cooperation',
            project=sample_project)

        payload = {'name': 'This is a sample review',
                   'cooperation': sample_cooperation.id,
                   'reviewer': self.user.id,
                   'reviewed': self.user2.id,
                   'review': 'This is a sample review body'
                   }
        self.client.post(REVIEW_URL, payload)

        exists = Review.objects.filter(
             reviewer=self.user,
             name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_review_invalid(self):
        """Test creating reviwe with invalid payload fails"""
        sample_org = Organization.objects.create(user=self.user,
                                                 name='Sample ngo',
                                                 country='spain')
        sample_project = Project.objects.create(user=self.user,
                                                organization=sample_org,
                                                name='Sample Project')
        sample_cooperation = Cooperation.objects.create(
            name='Sample cooperation',
            project=sample_project)

        payload = {'name': '',
                   'cooperation': sample_cooperation,
                   'reviewer': self.user,
                   'reviewed': self.user2,
                   'review': ''
                   }
        res = self.client.post(REVIEW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
