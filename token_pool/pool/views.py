import arrow

from django.db.models import Q
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from pool.models import TokenPool


class TokenPoolView(APIView):
    """Token Pool create and delete view."""

    def post(self, request):
        """Method for creating new token in pool."""
        token = TokenPool.objects.create(expiry_time=arrow.utcnow(
        ).shift(minutes=5).datetime)
        return Response({'token': str(token.uuid)})

    def delete(self, request):
        """Method for deleting token from pool."""
        token = TokenPool.objects.filter(uuid=request.data.get('token_uuid')).first()
        if token:
            token.delete()
            return Response({'response': 'Token deleted successfully'})
        else:
            raise ValidationError('Invalid token id')


class TokenBlockView(APIView):
    """Token Pool view to block token."""

    def post(self, request):
        """Method for blocking random token in pool."""

        token = TokenPool.objects.filter(Q(assigned_to=False,
                                           expiry_time__gte=arrow.utcnow().datetime) | Q(
            refresh_time__lt=arrow.utcnow().datetime,
            expiry_time__gte=arrow.utcnow().datetime)).first()
        if token:

            token.assigned_to = True
            token.expiry_time = arrow.utcnow().shift(minutes=5).datetime
            token.refresh_time = arrow.utcnow().shift(minutes=1).datetime
            token.save()
            return Response({'blocked_token': str(token.uuid)})

        else:
            return Response({"error": "No free tokens"}, status=status.HTTP_404_NOT_FOUND)


class KeepAliveView(APIView):
    """Token Pool view to keep the token alive/blocked."""

    def post(self, request, token_uuid):
        """Method for keeping token alive/blocked in pool."""
        token = TokenPool.objects.filter(uuid=token_uuid,
                                         expiry_time__gte=arrow.utcnow().datetime).first()
        if token:
            token.expiry_time = arrow.utcnow().shift(minutes=5).datetime

            if token.refresh_time and token.refresh_time >= arrow.utcnow().datetime:
                token.refresh_time = arrow.utcnow().shift(minutes=1).datetime
            token.save()
            return Response({'response': 'Token refreshed successfully'})
        else:
            raise ValidationError('Invalid token id')
