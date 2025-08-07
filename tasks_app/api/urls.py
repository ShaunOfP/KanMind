from django.urls import path

from .views import TaskCreateView, AssignedToMeView, ReviewingView, TaskUpdateAndDestroyView, CommentView, CommentDestroyView

urlpatterns = [
    path('', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskUpdateAndDestroyView.as_view(), name='task-detail'),
    path('<int:pk>/comments/', CommentView.as_view(), name='task-comments'),
    path('<int:pk>/comments/<int:comment_pk>/',
         CommentDestroyView.as_view(), name='comments-destroy'),
    path('assigned-to-me/', AssignedToMeView.as_view(), name='my-tasks'),
    path('reviewing/', ReviewingView.as_view(), name='task-reviewing'),
]
