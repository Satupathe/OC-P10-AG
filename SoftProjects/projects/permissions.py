from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    message = 'Editing projects is retricted to the author only!'
    my_safe_methods = ['get', 'post', 'put', 'delete']
    def has_permission(self, request, view):
        if request.method in self.my_safe_methods:
            return True
        return False
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_methods:
            return True    
        return obj.author_user_id == request.user


class IsContributor(BasePermission):
    message = 'You need to be author or contributor to create Issues and comments'
    my_safe_method = ['get', 'post'] # A vérifier

    def has_permission(self, request, view):
        return super().has_permission(request, view)

        """try:
            contributor = Contributors.objects.get(user=request.user)"""
