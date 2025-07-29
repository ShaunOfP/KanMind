from django.urls import path
from .views import BoardListView, BoardDetailView, EmailCheckView

urlpatterns = [
    path('', BoardListView.as_view(), name='boards-list'),
    path('<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='mail-check'),
]