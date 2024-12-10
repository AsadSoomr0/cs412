from django.contrib import admin
from .models import *

admin.site.register(Route)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Vote)


class NewsletterPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'likes_count')

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = 'Likes Count'

admin.site.register(NewsletterPost, NewsletterPostAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'date_created')
    fields = ('user', 'profile_picture', 'bio')




