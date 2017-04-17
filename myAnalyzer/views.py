from django.shortcuts import render
from django.template import loader, Context, RequestContext, Template
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate,get_user_model
from collections import namedtuple

from .forms import SelectFileForm,UpdateUserForm,UserProfileForm,CreateUserForm
from .parser import doLoadCode,formatProjectList, doLoadScreens
from .errors import fileFormatError,validationError
from .models import *
from .scoreMyApp import *
from .scoreMyAppMessages import *

import os


'''username
first_name
last_name
email
password
groups
user_permissions
is_staff
is_active
is_superuser
last_login'''

# Create your views here.

#------------Login------------#
def showLoginPage(request):
    '''
        Login page - Main
    '''
    if request.method == 'GET':
        # Main page shows the login form 
        t = loader.get_template('login.html')
        #t = loader.get_template('login.html')
        form = AuthenticationForm()
        c = {'form': form}
        response = HttpResponse(t.render(c,request)) 
        return response
    elif request.method == 'POST':
        # After receive the authentication data, the user is authenticated
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # User not disabled by administrator
                login(request, user)
                # Once logged, the user is redirected to /userprofile 
                return HttpResponseRedirect('userprofile/')
            else:
                # User disabled, show the main page with the info. Form is empty again
                t = loader.get_template('login.html')
                form = AuthenticationForm()
                msg = 'Your user has been disabled, please contact with the administrator'
                c = {'form': form, 'msg':msg}
                response = HttpResponse(t.render(c,request)) 
                return response
        else:
            # Login failed, show the main page with the info. Form is empty again
            t = loader.get_template('login.html')
            form = AuthenticationForm()
            msg = 'Login failed, please try it again'
            c = {'form': form, 'msg':msg}
            response = HttpResponse(t.render(c,request)) 
            return response
    else:
        print 'ERROR - Request Method - views.showLoginPage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))

#------------Logout------------#
def showLogoutPage(request):
    '''
        Logout page
    '''
    if request.method == 'GET':
        # The user has requested logging out
        logout(request)
        t = loader.get_template('logout.html')
        c = {}
        response = HttpResponse(t.render(c,request)) 
        return response
    else:
        print 'ERROR - Request Method - views.showLogoutPage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
#------------User Profile------------#
def showUserProfilePage(request):
    '''
        User page - Options displayed:
            - List of user projects 
            - Add new project
            - Modify user profile
            
    '''
    if request.method == 'GET':
        # Show available options
        if request.user.is_authenticated():
            t = loader.get_template('userprofile.html')
            c = {}
            response = HttpResponse(t.render(c,request)) 
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (showUserProfilePage.GET). Redirect to /login'          
            return HttpResponseRedirect('/')     
    else:
        # No POST or HEAD methods available in this view
        print 'ERROR - Request Method - views.showUserProfilePage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))

#------------Create Profile------------#
def showCreateProfilePage(request):
    '''
        Create user profile: username, first_name, last_name, email, pasword, appinventorLogin
            
    '''
    if request.method == 'GET':
        if request.user.is_authenticated():
            # If the user is authenticated, redirect to login 
            print 'User authenticated (showCreateProfilePage.GET). Redirect to /login'            
            return HttpResponseRedirect('/') 
        else:
            t = loader.get_template('createprofile.html')
            form = CreateUserForm({})
            c = {'form': form}
            response = HttpResponse(t.render(c,request)) 
            return response
              
    elif request.method == 'POST':
        # Update the data
        if request.user.is_authenticated():
           # If the user is authenticated, redirect to login 
            print 'User not authenticated (showUpdateProfilePage.GET). Redirect to /login' 
            return HttpResponseRedirect('/')
        else:
             # Load the POST data
            form = CreateUserForm(request.POST)
                                 
            if form.is_valid():
                try:
                    if request.POST['password1'] != request.POST['password2']:#check if both pass first validation
                        raise validationError("Passwords don't match")
                    try:
                        username = User.objects.get(username=request.POST['username'])
                        if username:
                            raise validationError('Username already exists')  
                    except ObjectDoesNotExist:
                        print "Username doesn't exists in database" # Continue
                    
                    new_user = User.objects.create_user(request.POST['username'],
                                          request.POST['email'],
                                          request.POST['password1'])
                    new_user.first_name = request.POST['first_name']
                    new_user.last_name = request.POST['last_name']
                    new_user.appinventorLogin = request.POST['last_name']
                    new_user.save()    
                    # Update the appinventorLogin
                    new_id = new_user.pk
                    new_profile = UserProfile.objects.create(user_id= new_id,appinventorLogin=request.POST['appinventorLogin'])
                    new_profile.save()
                    
                    msg = 'Your profile has been created successfully. Login to continue'
                    c = {'form': form,'msg':msg,}
                except validationError as ve:
                    errormsg = ve.message
                    c = {'form': form,'errormsg':errormsg,}
  
            else:
                # Not valid data
                errormsg = 'Sorry, your profile couldn"t been created successfully. Please, contact the Administrator'
                c = {'form': form,'errormsg':errormsg,}
            t = loader.get_template('createprofile.html')

            response = HttpResponse(t.render(c,request)) 
            return response
    else:
        #No POST or HEAD methods available in this view
        print 'ERROR - Request Method - views.showUpdateProfilePage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
    

