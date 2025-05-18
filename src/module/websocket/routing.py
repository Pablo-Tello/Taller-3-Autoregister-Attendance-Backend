from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/qr/session/(?P<session_id>\d+)/$', consumers.QRCodeConsumer.as_asgi()),
]
