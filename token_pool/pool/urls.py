from django.urls import path

from .views import *

urlpatterns = [
    path('current_weather/', TokenPoolView.as_view(),
         name='pool-list'),
    # path('mailing_list/', MailingListView.as_view(),
    #      name='mailing-list'),
]