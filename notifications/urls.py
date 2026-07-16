from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, UnreadNotificationCountView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications"),
    path("<int:pk>/read/", MarkNotificationReadView.as_view(), name="mark-read"),
    path("unread-count/", UnreadNotificationCountView.as_view(), name="unread-count"),
]