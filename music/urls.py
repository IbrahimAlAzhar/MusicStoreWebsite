from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'music'
# whenever you use the any url name in this urlpatterns if the same url name has in other urls.py file then you have to
# use app name for identify the specific url
urlpatterns = [
    # path('', WebListView.as_view(), name='web-list'),
    url(r'^$', views.IndexView.as_view(), name='index'), # this means empty path using regular expression,r means regular expression,^ is start
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # symbol and $ is end symbol
    # path('album_id/', views.detail, name='detail'),
    # it also working with url and re_path,here takes any regular expression means any integer value
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^login/$', views.login_user, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'), # this build in logout works on admin logout
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'), # /music/<album_id>/,using pk(build in) in class based view instead of using album_id
    # this url works on regular expression,r means regular expression,then takes album id 0 to 9,then + means take
    # number as u can wish,then $ sign means ending symbol
    # path('<int:id>/', WebDetailView.as_view(), name='web-detail'), # /music/<album_id>/favorite
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # music/album/add
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    # music/album/2
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    # music/album/2/delete
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
]