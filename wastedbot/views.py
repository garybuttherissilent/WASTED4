from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.info(
        'my_view was called - path: %s, method: %s, status: %s',
        request.path,
        request.method
    )
    return render(request, 'wastedbot/index.html')



