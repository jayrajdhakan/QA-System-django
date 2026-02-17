import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage 

# Load chat_tree.json
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(CURRENT_DIR, 'chat_tree.json')

try:
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        TREE_DATA = json.load(f)
except FileNotFoundError:
    TREE_DATA = {"nodes": {}}

class QAConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.is_admin = self.user.is_staff if self.user and self.user.is_authenticated else False
        
        # Identity setup
        if self.user and self.user.is_authenticated:
            self.display_name = self.user.first_name or self.user.username
            self.user_id = str(self.user.id)
        else:
            self.display_name = "Guest"
            session = self.scope.get("session")
            self.user_id = session.session_key[:5] if session and session.session_key else "Guest"

        self.admin_group = "admin_group"
        self.user_group = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.user_group, self.channel_name)
        if self.is_admin:
            await self.channel_layer.group_add(self.admin_group, self.channel_name)
        
        await self.accept()

        # Initial Bot Welcome
        start_node_id = TREE_DATA.get("start_node", "node_1")
        await self.send_node(start_node_id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        value = data.get('value') # Node ID from button click
        target_user_id = data.get('target_user_id')

        # 1. ADMIN MANUAL REPLY
        if target_user_id and message:
            payload = {
                'type': 'chat_message', 
                'message': message, 
                'sender': 'Admin', 
                'user_id': target_user_id,
                'is_handoff': False
            }
            # Send to the specific user's group
            await self.channel_layer.group_send(f"user_{target_user_id}", payload)
            # Send to all admins (so other open admin tabs update)
            await self.channel_layer.group_send(self.admin_group, payload)
            return

        # 2. USER CLICKED A BUTTON (Node Navigation)
        if value:
            # First, tell the Admin what the user clicked
            await self.channel_layer.group_send(self.admin_group, {
                'type': 'chat_message',
                'message': f"Selected option: {value}",
                'sender': self.display_name, 
                'user_id': self.user_id,
                'is_handoff': (value == "ai_agent_node") # Trigger green dot
            })
            # Then, send the next node response
            await self.send_node(value)
            return

        # 3. USER TYPED MESSAGE
        elif message:
            await self.save_message(self.user_id, self.display_name, message)
            await self.channel_layer.group_send(self.admin_group, {
                'type': 'chat_message',
                'message': message,
                'sender': self.display_name, 
                'user_id': self.user_id,
                'is_handoff': True # Trigger green dot for manual messages
            })

    async def send_node(self, node_id):
        """Finds node and sends it directly to the user to avoid duplication"""
        node = TREE_DATA.get("nodes", {}).get(node_id)
        if node:
            is_handoff = (node_id == "ai_agent_node")
            
            # Print for debugging
            print(f"DEBUG: Node ID: {node_id} | is_handoff: {is_handoff}")

            raw_question = node.get("question", "")
            message_text = raw_question.replace("{name}", self.display_name)

            ui_options = [
                {"label": opt["text"], "value": opt["next_node"]} 
                for opt in node.get("options", []) if opt.get("next_node") is not None
            ]

            # We use self.send instead of group_send to prevent the user
            # from receiving the message they just triggered twice.
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'sender': 'Admin', # Bot shows as 'Admin' to user
                'user_id': self.user_id,
                'message': message_text,
                'options': ui_options,
                'is_handoff': is_handoff
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, room_id, sender, message):
        if message == "User joined the chat": return None
        return ChatMessage.objects.create(room_id=room_id, sender=sender, message=message)