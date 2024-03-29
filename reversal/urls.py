from django.urls import path

from . import views

app_name = 'reversal'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('app', views.app, name='app'),
    path('prompt', views.prompt, name='prompt'),
    path('about', views.about, name='about'),
]