#------------Update Profile------------#
#https://docs.djangoproject.com/en/1.10/topics/db/transactions/
@transaction.atomic
def showUpdateProfilePage(request):
    '''
        Update user profile: first_name, last_name, email, appinventorLogin
            
    '''
    if request.method == 'GET':
        # Available options
        if request.user.is_authenticated():
            
            t = loader.get_template('updateprofile.html')
            # Load user's values
            data = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email':request.user.email}
            form = UpdateUserForm(data)
            
            dataPF = {'appinventorLogin':UserProfile.objects.filter(user = request.user.id).values_list('appinventorLogin',flat=True)[0]}
            profile_form = UserProfileForm(dataPF)
                
            c = {'form': form,'profileform':profile_form,}
            response = HttpResponse(t.render(c,request)) 
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (showUpdateProfilePage.GET). Redirect to /login'            
            return HttpResponseRedirect('/')   
          
    elif request.method == 'POST':
        # Update the data
        if request.user.is_authenticated():
            # Load the POST data
            data = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email':request.user.email}
            form = UpdateUserForm(request.POST, initial=data)
            
            profile_form = UserProfileForm(request.POST)
            
            if form.is_valid() and profile_form.is_valid():
                if form.has_changed():
                    print 'User: %s -> The following fields changed: %s' % (request.user.username,', '.join(form.changed_data))
                    for c in form.changed_data:
                        new = form.cleaned_data[c]
                        print '%s NEW: %s  OLD: %s' % (c,new,getattr(request.user, c)) 
                        setattr(request.user, c, new) 
                        request.user.save()
                
                if UserProfile.objects.filter(user = request.user.id).count() > 0:  
                    # Update the appinventorLogin
                    profile = UserProfile.objects.get(user = request.user.id)
                else: 
                    # Not appinventorLogin saved yet
                    profile = profile_form.save(commit=False)
                    profile.user = request.user
                profile.appinventorLogin = profile_form.cleaned_data['appinventorLogin'] 
                # Now we save the UserProfile model instance.
                profile.save()

                msg = 'Your profile has been updated successfully'
                
            else:
                # Not valid data
                msg = 'Sorry, your profile couldn"t been updated successfully. Please, contact the Administrator'
                
            t = loader.get_template('userprofile.html')
            # Load user's values
            data = {'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email':request.user.email}
            form = UpdateUserForm(data)
            c = {'form': form,'profileform':profile_form,'msg':msg,}
            response = HttpResponse(t.render(c,request)) 
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (showUpdateProfilePage.GET). Redirect to /login' 
            return HttpResponseRedirect('/')
    else:
        #No POST or HEAD methods available in this view
        print 'ERROR - Request Method - views.showUpdateProfilePage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
#------------User Projects------------#
def showUserProjectsPage(request):
    '''
        Saved user's projects 
            
    '''
    if request.method == 'GET':
        # Available options
        if request.user.is_authenticated():
            # Load the name of all projects saved by the user
            
            if Users.objects.filter(userID = request.user.id).count() > 0:
                # The user has saved projects (analyzed or not) in the data base
                print 'User %s already has saved some projects' % request.user.username
                projectList = Projects.objects.filter(users__userID = request.user.id).values_list('projectName',flat=True)
                #Convert list into dictionary with formatted names
                userProjects = formatProjectList(projectList)
            else:
                #The user hasn't saved projects in the data base yet 
                print 'User %s has not saved projects yet' % request.user.username
                userProjects = ''
                
            t = loader.get_template('userprojects.html')
            c = {'userProjects':userProjects}
            response = HttpResponse(t.render(c,request)) 
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (showUserProjectsPage.GET). Redirect to /login'          
            return HttpResponseRedirect('/')     
    else:
        #No POST or HEAD methods available in this view
        print 'ERROR - Request Method - views.showUserProjectsPage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
