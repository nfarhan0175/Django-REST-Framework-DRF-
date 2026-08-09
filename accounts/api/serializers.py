from rest_framework import serializers
from accounts import models
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.profile.role
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.profile.role
        return data

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=models.UserProfile.ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True,min_length=6)
    class Meta:
        model = models.User
        fields = ['email', 'username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = models.User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"]
        )
        user.profile.role = role
        user.profile.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Token is expired or invalid')}
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name",required=False)
    last_name = serializers.CharField(source="user.last_name",required=False)
    role = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.UserProfile
        fields = [
            "username", "email", "first_name", "last_name", "phone",
            "city", "state", "country", "role", "profile_picture",
        ]
# https://github.com/CryceTruly/incomeexpensesapi/blob/master/authentication/serializers.py            