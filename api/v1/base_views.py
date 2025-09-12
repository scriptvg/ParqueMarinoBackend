"""
Base API Views for Parque Marino Backend
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """
    Base API View with common functionality
    """
    
    def success_response(self, data=None, message="Success", status_code=status.HTTP_200_OK):
        """Return a standardized success response"""
        response_data = {
            "success": True,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)
    
    def error_response(self, message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Return a standardized error response"""
        response_data = {
            "success": False,
            "message": message,
            "errors": errors
        }
        return Response(response_data, status=status_code)