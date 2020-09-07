#from rest_framework import serializers 
from tasktracker.models import *
from tasktracker.Serializers import *
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

class UserSerializer(DocumentSerializer): 
    class Meta:
        model = User
        fields = '__all__'
        depth = 2
class OrganizationSerializer(DocumentSerializer): 
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 2
class ProjectSerializer(DocumentSerializer): 
    class Meta:
        model = Project
        fields = '__all__'
class UserProjectRoleSerializer(DocumentSerializer):    
    class Meta:
        model = UserProjectRole
        fields = '__all__'
class OtpSerializer(DocumentSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
