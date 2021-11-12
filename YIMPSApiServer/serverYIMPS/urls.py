from django.urls import path
from . import views
from .routes import postRoute

urlpatterns = [
    path('', views.index , name ='index'),
    path('getallposts',postRoute.getAllPost,name='getPost'),
    path('createpost',postRoute.createPost,name = 'createPost'),
    path('request-to-scrim/<str:pk>',postRoute.reqToScrim,name='reqToScrim'),
    path('getpost/<str:pk>',postRoute.getPostById,name='getPostById'),
]