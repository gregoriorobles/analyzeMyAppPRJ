from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Users) #Users available in Admin site
admin.site.register(Projects) #Users available in Admin site
admin.site.register(Screens) #Users available in Admin site

