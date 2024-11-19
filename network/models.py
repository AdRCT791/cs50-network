from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    post_text = models.TextField(max_length=300)
    post_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return self.post_text


# What is a like ? It is basically a change of state of an attribute
# either a user like a post or not. true of false
# Many users can like the same post
# how to count like. count the number of trues
# How to implement that in a model? 
# it is like a watchlist !
# So the like/heart button act as a form submit button



# Followers Model

# How can I represent a user following an other user ?
# Following
# Followers 