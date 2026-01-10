from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'disbursements', DisbursementViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
