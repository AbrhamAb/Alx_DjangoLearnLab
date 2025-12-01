from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create Editor, Viewer, and Admin groups and assign bookshelf permissions.'

    def handle(self, *args, **options):
        # Ensure the permissions exist for the Book model
        try:
            content_type = ContentType.objects.get(app_label='bookshelf', model='book')
        except ContentType.DoesNotExist:
            self.stdout.write(self.style.ERROR('ContentType for bookshelf.Book not found. Run makemigrations and migrate first.'))
            return

        perms = {}
        for codename, _ in (
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ):
            try:
                perms[codename] = Permission.objects.get(codename=codename, content_type=content_type)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission {codename} not found.'))
                perms[codename] = None

        # Create groups
        groups = {
            'Editors': ['can_create', 'can_edit', 'can_view'],
            'Viewers': ['can_view'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, group_perms in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group {group_name} already exists'))
            # Clear existing perms then add
            group.permissions.clear()
            for codename in group_perms:
                perm = perms.get(codename)
                if perm:
                    group.permissions.add(perm)
            self.stdout.write(self.style.SUCCESS(f'Assigned permissions to {group_name}'))

        self.stdout.write(self.style.SUCCESS('Groups setup completed.'))
