from rest_framework import serializers, generics
# from rest_framework.views import 
# from rest_framework.permissions import serializers, generics
# from rest_framework import serializers, generics
# from rest_framework import serializers, generics


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profiles, Short
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profiles
        fields = ['id', 'username', 'password', 'email']

class ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = '__all__'