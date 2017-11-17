from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^loggedin$', views.loggedin),
    url(r'^addappointment/(?P<number>\d+)/add$', views.add),
    url(r'^task/(?P<number>\d+)/edit$', views.abouttoedit),
    url(r'^task/(?P<number>\d+)/doneupdate$', views.edit),
    url(r'^task/(?P<number>\d+)/delete$', views.delete),
    url(r'^logout$', views.logout),
]
