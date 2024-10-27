from django.db import models
from django.utils import timezone
# Create your models here.

from django.db import models
from django.urls import reverse

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
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = [
            friend.profile2 if friend.profile1 == self else friend.profile1
            for friend in friends
        ]
        return friend_profiles

    
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