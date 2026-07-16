from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from accounts import models
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = [AllowAny]

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! This is a protected view."})

class LogoutView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response(status=status.HTTP_204_NO_CONTENT)    
        return Response({"message": "You have been logged out successfully."},status=status.HTTP_200_OK)