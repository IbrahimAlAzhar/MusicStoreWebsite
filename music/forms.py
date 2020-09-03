from django import forms
from django.contrib.auth.models import User

from .models import Album, Song
# at that time,there are no relationship in build in user and our model Albums,for that reason if u logout and login
# from another user you can show the albums of previous user (admin) in homepage


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) # creating password explicitly which is not present in user(django build in)

    class Meta:
        # this class is override django build in model file aka admin file using username,email,password attributes
        model = User
        fields = ['username', 'email', 'password']  # override username,email,password

'''
class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']
'''
