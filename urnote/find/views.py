from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MillisecondsSerializer


def find_home(request):
    return render(request, 'find/find_home.html')


class MillisecondsView(APIView):
    def post(self, request):
        serializer = MillisecondsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
