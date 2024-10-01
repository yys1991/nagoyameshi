import os
import django
from django.contrib.auth.models import User

# Djangoの設定を読み込む
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# ここを書き換える。
USER_NAME = "yushimizu"
EMAIL = "yu.californian@gmail.com"
PASSWORD = "yu0718"


# ユーザーを作成
if not User.objects.filter(username=USER_NAME).exists():
    User.objects.create_superuser(USER_NAME, EMAIL, PASSWORD)
    print('Superuser created successfully.')
else:
    print('Superuser already exists.')
