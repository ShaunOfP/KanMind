from django.urls import path

from .views import EmailCheckView

urlpatterns = [
    path('', EmailCheckView.as_view(), name='check-mail')
]
