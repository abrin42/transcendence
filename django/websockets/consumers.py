from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Envoyer un message de succès au client après l'acceptation
        await self.send(text_data=json.dumps({
            'type': 'connection_success',
            'message': 'Connexion réussie!'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Cette méthode est appelée lorsque le serveur reçoit un message du client
        data = json.loads(text_data)  # Parse le message reçu
        await self.send(text_data=json.dumps({
            'message': data['message']  # Renvoyer un message au client
        }))