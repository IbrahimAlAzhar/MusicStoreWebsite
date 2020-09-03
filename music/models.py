from django.db import models
from django.urls import reverse

# anytime you change something in database means attribute in class then just do two lines,
# one makemigrations then migrate command.


class Album(models.Model):
    # the attributes of Album
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.ImageField(upload_to='images/') # here we create album_logo is blank=true,but if i add
    # album logo then we handle this via form or python command line
    # MEDIA_URL = '/media/' , here in base directory where manage.py stores in this place we create a directory name media
    # MEDIA_ROOT = os.path.join(BASE_DIR,'media'),, and we create a sub directory in media so we add this in model's attribute like 'upload_to=images/'
    # and you have to add a new urlpatterns in website.url which one you add in settings file

    def get_absolute_url(self):
        # this method is using for when you submit the form  then this method ridirect to detail page
        return reverse('music:detail', kwargs={'pk': self.pk}) # in detail view that needs to album id for detail which one is pk

    def __str__(self):
        # here is a dunder string method when you see out about album in python shell then it shows the album title and
        # artist name alongside object name,this return term shows on admin site also
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    # this is the foreign key of the album class,the primary key of class album is id(build in) so the foreign key of
    # song is id,the activity of models.CASCADE is if the album is deleted then all related song is deleted
    album = models.ForeignKey(Album, on_delete=models.CASCADE) # the song from which album
    file_type = models.CharField(max_length=10) # file type is mp3 or avi
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title # here return the song_title
    # for that reason you need not to do migration because of method,it shows just song title in db or other places
