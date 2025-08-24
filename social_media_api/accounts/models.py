# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Many-to-many relationship for following
    following = models.ManyToManyField(
        'self', 
        through='Follow',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.username

class Follow(models.Model):
    """Intermediate model for user follows"""
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_following'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
