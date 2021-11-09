from rest_framework.permissions import BasePermission
from .models import Comments, Contributors, Issues, Projects, Users


class IsAuthenticatedProjectAuthor(BasePermission):
    """
    Allow access to the projects view if user is Authenticated
    Project Author car create, get, modify or delete
    Contributors can only get or create
    """
    message = 'Editing projects is retricted to the author only!'
    author_methods = ['GET', 'POST', 'PUT', 'DELETE']
    base_methods = ['GET', 'POST']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            contributors = Contributors.objects.filter(project_id=obj.id)
            if request.user == obj.author_user_id:
                if request.method in self.author_methods:
                    return True
            elif contributors.get(user_id=request.user) is not None:
                if request.method in self.base_methods:
                    return True
            else:
                print("you're not this project's author or contributor")


class IsProjectAuthorOrContributor(BasePermission):
    """
    Allow access to the contributors view if user is Authenticated and author or contributor
    Project Author car create, get, modify or delete contributors
    Contributors can only get informations
    """
    message = 'you should be authenticated and Author or contributor of an existing project!'
    message_project_not_exist = 'This project does not exist'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    contributor_methods = ['GET', ]

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                actual_project = Projects.objects.get(pk=view.kwargs['projects_pk'])
            except :
                return False
            author = actual_project.author_user_id
            contributors = Contributors.objects.filter(project_id=actual_project.id)
            if request.user == author:
                return True
            elif request.user in contributors:
                return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            actual_project = Projects.objects.get(pk=view.kwargs['projects_pk'])
            author = actual_project.author_user_id
            contributors = Contributors.objects.filter(project_id=actual_project.id)
            if request.user == author:
                if request.method in self.author_object_methods:
                    return True
            elif request.user in contributors:
                if request.method in self.contributor_methods:
                    return True


class IsIssueAuthorOrAssignee(BasePermission):
    """
    Allow access to the issues view if user is Authenticated and,
    author or contributors of the related project
    Issue Author can create, get, modify or delete contributors
    Contributors can only get and post Issues
    """
    message = 'you should be authenticated and this issue author or assignee!'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    base_methods = ['GET', 'POST']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            self.actual_project = Projects.objects.get(pk=view.kwargs['projects_pk'])
            self.project_author = self.actual_project.author_user_id
            self.project_contributors = Contributors.objects.filter(project_id=self.actual_project.id)
            if request.user == self.project_author:
                return True
            elif request.user in self.project_contributors:
                return True
            else:
                print('you are not associated with this project')

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            actual_issue = Issues.objects.get(pk=view.kwargs['pk'])
            issue_author = actual_issue.author_user_id
            assignee = Users.objects.get(id=actual_issue.assignee_user_id.id)
            if request.user == issue_author:
                if request.method in self.author_object_methods:
                    return True
            elif request.user in assignee:
                if request.method in self.base_methods:
                    return True
            else:
                print('you are not associated with this issue')


class IsCommentAuthor(BasePermission):
    """
    Allow access to the issues view if user is Authenticated and,
    author or Assignee of the related issue
    Comment Author can create, get, modify or delete Comment
    Related issue members can only get and post Comment
    """
    message = 'you should be authenticated and Author or contributor!'
    author_object_methods = ['GET', 'POST', 'PUT', 'DELETE']
    base_methods = ['GET', 'POST']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            self.actual_issue = Issues.objects.get(pk=view.kwargs['issues_pk'])
            self.issue_author = self.actual_issue.author_user_id
            self.assignee = Users.objects.get(id=self.actual_issue.assignee_user_id.id)
            if request.user == self.issue_author:
                return True
            elif request.user in self.assignee:
                return True
            else:
                print('you are not associated with this issue')

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            actual_comment = Comments.objects.get(pk=view.kwargs['pk'])
            comment_author = actual_comment.author_user_id
            if request.user == comment_author:
                if request.method in self.author_object_methods:
                    print('issue member, comment author')
                    return True
            else:
                if request.method in self.base_methods:
                    print('issue member alone')
                    return True
