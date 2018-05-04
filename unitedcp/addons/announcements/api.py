from .models import UserAnnouncements

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class Announcements(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        announcements_list = UserAnnouncements.objects.values().order_by('updated_date').all()
        if not announcements_list.exists():
            return Response({'announcements_list': False}, status=200, content_type='application/json')
        return Response({'announcements_list': announcements_list}, status=200, content_type='application/json')
