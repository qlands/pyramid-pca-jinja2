def error_view(request):
    request.response.status = 500
    return {}
