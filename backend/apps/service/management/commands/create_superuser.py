# -*- coding: utf-8 -*-
"""
Implement 'create_superuser' Django management command.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    A management command which creates default superuser.
    """
    help = 'Create default superuser'

    def handle(self, *args, **kwargs):
        User.objects.create_superuser(
            first_name='Admin-1',
            last_name='Super-1',
            email='admin1@example.com',
            password='admin123',
        )
        User.objects.create_superuser(
            first_name='Admin-2',
            last_name='Super-2',
            email='admin2@example.com',
            password='admin123',
        )
        User.objects.create_superuser(
            first_name='Admin-3',
            last_name='Super-3',
            email='admin3@example.com',
            password='admin123',
        )
