from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        notification = Notification.objects.filter(id=pk,user=request.user).first()
        if not notification:
            return Response({"error": "Notification not found"},status=404)
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)

class UnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        count = Notification.objects.filter(user=request.user,is_read=False).count()
        return Response({"unread": count})        