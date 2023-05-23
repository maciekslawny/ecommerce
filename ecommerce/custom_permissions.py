from rest_framework.permissions import BasePermission


class IsSellerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == request.user.SELLER


class IsCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == request.user.CUSTOMER