#------------Download------------#
def showDownloadPage(request):
    '''
        Download page - Select the app code to analyze.
        The user can add a new project and analyze it 
    '''
    if request.method == 'GET':

        if request.user.is_authenticated():
            # If the user is logged, shows a form to select a new file to open
            t = loader.get_template('loadAppCode.html')
            # Empty form
            form = SelectFileForm()
            c = {'form': form}
            response = HttpResponse(t.render(c,request))            
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (showDownloadPage.GET). Redirect to /login'          
            return HttpResponseRedirect('/')
    
    elif request.method == 'POST':
        # Received data from a logged user
        try:
            if request.user.is_authenticated(): 
                form = SelectFileForm(request.POST,request.FILES)
                # Once we have a file, we display the content in the web to verify it's loaded
                if form.is_valid():
                     
                    filename = form.cleaned_data['My_file'] 
                    '''t = loader.get_template('loadAppCode.html')'''
                                    
                    (filecontent,msg) = doLoadCode(request.user.username,request.user.id, filename)
                    if filecontent != 'existingProject':      
                        # Save the data in data base
                        if Users.objects.filter(userID = request.user.id).count() > 0:
                            # The user already exists in User table. Add the Project
                            print 'User %s already has saved some projects' % request.user.username
                            user = Users.objects.get(userID = request.user.id)
                        else:
                            #The user doesn't exists in User table. Create and Add the Project
                            print 'User %s has not saved projects yet' % request.user.username
                            user = Users(request.user.id)
                            user.save()
                        # Save the project data in data base
                        newProjectName = str(request.user.id)+'_'+filename.name
                        newProject = Projects(projectName = newProjectName,projectProperties = filecontent)
                        newProject.save()
                        user.projects.add(newProject)
                        user.save()
                    
                        # Read the screens info and save them in ddbb
                        msj = doLoadScreens(request.user.username, request.user.id, filename.name)
        
                        ''''c = {'form': form, 'msg':msg, 'fileName': filename, 'codeText':filecontent}
                        response = HttpResponse(t.render(c,request))                                  
                        return response'''
                        request.POST['project'] = filename.name
                        return showUserAnalyzeProjectsPage(request)
                else:
                    print 'ERROR - Request Method - views.showDowloadPage(request)'
                    t = loader.get_template('error.html')
                    return HttpResponse(t.render(request))
            else:
                # If the user is not authenticated, redirect to login 
                print 'User not authenticated (showDownloadPage.POST). Redirect to /login'          
                return HttpResponseRedirect('/')
        
        except fileFormatError as fe:
            filecontent = fe.message
            print 'ERROR - Request Method - views.showUserProjectsPage(request)'
            msg = 'Revise your file format. Only .aia files could be uploaded'
            c = {'msg': msg}
            t = loader.get_template('error.html')
            return HttpResponse(t.render(c,request))
        except Exception as e:
            print 'ERROR - Request Method - views.showUserProjectsPage(request)'
            print e
            t = loader.get_template('error.html')
            return HttpResponse(t.render(request))
    else:
        print 'ERROR - Request Method - views.showDowloadPage(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
#------------Analyze Project------------#
def showUserAnalyzeProjectsPage(request):
    '''
        Analyze selected project
            
    '''
    if request.method == 'POST':
        # Available options
        if request.user.is_authenticated():
            t = loader.get_template('analyzeAppCode.html')
            project = request.POST['project'] #.split('_', 1)[1]
            prjName =  os.path.splitext(project)[0]
            
            # Project already analyzed? -> Not implemented
            # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
            '''points = Projects.objects.filter(users__userID = request.user.id,projectName = str(request.user.id)+ '_'+project).values_list('totalScore',flat=True)[0]
            if points > 0:
                print "Project already analyzed"
            else:
                # Project not analyzed yet. Let's separate the screens and save them into ddbb
                print "Project not analyzed"'''
    
            # Load selected project screens
            prjSelected = Projects.objects.get(users__userID = request.user.id,projectName = str(request.user.id)+ '_'+project)
            
            prjScreens = prjSelected.screens
            score = getScore(prjScreens) # Dict
            
            m = getScoreMsgs(score)
            
            score_resume = [score['ComponentLevels']['Score'],
                            score['ProgrammingLevels']['Score'],
                            score['ScreensLevels']['Score']]
            
            c = {'fileName': prjName,
                 'score': score_resume,
                 'general_score_msg': m.general_score_msg,
                 'comp_score_msg':m.comp_score_msg,
                 'progr_score_msg':m.progr_score_msg,
                 'sched_score_msg':m.sched_score_msg,
                 'comp_score_info':m.comp_score_info,
                 'progr_score_info':m.progr_score_info,
                 'sched_score_info':m.sched_score_info}
            
            response = HttpResponse(t.render(c,request)) 
            return response
        else:
            # If the user is not authenticated, redirect to login 
            print 'User not authenticated (UserAnalyzeProjects.GET). Redirect to /login'          
            return HttpResponseRedirect('/')     
    else:
    
        #No GET or HEAD methods available in this view
        print 'ERROR - Request Method - views.UserAnalyzeProjects(request)'
        t = loader.get_template('error.html')
        return HttpResponse(t.render(request))
    
