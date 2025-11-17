from django.urls import path
from messaging.views import SendSMSView

urlpatterns = [
    path('messaging/send/', SendSMSView.as_view(), name='send_sms')
]