#Todo: Filefields Datatype to be changed

from django.db import models
#from djangotoolbox.fields import ListField, EmbeddedModelField
from mongoengine import *
import datetime
# Create your models here.
class Otp(Document):
    email = StringField()
    otp = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
class User(Document):
    #userid = models.CharField(max_length=70, blank= False, primary_key=True)
    username = StringField()
    email = StringField()
    password = StringField()    
    firstName = StringField()
    lastName = StringField()
    dob = StringField()
    address = StringField()
    pin = StringField()
    phone = StringField()
    addressproof = StringField()
    medicalstatus = StringField()
    userProjects = ListField(StringField())
    userOrganizations = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_by = StringField()
    status = StringField()
class Organization(Document):
   # organizationid = models.CharField(max_length=70, blank= False, primary_key=True)
    organizationName = StringField()
    organizationEmail = StringField()
    organizationLocation = StringField()    
    organizationPin = StringField()
    organizationLogo = StringField()
    #organizationProjects = models.ArrayField()
    organizationProjects = ListField(StringField())
    #organizationUsers = models.ArrayField()
    organizationUsers = ListField(StringField())
    organizationStatus = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_by = StringField()
    status = StringField()

class Project(Document):
    projectid = StringField()
    projectName = StringField()
    projectEmail = StringField()
    projectLocation = StringField()    
    projectPin = StringField()
    projectLogo = StringField()
    projectType = StringField()
    organizationId = StringField()
    users = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_by = StringField()
    status = StringField()
class UserProjectRole(Document):
    userid = StringField()
    projectid = StringField()
    organizationid = StringField()
    Role = StringField()
    userStatus = StringField()
    approver_id= StringField()
    
