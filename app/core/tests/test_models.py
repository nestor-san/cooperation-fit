from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@xemob.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@xemob.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@XEMOB.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@xemob.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_organization_str(self):
        """Test the NGO string representation"""
        organization = models.Organization.objects.create(
            user=sample_user(),
            name='sampleNGO',
            country='spain',
        )

        self.assertEqual(str(organization), organization.name)

    def test_cooperator_profile_str(self):
        """Test the cooperator string representation"""
        cooperator_pr = models.CooperatorProfile.objects.create(
            user=sample_user(),
            name='Pablo',
            description='I\'m a super web designer.',
            skills='Web design'
        )

        self.assertEqual(str(cooperator_pr), cooperator_pr.name)

    def test_portfolio_item_str(self):
        """Test the portfolio item string representation"""
        portfolio_item = models.PortfolioItem.objects.create(
            user=sample_user(),
            name='Portfolio item 1'
        )

        self.assertEqual(str(portfolio_item), portfolio_item.name)

    def test_projects_str(self):
        """Test the project string representation"""
        self.user = sample_user()
        self.organization = models.Organization.objects.create(
            user=self.user, name='Sample Ngo', country='Spain')

        project = models.Project.objects.create(
            user=self.user,
            name='Test project',
            organization=self.organization,
            description='Project description'
        )

        self.assertEqual(str(project), project.name)

    def test_cooperation_str(self):
        """Test the cooperation string representation"""
        self.user = sample_user()
        self.user2 = sample_user(email='other@xemob.com')
        self.organization = models.Organization.objects.create(
            user=self.user, name='Sample Ngo', country='Spain')
        self.project = models.Project.objects.create(
            user=self.user,
            name='Test project',
            organization=self.organization,
            description='Project description'
        )
        self.cooperation_name = f"""
        Cooperation between {self.user.name} and {self.user2.name},
        for the project {self.project.name}"""
        cooperation = models.Cooperation.objects.create(
            name=self.cooperation_name[:255],
            project=self.project,
            org_worker=self.user,
            voluntary=self.user2
        )

        self.assertEqual(str(cooperation), cooperation.name)
