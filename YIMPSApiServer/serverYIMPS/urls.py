from django.urls import path
from . import views
from .routes import postRoute
from .routes import profileRoute

urlpatterns = [
    path('', views.index , name ='index'),
    path('getallposts',postRoute.getAllPost,name='getPost'),
    path('createpost',postRoute.createPost,name = 'createPost'),
    path('request-to-scrim/<str:pk>',postRoute.reqToScrim,name='reqToScrim'),
    path('createUser',profileRoute.creteProfile,name='creteProfile'),
    path('getpost/<str:pk>',postRoute.getPostById,name='getPostById'),
    path('getposts-sorted',postRoute.getPostSort,name='getPostSort'),
    path('login',profileRoute.login,name='login'),
    path('editProfile',profileRoute.editProfile,name='editProfile'),
]

