from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsAuthor(BasePermission):
    message = 'Editing projects is retricted to the author only!'
    author_methods = ['PUT', 'DELETE']
    base_methods = ['GET', 'POST']
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print('essai')
            return True
    
    def has_object_permission(self, request, view, obj):
        print('vue')
        if request.user.is_authenticated:
            print('authenticated')
            print('obj.author_user_id', obj.author_user_id)
            print('request.user', request.user)
            print(request.method)
            if obj.author_user_id == request.user:
                if request.method in self.author_methods:
                    return True
            else:
                print("you're not this project's author")
            return obj.author_user_id == request.user
        
    


class IsContributor(BasePermission):
    message = 'You need to be author or contributor to create Issues and comments'
    my_safe_method = ['get', 'post'] # A vérifier

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print('essai contributor')
            return True

    def has_object_permission(self, request, view, obj):
        print('vue')
        if request.user.is_authenticated:
            print('authenticated')
            print('obj.author_user_id', obj.author_user_id)
            print('request.user', request.user)
            print(request.method)
            if obj.author_user_id == request.user:
                if request.method in self.author_methods:
                    return True
            else:
                print("you're not this project's author")
            return obj.author_user_id == request.user
    
    
