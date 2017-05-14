from django.conf.urls import url

from fiend.jobs import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
