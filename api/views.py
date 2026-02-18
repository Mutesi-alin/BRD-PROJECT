
import logging

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from clients.models import Client
from projects.models import Project
from loans.models import Loan
from disbursement.models import Disbursement
from user.models import User

from .serializers import (
    ClientSerializer,
    ProjectSerializer,
    LoanSerializer,
    DisbursementSerializer,
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    RoleUpdateSerializer,
)

from .permission import (
    IsAdmin,
    IsLoanOfficerOrAdmin,
    IsProjectOfficerOrAdmin,
    IsFinanceOfficerOrAdmin,
    IsManagementOrAdmin,
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)

                logger.info(f'User registered successfully: {user.email}')

                return Response({
                    'message': 'Registration successful',
                    'token': token.key,
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f'User registration failed: {str(e)}')
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logger.error(f'User registration validation failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Login attempt for non-existent user: {email}")
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        django_user = authenticate(request, username=email, password=password)

        if django_user:
            token, _ = Token.objects.get_or_create(user=django_user)

            logger.info(f'User logged in successfully: {email}')

            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        logger.warning(f'Login failed for user: {email}')
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()

            logger.info(f'User logged out: {request.user.email}')

            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f'Logout failed: {str(e)}')

            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.id != id and request.user.role != 'ADMIN':
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        logger.info(f"User with ID {id} retrieved successfully.")
        return Response(serializer.data)


class RoleUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request):
        serializer = RoleUpdateSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_role = serializer.validated_data['role']

            try:
                user = User.objects.get(id=user_id)
                user.role = new_role
                user.save()

                logger.info(f"Role updated for user {user.email}: {new_role}")

                return Response(
                    {
                        "message": f"Role updated to {new_role} successfully",
                        "user": UserSerializer(user).data
                    },
                    status=status.HTTP_200_OK,
                )

            except User.DoesNotExist:
                logger.error(f"User with ID {user_id} not found")

                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        logger.error(f'Invalid role update data: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsLoanOfficerOrAdmin]
        return [permission() for permission in permission_classes]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsProjectOfficerOrAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsManagementOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        """Override to ensure context is always passed"""
        kwargs['context'] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """Pass request context to serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
       
        
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsLoanOfficerOrAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsManagementOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
      
        return [permission() for permission in permission_classes]
    

class DisbursementViewSet(viewsets.ModelViewSet):
    queryset = Disbursement.objects.all()
    serializer_class = DisbursementSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsFinanceOfficerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        """Override to ensure context is always passed"""
        kwargs['context'] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """Pass request context to serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
