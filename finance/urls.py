# finance/urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AccountViewSet, CategoryViewSet, TransactionViewSet, TransferViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'transfers', TransferViewSet, basename='transfer')

urlpatterns = router.urls