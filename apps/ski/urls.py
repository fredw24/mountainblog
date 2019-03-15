from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createUser$', views.createUser),
    url(r'^loginresult$', views.login),
    url(r'^success$', views.success),
    url(r'^newMountain$', views.create),
    url(r'^createprocess$', views.createprocess),
    url(r'^blog$', views.blogs),
    url(r'^blogprocess$', views.blogprocess),
    url(r'^editblog$', views.blogedit),
    url(r'^blogeditprocess$', views.blogeditprocess),
    url(r'^deleteblog$', views.deleteblog),
    url(r'^view$', views.viewing),
    url(r'^like$', views.like),
    url(r'^unlike$', views.unlike),
    url(r'^back$', views.back),
    url(r'^logout$', views.logout)
]