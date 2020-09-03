from django.contrib import admin
from .models import Album, Song

# save the models into admin site
admin.site.register(Album)
admin.site.register(Song)
