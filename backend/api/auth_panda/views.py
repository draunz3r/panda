from django.shortcuts import render

# drf imports
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(http_method_names=['GET'])
def index(request):
    
    return Response({"msg": "hello world"})