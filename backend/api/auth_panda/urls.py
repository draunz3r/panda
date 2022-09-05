from django.urls import  path


# view imports
from .views import index

urlpatterns = [
    path('register/',index)
]