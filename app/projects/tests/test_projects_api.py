from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Organization

from projects.serializers import ProjectSerializer


PROJECT_URL = reverse('projects:project-list')


class PublicProjectApiTest(TestCase):
    """Test the publicly available projects API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_projects_list(self):
        """Test retrieving a list of projects by unauthenticated user"""
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123'
        )
        ngo = Organization.objects.create(user=self.user,
                                          name='NGO-1',
                                          country='Spain')
        Project.objects.create(user=self.user,
                               name='Project 1',
                               organization=ngo)
        Project.objects.create(user=self.user,
                               name='Project 2',
                               organization=ngo)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)


class PrivateProjectsApiTests(TestCase):
    """Test the authorized user projects API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123'
        )
        self.ngo = Organization.objects.create(user=self.user,
                                               name='NGO-1',
                                               country='Spain')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_project_successful(self):
        """Test creating a new project"""
        ngo = Organization.objects.create(user=self.user,
                                          name='NGO-inside',
                                          country='Spain')
        payload = {'name': 'Test project', 'organization': ngo}
        self.client.post(PROJECT_URL, payload)

        Project.objects.create(user=self.user,
                               name='Project 1',
                               organization=ngo)

        exists = Project.objects.filter().exists()
        self.assertTrue(exists)

    def test_create_project_invalid(self):
        """Create a project with invalid payload"""
        payload = {'name': '', 'organization': self.ngo}
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
