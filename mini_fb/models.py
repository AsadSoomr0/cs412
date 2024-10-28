from django.db import models
from django.utils import timezone
# Create your models here.

from django.db import models
from django.urls import reverse
from django.db.models import Q


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_friends(self):
        friends = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friend_profiles = [
            friend.profile2 if friend.profile1 == self else friend.profile1
            for friend in friends
        ]
        return friend_profiles

    def add_friend(self, other):
        if self != other and not Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists():
            Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())
    
    def get_friend_suggestions(self):
        # Step 1: Collect IDs of the current profile's friends
        current_friend_ids = set()

        for friendship in Friend.objects.filter(profile1=self):
            current_friend_ids.add(friendship.profile2.pk)
        for friendship in Friend.objects.filter(profile2=self):
            current_friend_ids.add(friendship.profile1.pk)

        # Step 2: Gather friends of friends, excluding current friends and self
        friend_suggestion_ids = set()

        # Friends of friends through profile1
        for friendship in Friend.objects.filter(profile1__in=current_friend_ids):
            if friendship.profile2.pk != self.pk and friendship.profile2.pk not in current_friend_ids:
                friend_suggestion_ids.add(friendship.profile2.pk)

        # Friends of friends through profile2
        for friendship in Friend.objects.filter(profile2__in=current_friend_ids):
            if friendship.profile1.pk != self.pk and friendship.profile1.pk not in current_friend_ids:
                friend_suggestion_ids.add(friendship.profile1.pk)

        # Return Profiles based on friend suggestion IDs
        return Profile.objects.filter(pk__in=friend_suggestion_ids)
    
    def get_news_feed(self):
        # Get this profile's friends using the ORM
        friends = self.get_friends()

        # Filter for status messages by this profile or any friend
        feed = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-timestamp')  # Order by most recent first

        return feed
    
class StatusMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} - {self.timestamp}'
    
    def get_images(self):
        return Image.objects.filter(status_message=self) #Filters and returns all image objects linked to a given status message
    
class Image(models.Model):
    #Image model includes a file, a timestamp for when the image was uploaded, and a foreign key to link the image to a statusmessage
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id} for StatusMessage {self.status_message.id}"
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name} "   