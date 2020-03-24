from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
        chat.routing.websocket_urlpatterns
        )
        ),
})

