
from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    """
    Base permission class for role-based access
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsAdmin(RolePermission):
    allowed_roles = ['ADMIN']


class IsLoanOfficer(RolePermission):
    allowed_roles = ['ADMIN', 'LOAN_OFFICER']


class IsProjectOfficer(RolePermission):
    allowed_roles = ['ADMIN', 'PROJECT_OFFICER']


class IsFinanceOfficer(RolePermission):
    allowed_roles = ['ADMIN', 'FINANCE_OFFICER']


class IsManagementOrAdmin(RolePermission):
    allowed_roles = ['ADMIN', 'MANAGEMENT']



class IsLoanOfficerOrAdmin(permissions.BasePermission):
    """
    Loan Officers and Admins can create loans
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['ADMIN', 'LOAN_OFFICER']


class IsProjectOfficerOrAdmin(permissions.BasePermission):
    """
    Project Officers and Admins can create projects
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['ADMIN', 'PROJECT_OFFICER']


class IsFinanceOfficerOrAdmin(permissions.BasePermission):
    """
    Finance Officers and Admins can create disbursements
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['ADMIN', 'FINANCE_OFFICER']


class ReadOnlyForManagement(permissions.BasePermission):
    """
    Management users can only read (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'MANAGEMENT':
            return request.method in permissions.SAFE_METHODS

        return True