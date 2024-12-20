"""
forms.py
Author: Asad Soomro
Email: asoomro@bu.edu

This file defines the Django forms used in the Rock City web application. These forms
provide user-friendly interfaces for creating and updating models such as comments,
newsletter posts, profiles, and routes.
"""
from django import forms
from .models import Comment, NewsletterPost, Profile, Route

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'parent': forms.HiddenInput()
        }

class NewsletterPostForm(forms.ModelForm):
    class Meta:
        model = NewsletterPost
        fields = ['title', 'content', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'location', 'difficulty', 'type', 'setter_name', 'date_set', 'replacement_date', 'status', 'image']
