from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from .models import Profiles, Short
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .serializers import UserSerializer, ProfileSerializer, ShortSerializer
ADMIN_API_KEY = 'Luke_I_am_your_father'

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        Profiles.objects.create(username=user, email=request.data['username'], password=request.data['password'])
        return Response({'token': token.key, "status": "Account successfully created","status_code": 200,'user': serializer.data["id"]})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    # print(AllowAny)
    user = get_object_or_404(User, username=request.data
    ['username'])
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        print("user verified")
    else:
        print("NOT VERIFIED!!!!")
    if not user.check_password(request.data['password']):
        return Response({
            "status": "Incorrect username/password provided. Please retry",
            "status_code": 401
        })
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({
        "status": "Login successful",
        "status_code": 200,
        'token': token.key, 'user': serializer.data["id"]})

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def test_token(request):
    return Response("passed!")


class CreateShortView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [AllowAny]
    print(ADMIN_API_KEY)
    print("this key")
    def post(self, request, *args, **kwargs):
        api_key = request.headers.get('API-Key')
        print(api_key)
        # if api_key != ADMIN_API_KEY:
        #     return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        short = Short.objects.create(**data)
        short.save()
        return Response({
            "message": "Short added successfully",
            "short_id": short.id,
            "status_code": 200
        })

class ShortsFeedView(generics.ListAPIView):
    queryset = Short.objects.all().order_by('-publish_date', '-upvote')
    serializer_class = ShortSerializer

class FilteredFeedView(generics.ListAPIView):
    serializer_class = ShortSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Short.objects.all()
        category = self.request.query_params.get('category', None)
        publish_date = self.request.query_params.get('publish_date', None)
        upvote = self.request.query_params.get('upvote', None)
        title = self.request.query_params.get('title', None)
        keyword = self.request.query_params.get('keyword', None)
        author = self.request.query_params.get('author', None)

        if category:
            queryset = queryset.filter(category=category)
        if publish_date:
            queryset = queryset.filter(publish_date__gte=publish_date)
        if upvote:
            queryset = queryset.filter(upvote__gte=upvote)
        if title:
            queryset = queryset.filter(title__icontains=title)
        # if keyword:
        #     queryset = queryset.filter(models.Q(title__icontains=keyword) | models.Q(content__icontains=keyword))
        if author:
            queryset = queryset.filter(author__icontains=author)
        

        return queryset

