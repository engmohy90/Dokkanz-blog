from channels import route

from consumers import connect_blog, disconnect_blog, save_post

channel_routing = [
    route("websocket.connect", connect_blog, path=r'^/blog/stream/$'),

    route("websocket.disconnect", disconnect_blog, path=r'^/blog/stream/$'),

    route("websocket.receive", save_post, path=r'^/blog/stream/$'),

]
