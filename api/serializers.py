from rest_framework import serializers
from .models import User, Login
import bcrypt


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
