from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UploadFileForm
from .utils.dabbamaker import save_map_with_legend
import logging

logger = logging.getLogger(__name__)

def upload_file(request):
    logger.info(
        'dabba maker was called - path: %s, method: %s',
        request.path,
        request.method
    )
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            map_html = save_map_with_legend(excel_file)
            request.session['map_html'] = map_html  # save HTML to session
            messages.add_message(request, messages.INFO, 'map_ready')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def display_map(request):
    if 'map_html' in request.session:
        map_html = request.session['map_html']
        del request.session['map_html']  # clear session
        return HttpResponse(map_html)  # return map HTML
    else:
        return HttpResponse("No map to display.")  # error message
