from django.urls import path
from . import views

app_name = 'realtime'

urlpatterns = [
    path('chat/list/', views.chat_list, name='chat_list'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
    path('notifications/', views.get_notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('privatemessage/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/toggle-read/', views.toggle_read, name='toggle_read'),
    path('new-message/', views.new_message, name='new_message'),
    path('test-message/', views.new_message, name='test_message'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
]
