from django.urls import path

from .views import BoardListView, BoardDetailView

urlpatterns = [
    path('', BoardListView.as_view(), name='boards-list'),
    path('<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
]
