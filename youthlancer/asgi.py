
import imp
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter ,URLRouter
import mesajlasma.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youthlancer.settings')


application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            mesajlasma.routing.websocket_urlpatterns
        )
    )
    
})
