from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/',views.home,name='home'),
    path('AttributeAuthorityLogin/',views.AttributeAuthorityLogin,name='AttributeAuthorityLogin'),
    path('userregistration/',views.userregistration,name='userregistration'),
    path('UsersLogin/',views.UsersLogin,name='UsersLogin'),
    path('Logout/',views.Logout,name='Logout'),
    path('useractivation/',views.useractivation,name='useractivation'),
    path('activate/<int:id>/',views.activate,name='activate'),
    path('viewactiveusers/',views.viewactiveusers,name='viewactiveusers'),
    path('ownerregistration/',views.ownerregistration,name='ownerregistration'),
    path('ownerlogin/',views.ownerlogin,name='ownerlogin'),
    path('uploadfile/',views.uploadfile,name='uploadfile'),
    path('myfiles/',views.myfiles,name='myfiles'),
    path('encryptedindex/',views.encryptedindex,name='encryptedindex'),
    path('csplogin/',views.csplogin,name='csplogin'),
    path('getsearch/',views.getsearch,name='getsearch'),
    path('searchrequest/',views.searchrequest,name='searchrequest'),
    path('getsearchverification/<int:id>',views.getsearchverification,name='getsearchverification'),
    path('VerificationAuthorityLogin/',views.VerificationAuthorityLogin,name='VerificationAuthorityLogin'),
    path('searchaccessrequest/',views.searchaccessrequest,name='searchaccessrequest'),
    path('verify/<int:id>',views.verify,name='verify'),
    path('myrequests/',views.myrequests,name='myrequests'),
    path('verifiedrequests/',views.verifiedrequests,name='verifiedrequests'),
    path('sendresults/<int:id>',views.sendresults,name='sendresults'),
    path('verifiedresults/',views.verifiedresults,name='verifiedresults'),
    path('download/<int:id>/',views.download,name='download'),
    path('viewdownloads/',views.viewdownloads,name='viewdownloads'),
    path('allsearchrequests/',views.allsearchrequests,name='allsearchrequests'),
   



    


    

]