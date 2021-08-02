import arrow
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from pool.models import TokenPool


class TokenPoolView(APIView):
    """Token Pool create and delete view."""

    def post(self, request):
        """Method for creating new token in pool."""
        token = TokenPool.objects.create()
        return Response({'token': str(token.uuid)})

    def delete(self, request, token_uuid):
        """Method for deleting token from pool."""
        token = TokenPool.objects.select_for_update(uuid=token_uuid).first()
        if token:
            token.delete()
            return Response({'response': 'Token deleted successfully'})
        else:
            raise ValidationError('Invalid token id')


class TokenBlockView(APIView):
    """Token Pool create and delete view."""

    def post(self, request):
        """Method for creating new token in pool."""
        token = None
        try:
            token = TokenPool.objects.select_for_update(expiry_time=,
                                                        refresh_time=).first()
            token.assigned_to = True
            token.expiry_time = arrow.now().shift(minute=+5)
            token.refresh_time = arrow.now().shift(minute=+1)
            token.save()
            return Response({'blocked_token': str(token.uuid)})
        except token is None:
            raise Http404


class KeepAliveView(APIView):

    def put(self, request, token_uuid):
        token = TokenPool.objects.select_for_update(uuid=token_uuid).first()
        if token.assigned_to is True:
            token.refresh_time = arrow.now().shift(minute=+1)
        else:
            token.expiry_time = arrow.now().shift(minute=+5)
