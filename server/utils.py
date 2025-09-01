from rest_framework.response import Response

def response(content=None, message="", status=200):
    if content is None:
        content = {}
    return Response({
        "content": content,
        "response": {
            "message": message,
            "status": status
        }
    }, status=status)

