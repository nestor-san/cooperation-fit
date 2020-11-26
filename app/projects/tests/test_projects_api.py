from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Organization

from projects.serializers import ProjectSerializer


PROJECT_URL = reverse('projects:project-list')


def detail_url(project_id):
    """Create the detail URL for a project"""
    return reverse('projects:project-detail', args=[project_id])


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
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.ngo = Organization.objects.create(user=self.user,
                                               name='NGO-1',
                                               country='Spain')

    def test_create_project_successful(self):
        """Test creating a new project"""
        payload = {'name': 'Test project',
                   'organization': self.ngo.id,
                   'user': self.user.id}
        self.client.post(PROJECT_URL, payload)

        exists = Project.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_project_invalid(self):
        """Create a project with invalid payload"""
        payload = {'name': '', 'organization': self.ngo}
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_project_successful(self):
        """Test updating a project by owner successful"""
        project = Project.objects.create(user=self.user,
                                         name='Project 1',
                                         organization=self.ngo)
        payload = {'name': 'Updated project'}
        url = detail_url(project.id)
        res = self.client.patch(url, payload)

        project.refresh_from_db()
        self.assertEqual(project.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_partial_update_by_not_owner_invalid(self):
        """Test updating a project by not owner return not authorized"""
        self.user2 = get_user_model().objects.create_user('other@xemob.com',
                                                          'testpass')
        project = Project.objects.create(user=self.user2,
                                         name='Project 1',
                                         organization=self.ngo)
        payload = {'name': 'Updated project'}
        url = detail_url(project.id)
        res = self.client.patch(url, payload)

        project.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(project.name, payload['name'])

    def test_full_update_project_successful(self):
        """Test full updating a project by owner successful"""
        project = Project.objects.create(user=self.user,
                                         name='Project 1',
                                         organization=self.ngo)
        payload = {'name': 'Test project',
                   'organization': self.ngo.id,
                   'user': self.user.id}

        url = detail_url(project.id)
        res = self.client.put(url, payload)

        project.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(project.name, payload['name'])

    def test_full_update_by_not_owner_invalid(self):
        """Test updating a project by not owner return not authorized"""
        self.user2 = get_user_model().objects.create_user('other@xemob.com',
                                                          'testpass')
        project = Project.objects.create(user=self.user2,
                                         name='Project 1',
                                         organization=self.ngo)
        payload = {'user': self.user,
                   'name': 'Updated project',
                   'organiztion': self.ngo}
        url = detail_url(project.id)
        res = self.client.put(url, payload)

        project.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(project.name, payload['name'])
