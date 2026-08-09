from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from accounts import models
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = [AllowAny]

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! This is a protected view."})

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

class LogoutView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response(status=status.HTTP_204_NO_CONTENT)    
        return Response({"message": "You have been logged out successfully."},status=status.HTTP_200_OK)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = serializers.ProfileSerializer(request.user.profile)
        return Response(serializer.data)
    def patch(self, request):
        profile = request.user.profile
        user = request.user
        user.first_name = request.data.get("first_name",user.first_name)
        user.last_name = request.data.get("last_name",user.last_name)
        user.save()
        profile.phone = request.data.get("phone",profile.phone)
        profile.city = request.data.get("city",profile.city)
        profile.state = request.data.get("state",profile.state)
        profile.country = request.data.get("country",profile.country)
        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]
        profile.save()
        return Response(
            serializers.ProfileSerializer(profile).data,
            status=status.HTTP_200_OK
        )