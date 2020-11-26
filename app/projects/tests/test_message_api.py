from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Message

from projects.serializers import MessageSerializer


MESSAGES_URL = reverse('projects:message-list')


class PublicMessagesApiTests(TestCase):
    """Test the publicly available messages API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_public_messages_invalid(self):
        """Test that unauthenticated users can't access the messages API"""
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123')
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'password123')
        Message.objects.create(user=self.user,
                               recipient=self.user2,
                               message='Hey man!')
        Message.objects.create(user=self.user2,
                               recipient=self.user,
                               message='Hey woman!')
        res = self.client.get(MESSAGES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('Hey man!', res.data)
        self.assertNotIn('Hey woman!', res.data)


class PrivateMessagesApiTests(TestCase):
    """Test the private messages API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@xemob.com',
            'password123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.user2 = get_user_model().objects.create_user(
            'other@xemob.com',
            'password123')

    def test_retrieve_messages_by_authenticated_valid_user(self):
        """Test that a user can retrieve messages where he is involved"""
        Message.objects.create(user=self.user,
                               recipient=self.user2,
                               message='Hey man!')
        Message.objects.create(user=self.user2,
                               recipient=self.user,
                               message='Hey woman!')
        res = self.client.get(MESSAGES_URL)

        messages = Message.objects.all().order_by('-date')
        serializer = MessageSerializer(messages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_messages_by_not_owner_invalid(self):
        """Test retrieve messages by non-authorized user returns invalid"""
        Message.objects.create(user=self.user2,
                               recipient=self.user2,
                               message='Hey man!')
        Message.objects.create(user=self.user2,
                               recipient=self.user2,
                               message='Hey woman!')
        res = self.client.get(MESSAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('Hey man!', res.data)
        self.assertNotIn('Hey woman!', res.data)

    def test_create_a_message_successful(self):
        """Test create a message by an authenticated user"""
        message = 'Are you as supercool as me?'
        payload = {'user': self.user.id, 'recipient': self.user2.id,
                   'message': message}
        self.client.post(MESSAGES_URL, payload)

        exists = Message.objects.filter(
            user=self.user,
            message=payload['message']
        ).exists()
        self.assertTrue(exists)

    def test_create_a_message_invalid(self):
        """Test create a messge with invalid payload fails"""
        message = ''
        payload = {'user': self.user.id, 'recipient': self.user2.id,
                   'message': message}
        res = self.client.post(MESSAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
