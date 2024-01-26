from rest_framework import serializers
from .models import User, Login
from .utils import required_validators
import bcrypt
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        raw_password = validated_data.get('password')
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

        new_data = validated_data.copy()
        new_data['password'] = hashed_password.decode('utf-8')

        return User.objects.create(**new_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):

    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        required_validators(login=login, password=password)

        email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')

        if email_regex.match(login):
            default_login = "email"
        else:
            default_login = "username"

        user = User.objects.filter(**{default_login: login}).first()

        if not user:
            raise serializers.ValidationError({'login': f'User with this {default_login} does not exist'})
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError({'password': 'Invalid password'})

        return user
