from .forms import DownloadComplaintsForm
from api.models import Complaint
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from .utils.style_excel import create_styled_excel
from .utils.style_excel_street import create_styled_excel_street
import logging

logger = logging.getLogger(__name__)

def download_complaints(request):
    logger.info(
        'complaint organizer was called - path: %s, method: %s',
        request.path,
        request.method
    )
    if request.method == 'POST':
        form = DownloadComplaintsForm(request.POST)
        if form.is_valid():
            complaints_type = form.cleaned_data['complaints_type']
            filter_field = form.cleaned_data['filter_field']
            filter_value = form.cleaned_data['filter_value']

            if complaints_type == 'latest':
                if filter_field == 'route_id':
                    df = Complaint.objects.get_latest_complaints_by_route(filter_value)
                    use_style_excel = True
                    use_style_excel_street = False
                elif filter_field == 'street_name':
                    df = Complaint.objects.get_latest_complaints_by_street(filter_value)
                    use_style_excel = False
                    use_style_excel_street = True
                # Add more conditions based on available filter fields
            elif complaints_type == 'recurring':
                if filter_field == 'route_id':
                    df = Complaint.objects.get_recurring_complaints_by_route(filter_value)
                    use_style_excel = True
                elif filter_field == 'street_name':
                    df = Complaint.objects.get_recurring_complaints_by_street(filter_value)
                    use_style_excel = False
                    use_style_excel_street = True

            # Convert the 'complaint_date' column to datetime type
            df['complaint_date'] = pd.to_datetime(df['complaint_date'])

            # Format the 'complaint_date' column in the desired format
            df['complaint_date'] = df['complaint_date'].dt.strftime('%Y-%m-%d')

            # Convert DataFrame to Excel and return as response
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=complaints.xlsx'

            if use_style_excel:
                byte_data = create_styled_excel(df)
                response.write(byte_data.getvalue())
            elif use_style_excel_street:
                byte_data = create_styled_excel_street(df)
                response.write(byte_data.getvalue())
            else:
                df.to_excel(response, index=False)

            return response
    else:
        form = DownloadComplaintsForm()

    return render(request, 'complaintorganizer/download_complaints.html', {'form': form})
