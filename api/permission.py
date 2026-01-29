# api/permission.py
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allow access only to Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsLoanOfficer(permissions.BasePermission):
    """Allow access to Loan Officers and Admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'LOAN_OFFICER']


class IsProjectOfficer(permissions.BasePermission):
    """Allow access to Project Officers and Admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'PROJECT_OFFICER']


class IsFinanceOfficer(permissions.BasePermission):
    """Allow access to Finance Officers and Admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'FINANCE_OFFICER']


class IsManagementOrAdmin(permissions.BasePermission):
    """Allow access to Management and Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'MANAGEMENT']


class ReadOnlyForManagement(permissions.BasePermission):
    """Management users can only read (GET), not modify"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.role == 'MANAGEMENT':
            # Management can only use safe methods (GET, HEAD, OPTIONS)
            return request.method in permissions.SAFE_METHODS
        
        # For other roles, allow all methods
        return True