from __future__ import unicode_literals

from django.db import models
from django.forms import CharField, Form, PasswordInput

from django.contrib.auth.models import User

# Create your models here.

#------------Models used in FORMS------------# 
class AppCodeFile(models.Model):
    My_file = models.FileField() # Selected File 

'''class UpdateUser(models.Model):
    first_name = models.CharField(max_length =254 )
    last_name = models.CharField(max_length =254 )
    email = models.EmailField()'''

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    # http://www.tangowithdjango.com/book17/chapters/login.html
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    appinventorLogin = models.CharField(max_length =254 )

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username    
        
#------------Models used in DDBB------------#

# https://docs.djangoproject.com/en/dev/ref/models/fields/
class Users(models.Model):
    userID = models.IntegerField(primary_key=True) # user_id
    projects = models.ManyToManyField('Projects') # The user can load and analyze multiple projects
    #userFolder = localpath+username 

class Projects(models.Model):
    projectName = models.TextField(primary_key=True) # user.id_filename.name
    screens = models.ManyToManyField('Screens') # The project can include multiple screens
    projectProperties = models.TextField() # Project properties
    #totalScore = models.IntegerField() # Project general score. 0 = not scored yet
    
class Screens(models.Model):
    scrID = models.TextField(primary_key=True) # user.id_filename.name_Screen number
    bky = models.TextField() # Blockly info
    scm = models.TextField() # Screen Description
    

    

    

