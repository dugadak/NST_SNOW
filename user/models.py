from django.contrib.auth.models import AbstractUser
from django.db import models


# 장고 유저모델 상속하여 UserModel 생성
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"
