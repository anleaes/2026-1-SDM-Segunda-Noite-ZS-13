from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            connection.ensure_connection()
            db_status = 'up'
            http_status = 200
            overall = 'ok'
        except Exception:
            db_status = 'down'
            http_status = 503
            overall = 'degraded'

        return Response(
            {
                'status': overall,
                'database': db_status,
            },
            status=http_status,
        )
