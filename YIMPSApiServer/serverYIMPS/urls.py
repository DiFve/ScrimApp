from django.urls import path
from . import views
from .routes import homeRoute,postRoute,teamRoute,profileRoute

urlpatterns = [
    path('', views.index , name ='index'),

    path('getNextFiveMatch/<str:pk>',homeRoute.getNextFiveMatch,name='getNextFiveMatch'),
    #postRoute
    
    path('getallposts',postRoute.getAllPost,name='getPost'),
    path('createpost',postRoute.createPost,name = 'createPost'),
    path('request-to-scrim/<str:pk>',postRoute.reqToScrim,name='reqToScrim'),
    path('getposts-sorted',postRoute.getPostSort,name='getPostSort'),
    path('getpost/<str:pk>',postRoute.getPostById,name='getPostById'),
    path('test-averagerank/<str:pk>',postRoute.getAvgRank,name='getAvgRank'),
    path('post/<str:pk>/accept-request',postRoute.acceptReq,name='acceptReq'),
    path('get-match/<str:pk>',postRoute.getAllUserPost,name='getAllTeamPost'),
    path('post/<str:pk>/reject-request',postRoute.rejectReq,name='rejectReq'),
    
    #teamRoute
    path('createteam',teamRoute.createTeam,name='createTeam'),
    path('getteam/<str:pk>',teamRoute.getTeam,name='getTeam'),
    path('addmember/<str:pk>',teamRoute.addMember,name='addMember'),
    path('removemember/<str:pk>',teamRoute.removeMember,name='removeMember'),
    path('editteam/<str:pk>',teamRoute.editTeam,name='editTeam'),
    path('getTeamImage/<str:pk>',teamRoute.getTeamImage,name='getTeamImage'),
    path('setTeamImage',teamRoute.setTeamImage,name='setTeamImage'),




    #profileRoute
    path('createUser',profileRoute.creteProfile,name='creteProfile'),
    path('login',profileRoute.login,name='login'),
    path('editProfile',profileRoute.editProfile,name='editProfile'),
    path('getUserInfoByID/<str:pk>',profileRoute.getUserInfoByID,name='getUserInfoByID'),
    path('getUserInfoByName/<str:pk>',profileRoute.getUserInfoByName,name='getUserInfoByName'),
    path('getProfileImage/<str:pk>',profileRoute.getProfileImage,name='getProfileImage'),
    path('setProfileImage',profileRoute.setProfileImage,name='setProfileImage')
]

