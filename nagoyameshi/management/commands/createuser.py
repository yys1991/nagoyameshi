from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # ここを書き換える。
        USER_NAME = "yushimizu1"
        EMAIL = "yu.shimizu1991@gmail.com"
        PASSWORD = "yushimizu0718"

        # ユーザーを作成
        if not User.objects.filter(username=USER_NAME).exists():
            User.objects.create_superuser(USER_NAME, EMAIL, PASSWORD)
            print('Superuser created successfully.')
        else:
            print('Superuser already exists.')
