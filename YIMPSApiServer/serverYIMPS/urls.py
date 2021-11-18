from django.urls import path
from . import views
from .routes import postRoute
from .routes import profileRoute

urlpatterns = [
    path('', views.index , name ='index'),
    path('getposts',postRoute.getAllPost,name='getPost'),
    path('createpost',postRoute.createPost,name = 'createPost'),
    path('request-to-scrim/<str:pk>',postRoute.reqToScrim,name='reqToScrim'),
    path('createUser',profileRoute.creteProfile,name='creteProfile'),
]