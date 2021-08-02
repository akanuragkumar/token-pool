from django.urls import path

from .views import *

urlpatterns = [
    path('token_pool/', TokenPoolView.as_view(),
         name='pool-token'),
    path('block_token/', TokenBlockView.as_view(),
         name='block-token'),
    path('keep_alive/<uuid:token_uuid>', KeepAliveView.as_view(),
         name='keep-alive'),
]