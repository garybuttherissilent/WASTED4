from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib import messages
from .forms import UploadFileForm
from .utils.dagplanningmaker2 import *
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def file_upload(request):
    logger.info(
        'shift scheduler was called - path: %s, method: %s',
        request.path,
        request.method
    )
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_file = request.FILES['file']
            wb = dagplanningmaker(input_file)
            output = BytesIO()  # Create a BytesIO object
            wb.save(output)  # Save the workbook to the BytesIO object
            output.seek(0)  # Seek back to the beginning of the file
            response = FileResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=dagplanning.xlsx'
            messages.success(request, 'File uploaded and converted successfully!')
            return response  # Return the response immediately
        else:
            messages.error(request, 'There was an error with your file upload. Please try again.')
    else:
        form = UploadFileForm()
    return render(request, 'file_upload.html', {'form': form})
