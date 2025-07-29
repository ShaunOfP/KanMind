from django.urls import path
from .views import TaskListView, AssignedToMeView, ReviewingView, TaskDetailView, CommentView, CommentDestroyView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/comments/', CommentView.as_view(), name='task-comments'),
    path('<int:pk>/comments/<int:pk>/', CommentDestroyView.as_view(), name='comments-detail'),
    path('assigned-to-me/', AssignedToMeView.as_view(), name='my-tasks'),
    path('reviewing/', ReviewingView.as_view(), name='task-reviewing'),
]
