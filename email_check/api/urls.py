from django.urls import path

from .views import EmailCheckView

urlpatterns = [
    path('<str:email>/', EmailCheckView.as_view(), name='check-mail')
]
