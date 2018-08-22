from channels.routing import ProtocolTypeRouter, URLRouter
import mines.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        mines.routing.websocket_urlpatterns
    )
})
