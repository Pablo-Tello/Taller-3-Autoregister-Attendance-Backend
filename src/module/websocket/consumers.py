import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.utils import timezone
from src.module.asistencia.models import Asistencia, CodigoQR
from src.module.academico.models import SesionClase


class QRCodeConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for QR code verification notifications.
    
    This consumer handles WebSocket connections for teachers to receive
    real-time notifications when a student verifies a QR code and registers
    attendance.
    """
    
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        # Get the session ID from the URL route
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'qr_session_{self.session_id}'
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept the connection
        await self.accept()
        
        # Send a confirmation message
        await self.send_json({
            'type': 'connection_established',
            'message': f'Connected to QR code session {self.session_id}',
            'session_id': self.session_id
        })
    
    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive_json(self, content):
        """
        Called when we receive a text frame from the client.
        """
        message_type = content.get('type', None)
        
        if message_type == 'ping':
            # Respond to ping messages to keep the connection alive
            await self.send_json({
                'type': 'pong',
                'timestamp': str(timezone.now())
            })
    
    async def qr_verified(self, event):
        """
        Called when a QR code has been verified.
        This method sends a message to the WebSocket client.
        """
        # Send the notification to the WebSocket
        await self.send_json({
            'type': 'qr_verified',
            'session_id': event['session_id'],
            'student_id': event['student_id'],
            'student_name': event['student_name'],
            'attendance_id': event['attendance_id'],
            'timestamp': event['timestamp']
        })
