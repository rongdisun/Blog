# context_processors.py
def current_url(request):
    return {
        'current_url': request.get_full_path()
    }
