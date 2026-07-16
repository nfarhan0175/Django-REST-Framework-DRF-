from rest_framework import serializers
from accounts import models
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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

# https://github.com/CryceTruly/incomeexpensesapi/blob/master/authentication/serializers.py            