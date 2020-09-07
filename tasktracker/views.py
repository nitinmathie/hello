# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
from tasktracker.models import *
from tasktracker.Serializers import *
from rest_framework.decorators import api_view
from rest_framework_mongoengine import viewsets
from bson import ObjectId
import bcrypt
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from bson.json_util import dumps
#user registration
@api_view(["POST"])
def userregistration_view(request):
    if request.method == 'POST':
        password= request.data['password'].encode('utf-8')
        pwdhash= bcrypt.hashpw(password, bcrypt.gensalt())
        #pwdhashencode = pwdhash.encode('utf-8')
        request.data['password']=pwdhash.decode('utf-8')
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            username = request.data['username']
            usercount = User.objects.filter(username=username).count()
            if usercount>=1:
                return Response(request.data['username']+' exists' + ' Choose another username')
            else:                
                user = serializer.save()
                #bcrypt.checkpw(password,pwdhash)
                data['response'] = "Successfully registered new user."
                data['email'] = user.email
                data['username'] = user.firstName
        else:
            data['username'] = request.data['password']
            #data = serializer.errors
        return Response(data)
#generate otp and send otp
@api_view(["POST"])
def gensend_otp(request):
    if request.method == 'POST':
        email = request.data['email']
        otp = mailotp(email)        
        request.data['otp'] = otp
        otpserializer = OtpSerializer(data=request.data)
        if otpserializer.is_valid():
            try :
                otps = Otp.objects.filter(email=email)
                if otps.count()>=1:
                    otps.delete()
                otp = otpserializer.save()
            except :
                otp = otpserializer.save()
        try:
            otpreceived = mailotp(email)            
            return Response(otpreceived)
        except:
            return Response("Error")
@api_view(["POST"])
def verify_otp(request):
    if request.method == 'POST':
        email = request.data['email']
        otp = request.data['otp']
        otps = Otp.objects.filter(email=email).order_by('-created_at')
        if otps.count()>=1:
            verifyotp = otps[0]
            if str(otp)==str(verifyotp.otp):
                return Response(1)
            else:
                return Response(otp)

        else:
           return Response("Otp has never been generated")
        #return Response("")
#mail otp
def mailotp(mailid):

    from_address = 'nithunitin@gmail.com'

    to_address = str(mailid)

    message = MIMEMultipart('Foobar')

#    epos_liggaam['Subject'] = 'Foobar'

    message['From'] = from_address

    message['To'] = to_address
    otp = otpgenerator()
    content = MIMEText(str(otp), 'plain')

    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(from_address, 'N1t!nwonffa')

    mail.sendmail(from_address,to_address, message.as_string())

    mail.close()
    return otp
#    except:
#        return Response("MailError")
#otp generation
def otpgenerator():    
    #if request.method == 'POST':
    #email= request.data['email']
    otp = randint(999,10000)        
    return otp
