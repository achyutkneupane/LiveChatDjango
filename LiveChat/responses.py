from drf_yasg import openapi

error_response = {
    400: openapi.Response('Invalid Data', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_INTEGER)
        }
    ), examples={
        'application/json': {
            'message': 'Invalid Data',
            'status': 400
        }
    }),
}

login_response = {
    200: openapi.Response('User Logged In Successfully', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': {
                'access': openapi.Schema(type=openapi.TYPE_STRING)
            },
            'status': openapi.Schema(type=openapi.TYPE_INTEGER)
        }
    ), examples={
        'application/json': {
            'message': 'User Logged In Successfully',
            'data': {
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
            },
            'status': 200
        }
    }),
    400: error_response[400]
}

register_response = {
    200: openapi.Response('User Registered Successfully', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_INTEGER)
        }
    ), examples={
        'application/json': {
            'message': 'User Registered Successfully',
            'status': 200
        }
    }),
    400: error_response[400]
}