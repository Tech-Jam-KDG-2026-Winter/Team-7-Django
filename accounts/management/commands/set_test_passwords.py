from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User


class Command(BaseCommand):
    help = "テストユーザーのために仮パスワードを設定"

    def handle(self, *args, **options):
        
        test_users = [
            ('tanaka@example.com', 'password123'),
            ('sato@example.com', 'password123'),
            ('suzuki@example.com', 'password123'),
        ]

        for email, password in test_users:
            try:
                user = User.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'({email}) のパスワードを設定しました')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'ユーザー {email} が見つかりません')
                )

        self.stdout.write(
            self.style.SUCCESS('\n全てのテストユーザーのパスワード: password123')
        )