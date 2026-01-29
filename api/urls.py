# from rest_framework.routers import DefaultRouter
# from .views import *

# router = DefaultRouter()
# router.register(r'clients', ClientViewSet)
# router.register(r'projects', ProjectViewSet)
# router.register(r'loans', LoanViewSet)
# router.register(r'disbursements', DisbursementViewSet)
# router.register(r'users', UserViewSet)

# urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    ProjectViewSet,
    LoanViewSet,
    DisbursementViewSet,
    # UserViewSet,  ← REMOVED
    RegisterView,
    LoginView,
    LogoutView,
    UserListView,
    UserDetailView,
    RoleUpdateView,
)

# Router for resources only (NO UserViewSet)
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'disbursements', DisbursementViewSet, basename='disbursement')

urlpatterns = [
    # User endpoints - BEFORE router.urls
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/logout/', LogoutView.as_view(), name='user-logout'),
    path('users/role/update/', RoleUpdateView.as_view(), name='user-role-update'),
    path('users/list/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]

# Add router URLs
urlpatterns += router.urls