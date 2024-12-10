"""
Asad Soomro
asoomro@bu.edu

This file defines the data models for the Rock City climbing gym project. It includes the following models:
1. Route: Represents climbing routes, their attributes, and associated images.
2. Comment: Allows users to comment on specific routes, with support for replies and likes.
3. Vote: Tracks user votes for archived climbing routes to bring them back into rotation.
4. NewsletterPost: Represents newsletter posts with titles, content, creation dates, likes, and optional images.
5. Profile: Extends the user model to include profile pictures, staff status, bio, and a list of completed routes.

Each model includes methods for string representation and absolute URL generation where applicable.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver


class Route(models.Model):
    STATUS_CHOICES = [
        ('current', 'Current'),
        ('archived', 'Archived'),
    ]

    TYPE_CHOICES = [
        ('overhang', 'Overhang'),
        ('slab', 'Slab'),
        ('vertical', 'Vertical'),
        ('traverse', 'Traverse'),
        ('dyno', 'Dyno'),
    ]

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='overhang',
    )

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    difficulty = models.IntegerField(choices=[(i, f'V{i}') for i in range(13)], default=0)
    setter_name = models.CharField(max_length=100)
    date_set = models.DateField()
    replacement_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='current')
    image = models.ImageField(upload_to='route_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'
    
    def get_absolute_url(self):
        return reverse('route-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.route.name}'

    @property
    def is_parent(self):
        return self.parent is None



class Vote(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('route', 'user')

    def __str__(self):
        return f'Vote by {self.user.username} for {self.route.name}'
    
class NewsletterPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=now, editable=True)
    likes = models.ManyToManyField(User, related_name='liked_newsletters', blank=True)
    image = models.ImageField(upload_to='newsletter_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    completed_routes = models.ManyToManyField(Route, related_name='completed_by', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    staff_status = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})
    
