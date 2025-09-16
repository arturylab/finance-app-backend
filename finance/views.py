# finance/views.py
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import Account, Category, Transaction, Transfer
from .serializers import (
    UserRegisterSerializer, UserSerializer, AccountSerializer, CategorySerializer, 
    TransactionSerializer, TransferSerializer
)
from .permissions import IsOwner


# View for handling user registration
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

# ViewSet for managing user profile
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Solo permitir que el usuario vea su propio perfil
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'], url_path='me')
    def get_current_user(self, request):
        """Endpoint para obtener datos del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

# Mixin to handle owner-specific operations
class OwnerMixin:
    # Filter queryset to only show objects owned by the current user
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    # Automatically set the owner when creating new objects
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# ViewSet for managing bank accounts
class AccountViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# ViewSet for managing transaction categories
class CategoryViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'type']

# ViewSet for managing financial transactions
class TransactionViewSet(OwnerMixin, viewsets.ModelViewSet):
    # Use select_related to optimize database queries
    queryset = Transaction.objects.all().select_related('account', 'category')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['account', 'category', 'date']
    ordering_fields = ['date', 'amount']
    search_fields = ['description']

# ViewSet for managing transfers between accounts
class TransferViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['description']