#user login
@api_view(["POST"])
def userlogin_view(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        data = {}
        userResponse ={}
        try:
            pwd = user.password.encode('utf-8')
            password = password.encode('utf-8')    
            x = bcrypt.checkpw( password, pwd)
            data['isSuccesful']=x 
            userResponse['email'] =user.email
            userResponse['firstname'] =user.firstName
            #userResponse['projects']=user.userProjects
            #userResponse['organizations']=user.userOrganizations
            data['user'] = userResponse
        except:
            return Response("Error")
        return JsonResponse(data, safe=False)
#organization registration
@api_view(["POST"])
def organizationregistration_view(request, userid):
    if request.method == 'POST':
        #creating serializer data
        request.data['created_by']=userid
        userlist = []
        userlist.append(userid)
        request.data['organizationUsers']= userlist
        organizationserializer = OrganizationSerializer(data=request.data)    
        data = {}
        #validate serializer
        if organizationserializer.is_valid():
            #uniqueness of organizationname
            organizationname = request.data['organizationName']
            organizationcount = Organization.objects.filter(organizationName=organizationname).count()
            if organizationcount>=1:
                return Response(request.data['organizationName']+' exists' + ' Choose another username')
            else:                
                organization = organizationserializer.save()                
                data['response'] = "Successfully added new Organization."
                organization = Organization.objects.get(organizationName=organizationname)
                data['id'] = str(organization.id)
                #save the organization info in users collection
                user = User.objects.get(id=ObjectId(userid))
                organizationlist=user.userOrganizations
                organizationlist.append(str(organization.id))
                user.update(set__userOrganizations=organizationlist)
                data['x'] = request.data['created_by']
        else:
            data = organizationserializer.errors
        return Response(data)
#Update Organization
@api_view(["POST"])
def updateorganization_view(request, userid, organizationid):
    if request.method == 'POST':        
        try:
            organization = Organization.objects.get(id=ObjectId(organizationid))
        except Organization.DoesNotExist:
            return Response("no record")
            
        #if organization.count()>0:            
        request.data['updated_by']=userid
        #organiztion_data = JSONParser().parse(request)
        organizationserializer = OrganizationSerializer(organization,data= request.data)
        if organizationserializer.is_valid():
            organizationserializer.save()
        else:
            return Response(organizationserializer.errors)
        return Response("Organization information Updated Succesfully")
#Deactivate Organization
@api_view(["POST"])
def deleteorganization_view(request, userid, organizationid):
    if request.method == 'POST':        
        try:
            organization = Organization.objects.get(id=ObjectId(organizationid))
           # projects = organization.projects
           # for i in projects:
           #     project = Project.objects.get(id=ObjectId(i))
           #     project.delete()
             #also deactivate the user from userprojectrole table   
        except Organization.DoesNotExist:
            return Response("no record")
        request.data['updated_by']=userid
        request.data['status']='0'
        #organiztion_data = JSONParser().parse(request)
        organizationserializer = OrganizationSerializer(organization,data= request.data)
        if organizationserializer.is_valid():
            organizationserializer.save()
        else:
            return Response(organizationserializer.errors)
        return Response("Organization deactivated Succesfully")
        #organization.delete()
        #return Response({'message': 'Deleted the organization and its projects'})        
# Project Registration
@api_view(["POST"])
def projectregistration_view(request, userid, organizationid):
    if request.method == 'POST':
        #creating serializer data
        request.data['created_by']=userid
        request.data['organizationId']=organizationid
        userlist = []
        userlist.append(userid)
        request.data['users']= userlist
        projectserializer = ProjectSerializer(data=request.data)    
        data = {}
        #validate serializer
        if projectserializer.is_valid():
            #uniqueness of organizationname
            projectname = request.data['projectName']
            projectcount = Project.objects.filter(projectName=projectname).count()
            if projectcount>=1:
                return Response(request.data['projectName']+' exists' + ' Choose another username')
            else:                
                project = projectserializer.save()                
                data['response'] = "Successfully added new project to the organization."
                project = Project.objects.get(projectName=projectname)
                data['id'] = str(project.id)
                #save the project info in users collection
                user = User.objects.get(id=ObjectId(userid))
                projectlist=user.userProjects
                projectlist.append(str(project.id))
                user.update(set__userProjects=projectlist)
                data['x'] = request.data['created_by']
                #save the project info in organization collection
                organization = Organization.objects.get(id=ObjectId(organizationid))
                projectlist=organization.organizationProjects
                projectlist.append(str(project.id))
                organization.update(set__organizationProjects=projectlist)
                #save status as admin
                #create userproject role searializer and save it.
                userprojectrole = {'userid':userid, 'projectid':str(project.id),
                                   'organizationid': organizationid,
                                   'Status' : 'created',
                                   'Role' : 'Admin'}
                userprojectserializer=UserProjectRoleSerializer(data = userprojectrole)
                if userprojectserializer.is_valid():
                    userprojectrole = userprojectserializer.save()
                    projectrole = UserProjectRole.objects.get(projectid=str(project.id))
                    data['k']=str(projectrole.id)
                else:
                    data = userprojectserializer.errors
        else:
            data = projectserializer.errors
        return Response(data)
#Update Project
@api_view(["POST"])
def updateproject_view(request, userid, projectid):
    if request.method == 'POST':        
        try:
            project = Project.objects.get(id=ObjectId(projectid))
        except Project.DoesNotExist:
            return Response("no record")
            
        #if organization.count()>0:            
        request.data['updated_by']=userid
        #organiztion_data = JSONParser().parse(request)
        projectserializer = ProjectSerializer(project,data= request.data)
        if projectserializer.is_valid():
            projectserializer.save()
        else:
            return Response(projectserializer.errors)
        return Response("Project information Updated Succesfully")
#deleteproject    
@api_view(["POST"])
def deleteproject_view(request, userid, projectid):
    if request.method == 'POST':        
        try:
            project = Project.objects.get(id=ObjectId(projectid))
        except Project.DoesNotExist:
            return Response("no record")
            
        #if organization.count()>0:            
        request.data['updated_by']=userid
        request.data['status']='0'
        #organiztion_data = JSONParser().parse(request)
        projectserializer = ProjectSerializer(project,data= request.data)
        if projectserializer.is_valid():
            projectserializer.save()
        else:
            return Response(projectserializer.errors)
        return Response("Project deactivated Succesfully")
@api_view(["POST"])
def adduser_view(request,userid, projectid,organizationid, role):
    #this request would not be model serializable infuture.
    # organizations and projects are not being added to the array
    if request.method == 'POST':
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            request.data['created_by']=userid
            organizationlist = []
            organizationlist.append(user.UserOrganizations)
            organizationlist.append(str(organizationid))
            request.data['UserOrganizations']= organizationlist
            #request.data['UserOrganizations']=user.UserOrganizations.append(str(organizationid))
            #password= request.data['password'].encode('utf-8')
            #pwdhash= bcrypt.hashpw(password, bcrypt.gensalt())
        #pwdhashencode = pwdhash.encode('utf-8')
            #request.data['password']=pwdhash.decode('utf-8')
            serializer = UserSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                username = request.data['username']
                usercount = User.objects.filter(username=username).count()
                if usercount>=1:
                    return Response(request.data['username']+' exists' + ' Choose another username')
                else:                
                    user = serializer.save()
                    userprojectrole = {'userid':userid, 'projectid':str(project.id),
                                   'organizationid': str(organizationid),
                                   'Status' : 'Added',
                                   'Role' : str(role)}
                    userprojectserializer=UserProjectRoleSerializer(data = userprojectrole)
                    if userprojectserializer.is_valid():
                        userprojectrole = userprojectserializer.save()
                    else:
                        data = userprojectserializer.errors    

            else:
                return Response("error")                        
        except:
            
            password= request.data['password'].encode('utf-8')
            pwdhash= bcrypt.hashpw(password, bcrypt.gensalt())
        #pwdhashencode = pwdhash.encode('utf-8')
            request.data['password']=pwdhash.decode('utf-8')
            request.data['organization']=str(organizationid)           
            serializer = UserSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                username = request.data['username']
                usercount = User.objects.filter(username=username).count()
                if usercount>=1:
                    return Response(request.data['username']+' exists' + ' Choose another username')
                else:                
                    user = serializer.save()
                #bcrypt.checkpw(password,pwdhash)
                    data['response'] = "Successfully registered new user."
                    data['email'] = user.email
                    data['username'] = user.firstName
                    userprojectrole = {'userid':userid, 'projectid':str(projectid),
                                   'organizationid': str(organizationid),
                                   'Status' : 'Added',
                                   'Role' : str(role)}
                    userprojectserializer=UserProjectRoleSerializer(data = userprojectrole)
                    if userprojectserializer.is_valid():
                        userprojectrole = userprojectserializer.save()
                    else:
                        data = userprojectserializer.errors    
            else:                
                data = serializer.errors                            
        return Response(data)
#Update User
@api_view(["POST"])
def updateuser_view(request, userid):
    if request.method == 'POST':        
        try:
            user = User.objects.get(id=ObjectId(userid))
        except User.DoesNotExist:
            return Response("no record")
            
        #if organization.count()>0:            
        request.data['updated_by']=userid
        #organiztion_data = JSONParser().parse(request)
        userserializer = UserSerializer(user,data= request.data)
        if userserializer.is_valid():
            userserializer.save()
        else:
            return Response(userserializer.errors)
        return Response("User information Updated Succesfully")
#delete user
@api_view(["POST"])
def deleteuser_view(request, userid):
    if request.method == 'POST':        
        try:            
            user = User.objects.get(id=ObjectId(userid))
        except User.DoesNotExist:
            return Response("no record")
            
        #if organization.count()>0:            
        request.data['updated_by']=userid
        request.data['status']='0'
        #organiztion_data = JSONParser().parse(request)
        userserializer = UserSerializer(user,data= request.data)
        if userserializer.is_valid():
            userserializer.save()
        else:
            return Response(userserializer.errors)
        return Response("User deactivated Succesfully")    
#user admit request
@api_view(["POST"])
def useradmitreq_view(request):
    if request.method == 'POST':        
        try:
            userid = request.data['userid']
            organizationid = request.data['organizationid']
            projectid = request.data['projectid']
            role = request.data['role']
            project = Project.objects.get(id=ObjectId(projectid))
        except :
            return Response("no record")
        #users=[]    
        #projectusers = project.users
        #for i in projectusers.count:            
        #    users.append(i)
        #users.append(userid)
        #project.users = users
        projectdict = project.__dict__
        projectserializer = ProjectSerializer(project,data= projectdict)
        if projectserializer.is_valid():
            projectserializer.save()
            userprojectrole = {'userid':userid, 'projectid':str(projectid),
                                   'organizationid': organizationid,
                                   'Status' : 'created',
                                   'Role' : role}
            userprojectserializer=UserProjectRoleSerializer(data = userprojectrole)
            if userprojectserializer.is_valid():                
                userprojectrole = userprojectserializer.save()
            else:
                return Response(userprojectserialzer.errors)
        else:
            return Response(projectserializer.errors)
        return Response("User added to the project")
@api_view(['POST'])
def approveuser_view(request,approverid):
    userprojectrole = {'userid':request.data['userid'],
                       'projectid':request.data['projectid'],
                       'organizationid': request.data['organizationid'],
                       'Status' : request.data['status'],
                       'Role' : request.data['role'],
                       'approver_id':approverid}
    userprojectserializer=UserProjectRoleSerializer(data = userprojectrole)
    if userprojectserializer.is_valid():                
        userprojectrole = userprojectserializer.save()
        return Response("Updated")
    else:
        return Response(userprojectserialzer.errors)
    
    
