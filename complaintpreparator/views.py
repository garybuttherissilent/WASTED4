from django.shortcuts import render
from django.http import HttpResponse
from api.models import Route, Complaint
from .utils.style_excel_route_dict import create_styled_excel_ws
import pandas as pd
from .forms import DownloadComplaintsForm

def download_complaints(request):
    if request.method == 'POST':
        form = DownloadComplaintsForm(request.POST)
        if form.is_valid():
            day_of_week = form.cleaned_data['day_of_week']
            area = form.cleaned_data['area']

            # Mapping
            area_routes_mapping = {
                'CA': ['T1', 'T2', 'T4', 'T5', 'C1', 'C2', 'C4', 'C5', 'C1A', 'C2A', 'C4A', 'C5A'],
                'ZA': ['T1', 'T2', 'T4', 'T5', 'Z1', 'Z2', 'Z4', 'Z5', 'Z1A', 'Z2A', 'Z4A', 'Z5A'],
                'CB': ['T1', 'T2', 'T4', 'T5', 'C1', 'C2', 'C4', 'C5', 'C1B', 'C2B', 'C4B', 'C5B'],
                'ZB': ['T1', 'T2', 'T4', 'T5', 'Z1', 'Z2', 'Z4', 'Z5', 'Z1B', 'Z2B', 'Z4B', 'Z5B']
            }

            routes = Route.objects.filter(day_of_week=int(day_of_week), area__in=area_routes_mapping[area])

            df_list = []  # List to hold all dataframes
            for route in routes:
                df = Complaint.objects.get_latest_complaints_by_route(route.route_id)
                if not df.empty:
                    df_list.append((df, route.route_id))  # add to list if not empty

            if df_list:  # check if there is at least one non-empty dataframe
                print(df_list)
                with pd.ExcelWriter('complaints.xlsx', engine='openpyxl') as excel_writer:
                    for df, route_id in df_list:
                        create_styled_excel_ws(df, sheet_name=route_id, excel_writer=excel_writer)

                # Return the Excel file as a response
                with open('complaints.xlsx', 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=complaints.xlsx'
                    return response
            else:
                # Handle the case when there are no complaints to report
                # (you may want to show a message to the user instead of just passing)
                pass

    else:
        form = DownloadComplaintsForm()
    return render(request, 'complaintpreparator/download_complaints.html', {'form': form})
