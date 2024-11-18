from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    post_text = models.TextField(max_length=300)
    post_date = models.DateTimeField(auto_now=True)


# Followers Model

# How can I represent a user following an other user ?
# Following
# Followers 