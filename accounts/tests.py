# accounts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserModelTests(TestCase):
    
    def test_create_user_with_default_role(self):
        """Memastikan user baru dibuat dengan role default TECHNICIAN"""
        User = get_user_model()
        user = User.objects.create_user(
            username='teknisi1',
            email='teknisi1@cmms.com',
            password='passwordaman123'
        )
        self.assertEqual(user.username, 'teknisi1')
        self.assertEqual(user.role, User.Role.TECHNICIAN)
        self.assertFalse(user.is_staff)

    def test_create_superuser_role(self):
        """Memastikan superuser berhasil dibuat"""
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='admin_cmms',
            email='admin@cmms.com',
            password='passwordsuper123'
        )
        self.assertEqual(admin_user.username, 'admin_cmms')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)