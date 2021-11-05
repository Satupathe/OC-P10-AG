from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Comments, Contributors, Issues, Projects, Users

class IsAuthenticatedProjectAuthor(BasePermission):
    message = 'Editing projects is retricted to the author only!'
    author_methods = ['GET', 'POST', 'PUT', 'DELETE']
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
            print('obj.id', obj.id)
            contributors = Contributors.objects.filter(project_id=obj.id)
            print('contributors', contributors)
            print(obj.author_user_id)
            [print(contributor.user_id) for contributor in contributors]
            if request.user == obj.author_user_id: #mettre pk ?
                print("auteur")
                print(request.method)
                if request.method in self.author_methods:
                    return True
            elif contributors.get(user_id=request.user) is not None:
                print('contributeur')
                print(request.method)
                if request.method in self.base_methods:
                    print('youpi!!')
                    return True
            else: 
                print("you're not this project's author")


class IsProjectAuthorOrContributor(BasePermission):
    message = 'you should be authenticated and Author or contributor!'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    contributor_methods = ['GET',]
    def has_permission(self, request, view):
        print('permission1')
        if request.user.is_authenticated:
            print(request.user)
            actual_project = Projects.objects.get(pk=view.kwargs['projects_pk'])
            print(actual_project)
            author = actual_project.author_user_id
            contributors = Contributors.objects.filter(project_id=actual_project.id)
            if request.user == author:
                print('permission4')
                return True
            elif request.user in contributors:
                print('permission3')
                return True

    def has_object_permission(self, request, view, obj):
        print('permissionobject1')
        if request.user.is_authenticated:
            print(request.user)
            actual_project = Projects.objects.get(pk=view.kwargs['projects_pk'])
            print(actual_project)
            author = actual_project.author_user_id
            print(author)
            contributors = Contributors.objects.filter(project_id=actual_project.id)
            print(contributors)
            print('permissionobject2')
            if request.user == author:
                print('permissionobject3')
                if request.method in self.author_object_methods:
                    print('author object methods')
                    return True
            elif request.user in contributors:
                print('permissionobject4')
                if request.method in self.contributor_methods:
                    print('contributor object methods')
                    return True

            
class IsIssueAuthorOrAssignee(BasePermission):
    message = 'you should be authenticated and this issue author or assignee!'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    base_methods = ['GET', ]
    def has_permission(self, request, view):
        print('permission1')
        if request.user.is_authenticated:
            print(request.user)
            print(view.kwargs)
            self.actual_project = Projects.objects.get(pk=view.kwargs['projects_pk']) # a changer mais comment ??
            
            print(self.actual_project)
            self.project_author = self.actual_project.author_user_id
            self.project_contributors = Contributors.objects.filter(project_id=self.actual_project.id)
            
            if request.user == self.project_author:
                print('permission4')
                return True
            elif request.user in self.project_contributors:
                print('permission3')
                return True
            else:
                print('you are not associated with this project')

    def has_object_permission(self, request, view, obj):
        print('permissionobject1')
        if request.user.is_authenticated:
            print('permissionobject2')
            print(view.kwargs)
            #print(obj.kwargs)
            actual_issue = Issues.objects.get(pk=view.kwargs['pk'])
            issue_author = actual_issue.author_user_id
            assignee = Users.objects.get(id=actual_issue.assignee_user_id.id)
            if request.user == issue_author:
                if request.method in self.author_object_methods:
                    print('project member, issue author')
                    return True
            elif request.user in assignee:
                if request.method in self.base_methods:
                    print('project member, issue assignee')
                    return True
            else:
                print('you are not associated with this issue')


class IsCommentAuthor(BasePermission):
    message = 'you should be authenticated and Author or contributor!'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    base_methods = ['GET',] # Rajouter post?
    
    def has_permission(self, request, view):
        print('permission1')
        if request.user.is_authenticated:
            print(request.user)
            print(view.kwargs)
            self.actual_issue = Issues.objects.get(pk=view.kwargs['issues_pk'])
            
            print(self.actual_issue)
           
            self.issue_author = self.actual_issue.author_user_id
            self.assignee = Users.objects.get(id=self.actual_issue.assignee_user_id.id)
            if request.user == self.issue_author:
                print('permission4')
                return True
            elif request.user in self.assignee:
                print('permission3')
                return True
            else:
                print('you are not associated with this issue')

    def has_object_permission(self, request, view, obj):
        print('permissionobject1')
        if request.user.is_authenticated:
            print('permissionobject2')
            actual_comment = Comments.objects.get(pk=view.kwargs['pk'])
            comment_author = actual_comment.author_user_id
            print('permissionobject3')
            if request.user == comment_author:
                if request.method in self.author_object_methods:
                    print('issue member, comment author')
                    return True
            else:
                if request.method in self.base_methods:
                    print('issue member alone')     
                    return True 