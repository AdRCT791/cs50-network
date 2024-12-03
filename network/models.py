from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', through='Follow', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_relations")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relations")

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}" 

class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    post_text = models.TextField(max_length=300)
    post_date = models.DateTimeField(auto_now=True)

    def likes_count(self):
        return self.like.count()

    def __str__(self):
        return f"{self.post_author} posted {self.post_text} on {self.post_date}"

class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")

# What is a like ? It is basically a change of state of an attribute
# either a user like a post or not. true of false
# Many users can like the same post
# how to count like. count the number of trues
# How to implement that in a model? 
# it is like a watchlist !
# So the like/heart button act as a form submit button



# Followers Model

# How can I represent a user following an other user ?
# Following Boolean True or False
# Followers 