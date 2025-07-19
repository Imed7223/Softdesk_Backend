from django.urls import path
from .views import ContributorViewSet, IssueViewSet, CommentViewSet


contributor_list = ContributorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
contributor_detail = ContributorViewSet.as_view({
    'delete': 'destroy'
})

issue_list = IssueViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
issue_detail = IssueViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'put': 'update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'put': 'update',
    'post': 'create'
})
comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('projects/<int:project_id>/contributors/', contributor_list, name='contributor-list'),
    path('projects/<int:project_id>/contributors/<int:pk>/', contributor_detail, name='contributor-detail'),

    path('projects/<int:project_id>/issues/', issue_list, name='issue-list'),
    path('projects/<int:project_id>/issues/<int:pk>/', issue_detail, name='issue-detail'),

    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', comment_list, name='comment-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/', comment_detail, name='comment-detail'),
]
