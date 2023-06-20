# views.py
from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objs as go
from api.models import Order, Complaint
from .forms import RouteSearchForm, FractionSearchForm
import logging

logger = logging.getLogger(__name__)


def dashboard_home_routes(request):
    logger.info(
        'dashboard_home_routes was called - path: %s, method: %s',
        request.path,
        request.method
    )
    form = RouteSearchForm()
    return render(request, 'dashboard_home_routes.html', {'form': form})

def dashboard_view_routes(request):
    logger.info(
        'dashboard_view_routes was called - path: %s, method: %s',
        request.path,
        request.method
    )
    form = RouteSearchForm(request.GET)
    if form.is_valid():
        route_id = form.cleaned_data['route_id']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Get data for all widgets
        df = Order.objects.weight_df_route(route_id, start_date, end_date)
        df_recurring_complaints = Complaint.objects.get_recurring_complaints_by_route(route_id)
        df_latest_complaints = Complaint.objects.get_latest_complaints_by_route(route_id)
        total_weight = Order.objects.total_weight_route(route_id, start_date, end_date)
        stats = Order.objects.get_stats_for_route(route_id, start_date, end_date)

        # New data
        heaviest_days = Order.objects.top_heaviest_days(route_id, start_date, end_date)
        least_heaviest_days = Order.objects.least_heaviest_days(route_id, start_date, end_date)
        count_days_weight_range = Order.objects.count_days_per_weight_range(route_id, [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000], start_date, end_date)


        # Plotly - Bar Chart
        trace = go.Bar(x=df['date'], y=df['weight'], name='Weight')
        layout = go.Layout(title='Weight over Time', xaxis=dict(title='Date'), yaxis=dict(title='Weight'))
        fig = go.Figure(data=[trace], layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        # Plotly - Pie Chart for count_days_weight_range
        pie_trace = go.Pie(labels=count_days_weight_range['bin'], values=count_days_weight_range['count'], name='Weight Ranges')
        pie_layout = go.Layout(title='Days in each Weight Range')
        pie_fig = go.Figure(data=[pie_trace], layout=pie_layout)

        pie_plot_div = plot(pie_fig, output_type='div', include_plotlyjs=False)

        # Convert DataFrame to html table
        table_div = df.to_html(index=False)

        df_recurring_complaints_div = df_recurring_complaints.to_html
        df_latest_complaints_div = df_latest_complaints.to_html

        return render(request, "dashboard_view_routes.html", context={
            'plot_div': plot_div,
            'total_weight': total_weight,
            'stats': stats,
            'table_div': table_div,
            'heaviest_days': heaviest_days,
            'least_heaviest_days': least_heaviest_days,
            'pie_plot_div': pie_plot_div,
            'route_id': route_id,
            'df_recurring_complaints_div': df_recurring_complaints_div,
            'df_latest_complaints_div': df_latest_complaints_div
        })
    else:
        return redirect('analytics:dashboard_home_routes')


def dashboard_home_fractions(request):
    logger.info(
        'dashboard_home_fractions was called - path: %s, method: %s',
        request.path,
        request.method
    )
    form = FractionSearchForm()
    return render(request, 'dashboard_home_fractions.html', {'form': form})


def dashboard_view_fractions(request):
    logger.info(
        'dashboard_view_fractions was called - path: %s, method: %s',
        request.path,
        request.method
    )
    form = FractionSearchForm(request.GET)
    if form.is_valid():
        fraction = form.cleaned_data['fraction']
        city_or_rural = form.cleaned_data['area']
        day_of_week = form.cleaned_data['day_of_week']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Get data for all widgets
        df = Order.objects.weight_df_fraction_month(fraction, city_or_rural, day_of_week, start_date, end_date)
        total_weight = Order.objects.total_weight_fraction(fraction, city_or_rural, day_of_week, start_date, end_date)
        stats = Order.objects.get_stats_for_fraction(fraction, city_or_rural, day_of_week, start_date, end_date)

        # New data for charts and lists
        route_weights = Order.objects.total_weight_fraction_per_route(fraction, city_or_rural, day_of_week, start_date, end_date)
        daily_weights = Order.objects.daily_weight_fraction_per_route(fraction, city_or_rural,day_of_week, start_date, end_date)
        top_5_routes_by_weight = Order.objects.top_5_routes_by_weight(fraction, city_or_rural, day_of_week, start_date, end_date)

        # Plotly - Bar Chart
        trace = go.Bar(x=df['date'], y=df['total_weight'], name='Weight')
        layout = go.Layout(title='Weight over Time', xaxis=dict(title='Date'), yaxis=dict(title='Weight'))
        fig = go.Figure(data=[trace], layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        # Plotly - Pie Chart
        labels = [rw['route_id'] for rw in route_weights]
        values = [rw['total_weight'] for rw in route_weights]

        pie_trace = go.Pie(labels=labels, values=values)
        pie_layout = go.Layout(title='Total Weight by Route')
        pie_fig = go.Figure(data=[pie_trace], layout=pie_layout)

        pie_plot_div = plot(pie_fig, output_type='div', include_plotlyjs=False)

        # Convert DataFrame to html table
        table_div = df.to_html(index=False)

        return render(request, "dashboard_view_fractions.html",
                      context={'plot_div': plot_div,
                               'total_weight': total_weight,
                               'stats': stats,
                               'table_div': table_div,
                               'route_weights': route_weights,
                               'daily_weights': daily_weights,
                               'top_5_routes_by_weight': top_5_routes_by_weight,
                               'pie_plot_div': pie_plot_div,
                               'fraction' : fraction})
    else:
        return redirect('analytics:dashboard_home')
