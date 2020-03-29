def notfound_view(request):
    request.response.status = 404
    return {}
