from django.views import generic
from .models import Album
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView
)
from django.contrib.auth import logout
from .models import Album, Song
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
# authenticate takes username and password and verify the user is authenticate or not(build in)


class IndexView(generic.ListView):
    # class based view
    template_name = 'music/index.html'
    context_object_name = 'albums' # by default the class based view passed object_list but if u override this that way,now passes 'all_albums' instead of 'object_list'

    def get_queryset(self):
        # built in method to retirve all objects from model
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    # we can use model form instead of using fields in class based model
    # we don't need to specify template name because the html file is create by model_name_form.html
    model = Album # don't need to create form,the model itself create this
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):  # in class based view the form shows automatically updating format,you should nothing to do
    model = Album  # update view is same as create view,you don't need to define html rendering
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView): # here nothing you have to do,the class based model automatically delete this thing
    model = Album  # you don't need to get_object method because the id is handle from html template(index.html)
    # success_url = '/music/index/'

    def get_success_url(self):
        return reverse('music:index')  # return the index page after deleting the album


class UserFormView(View):  # for registration and then login this user automatically
    form_class = UserForm # the user form which is in forms.py file
    template_name = 'music/registration_form.html'

    # display blank form: you don't need to write condition of get,post
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False) # here create a instance of form,but not save in database
            username = form.cleaned_data['username']  # cleaned_data of username passed to username variable
            password = form.cleaned_data['password'] # cleaned data represent the fresh value from form
            user.set_password(password) # password set using function,because password is not a plain text
            user.save()

            # returns User objects if credentials are correct (for authentication)
            user = authenticate(username=username, password=password) # take the username and password
            if user is not None:  # if the user is exist in admin database
                if user.is_active:
                    login(request, user)  # login automatically if all conditions are ok
                    return redirect('music:index') # after successfully login then the index page redirect
                    # using render instead of using redirect and send user to the html,this also can happen for reg.
        return render(request, self.template_name, {'form': form})  # if form is not valid or user is not register in database then redirect the same registration form


def login_user(request): # after logout a valid user,then login shows a page for that a valid user can login
    # at that time,there are no relationship in build in user and our model Albums,for that reason if u logout and login
    # from another user you can show the albums of previous user (admin) in homepage
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                         password=cd['password'])
            if user is not None: # if user is in database
                if user.is_active:
                    login(request, user)  # login automatically,build in django function
                    return render(request, 'music/index.html')
                else:
                    return render(request, 'music/login.html')
            else:
                return render(request, 'music/login.html')

    return render(request, 'music/login.html')  # redirect to index.html page which is empty for this user


def logout_user(request):
    logout(request)    # this logout from django auth build in,logout works well,if u logout the user then it will logout from admin page also
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


'''
def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {    # if image file types is not valid then shows error
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {  # if the form is not valid
            "form": form,
        }
        return render(request, 'music/create_album.html', context)
'''


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id) # take th id
    try:
        selected_song = album.song_set.get(pk=request.POST['song']) # take the selected song via Post method which one is clicked
    except (KeyError, Song.DoesNotExist): # if keyError happens then shows the messages
        return render(request, 'music/detail.html'), {
            'album': album,
            'error_message': "You did not select a valid song",
        }
    else:
        selected_song.is_favorite = True # if the condition does not goes onto except block then the selected song is favorite goes on true and then save it
        selected_song.save()
        return render(request,'music/detail.html', {'album': album})

'''
This all one is function based view and previously described class based view

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
    DetailView,
    ListView
)
from .models import Album, Song
from django.http import Http404


def index(request):
    # you can use render or HttpResponse any of this
    all_albums = Album.objects.all()
    context = {
        'all_albums': all_albums
    }
    # return render(request,'music/index.html', {'all_albums': all_albums})
    return render(request, 'music/index.html',context) # actualy render works as same as HttpResponse,render is shortcut

def detail(request, album_id):
    # this parameter album_id takes from models.py file as a pk and transfer into urls.py file
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id) # take th id
    try:
        selected_song = album.song_set.get(pk=request.POST['song']) # take the selected song via Post method which one is clicked
    except (KeyError, Song.DoesNotExist): # if keyError happens then shows the messages
        return render(request, 'music/detail.html'), {
            'album': album,
            'error_message': "You did not select a valid song",
        }
    else:
        selected_song.is_favorite = True # if the condition does not goes onto except block then the selected song is favorite goes on true and then save it
        selected_song.save()
        return render(request,'music/detail.html', {'album': album})



#def detail(request, album_id):
   # try:
    #    album = Album.objects.get(pk=album_id)
    #except Album.DoesNotExist:
   #     raise Http404("Album does not exist")
    #return render(request, 'music/detail.html', {'album': album})

# instead of using this detail method,you can use the new detail method using get_object_or_404 instead of using try
# catch block

#def index(request):
 #   all_albums = Album.objects.all() # take all items from database
  #  template = loader.get_template('music/index.html') # takes the template using loader
   # context = {
        # create a dictionary to pass the all objects through all_albums
    #    'all_albums': all_albums
    #}
    #return HttpResponse(template.render(context, request)) # you can either use HttpResonse or return render


#def index(request):
 #   return HttpResponse("<h1>Welcome Home</h1>")

#def index(request):
 #   all_albums = Album.objects.all()
  #  html = ''
   # for album in all_albums:
        # add music url and album id and make a link then when you click the link it shows this web detail
    #    url = '/music/' + str(album.id) + '/'
       # html += '<a href="' + url + '">' + album.album_title + '</a><br>'
        # it shows album title and link onto album id
    #return HttpResponse(html)

#def detail(request, album_id):
 #   return HttpResponse("<h2>Details for Album id: " + str(album_id) + "</h2>")



class WebListView(ListView):
    template_name = 'websites/web_list.html'
    queryset = Album.objects.all()


class WebDetailView(DetailView):
    template_name = 'websites/web_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Album, id=id_)

'''
