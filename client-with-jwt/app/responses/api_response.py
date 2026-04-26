import json
from flask import Flask, Response


class APIResponse:
    @staticmethod
    def success(data=None, message=None, status_code=200):
        response = {}
        if message:
            response['message'] = message
        if data:
            response.update(data)
        json_str = json.dumps(response, indent=2)
        return Response(json_str, status_code, mimetype='application/json')
    
    @staticmethod
    def error(message, error_code=None, status_code=400):
        response = {'error': error_code or 'Error', 'message': message}
        json_str = json.dumps(response, indent=2)
        return Response(json_str, status_code, mimetype='application/json')
    
    @staticmethod
    def validation_error(missing_fields):
        return APIResponse.error(
            message=f'Missing required fields: {', '.join(missing_fields)}',
            error_code='Validation Error',
            status_code=400
        )
    
    @staticmethod
    def unauthorized(message='Authentication required'):
        return APIResponse.error(message, 'Unauthorized', 401)
    
    @staticmethod
    def forbidden(message='Access denied'):
        return APIResponse.error(message, 'Forbidden', 403)
    
    @staticmethod
    def not_found(message='Resource not found'):
        return APIResponse.error(message, 'Not Found', 404)
    
    @staticmethod
    def conflict(message='Resource already exists'):
        return APIResponse.error(message, 'Conflict', 409)
    
    @staticmethod
    def server_error(message='An unexpected error occurred'):
        return APIResponse.error(message, 'Internal Server Error', 500)