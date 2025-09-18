# finance/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, Category, Transaction, Transfer

# ---------- User ----------
class UserSerializer(serializers.ModelSerializer):
    "Serializer to retrieve user data (without password)"
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'tokens']

    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar datos del usuario (solo first_name y last_name)"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

# ---------- Account ----------
class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'owner']


# ---------- Category ----------
class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'owner']


# ---------- Transaction ----------
class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'category', 'amount', 'date', 'description', 'owner']
        # read_only_fields = ['date']

# ---------- Transfer ----------
class TransferSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    to_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Transfer
        fields = ['id', 'from_account', 'to_account', 'amount', 'date', 'description', 'owner']
        # read_only_fields = ['date']