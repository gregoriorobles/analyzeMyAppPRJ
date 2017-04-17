import zipfile
import shutil
import os
import xml.etree.ElementTree as ET

from .errors import fileFormatError
from .models import *
from django.conf import settings
from posixfile import fileopen
from __builtin__ import False


def unzip(source_file, dest_dir):
    '''
        Unzips the source_file in the dest_dir folder. 
        
        Input: 
            - source_file (In Memory File)
            - dest_dir (str)
        Output: 
            - None
        
    '''
    z = zipfile.ZipFile(source_file,"r")
    zl = z.namelist()
    z.extractall(dest_dir)
    z.close()

def doLoadCode(username, user_id, file):
    '''
        Load the code before analyze it.
        If the project doesn't exists, creates a new folder with the uncompressed info. 
        
        Input: 
            - username (str)
            - user_id (str)
            - file (In Memory File)
        Output: 
            - filecontent (str): project.properties content if OK, empty if Error
            - msg (str): info for the user
    '''
    
    if zipfile.is_zipfile(file):
        # Unzip the file in the user's folder. 
        folder = os.path.join(settings.SAVEDPROJECTS_ROOT,str(user_id)+'_'+username)
        
        file_path = os.path.join(folder,file.name)  
        if os.path.exists(file_path):
            # No actions
            print 'Project %s already exists' % file
            filecontent = 'existingProject'
            msg  = 'Project %s already exists' % file
            
        else:
            print 'New project %s created' % file
            unzip(file, file_path)
            # Read the Properties doc
            f = open(os.path.join(file_path,'youngandroidproject','project.properties'),'r')
            filecontent = f.read()
            f.close()
            msg  = 'New project %s created' % file

    else:
        raise fileFormatError('Error. Not zip file selected')
   
    return (filecontent,msg)

def formatProjectList (projectList):
    '''
        Format the list by deleting the user_id of the project names (user_id + _ + projectname)
        Input:
            - projectList (list)
        Output:
            - projectListFormatted {'Label1':'Project1', 'Label2': 'Project2'} where labels = projectlist
    '''
    projectListFormatted = {}
    
    for p in projectList:
        project =  p.split('_', 1)
        #projectName =  os.path.splitext(project[1])
        projectListFormatted[p] = project[1] #Name[0]
            
    return projectListFormatted

def doLoadScreens(username, user_id,project):
    '''
        Analyze the project and save the screens info into data base.
        Each screen has: 
                * scrID (int) : screen number
                * bky (str) : blockly info
                * scm (str) : screen Description
        
        Input: 
            - username (str)
            - user_id (int)
            - project (str.aia)
            
        Output: 
            - msg (str): info for the user
    '''
    
    
    appinventorLogin = UserProfile.objects.filter(user = user_id).values_list('appinventorLogin',flat=True)[0]
    projectName =  os.path.splitext(project)[0] # .without .aia
   
    prjFolder = os.path.join(settings.SAVEDPROJECTS_ROOT,str(user_id)+'_'+username,project,'src','appinventor','ai_'+appinventorLogin,projectName)
    
    selectedProject = Projects.objects.get(users__userID = user_id,projectName = str(user_id)+'_'+project)
    
    if os.path.exists(prjFolder):
        
        prjListDir  = os.listdir(prjFolder)
        nScreens = len(prjListDir)/2 # .bky + .scm
        
        # Read the content of the screen files and save them into ddbb
        for n in prjListDir:
            filename, filextension = os.path.splitext(n)
            if filextension == '.bky':
            
                bkyN = filename + '.bky'
                f = open(os.path.join(prjFolder,n),'r')
                filecontent = f.read()
                f.close()
            
                scmN =  filename + '.scm'
                f = open(os.path.join(prjFolder,scmN),'r')
                filecontent2 = f.read()
                f.close()
            
                scr_id = str(user_id) + '_' + projectName + '_' + str(n) #user.id_filename.name_Screen number
                scr = Screens(scrID=scr_id,bky=filecontent,scm=filecontent2)
                scr.save()
                selectedProject.screens.add(scr)
                selectedProject.save()
              
        '''for n in range (1,nScreens+1):
            
            bkyN = 'Screen'+str(n)+'.bky'
            f = open(os.path.join(prjFolder,bkyN),'r')
            filecontent = f.read()
            f.close()
            
            scmN =  'Screen'+str(n)+'.scm'
            f = open(os.path.join(prjFolder,scmN),'r')
            filecontent2 = f.read()
            f.close()
            
            scr_id = str(user_id) + '_' + projectName + '_' + str(n) #user.id_filename.name_Screen number
            scr = Screens(scrID=scr_id,bky=filecontent,scm=filecontent2)
            scr.save()
            selectedProject.screens.add(scr)
            selectedProject.save()
        '''  
    return str(prjFolder)  


def parseXML(file):
    
    '''
        Extract the xml info

        Input: 
            - file (str)
     
        Output: 
            - tree (ElementTree)
    '''
    
    tree = ET.fromstring(file)
    
    return tree    
