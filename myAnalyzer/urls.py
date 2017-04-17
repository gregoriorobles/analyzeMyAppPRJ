from django.conf.urls import url

from . import views

urlpatterns = [
               url(r'^login/', views.showLoginPage),
               url(r'^logout/', views.showLogoutPage),
               url(r'^createprofile/', views.showCreateProfilePage),
               url(r'^userprofile/', views.showUserProfilePage),
               url(r'^download/', views.showDownloadPage),
               url(r'^updateprofile/', views.showUpdateProfilePage),
               url(r'^userprojects/', views.showUserProjectsPage),
               url(r'^analyze/', views.showUserAnalyzeProjectsPage),
               url(r'^$', views.showLoginPage),
               ]
