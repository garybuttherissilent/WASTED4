from api.models import *
import pandas as pd
import numpy as np
from django.db.models import QuerySet, Sum
from django.forms.models import model_to_dict


class OrderQuerySet(QuerySet):
    # Functions for route_analysis
    def weight_df_route(self, route_id, start_date=None, end_date=None):
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        data = queryset.values('date', 'vehicle', 'weight', ).order_by('date')
        return pd.DataFrame.from_records(data)

    def total_weight_route(self, route_id, start_date=None, end_date=None):
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.aggregate(total_weight=Sum('weight'))['total_weight']

    def get_stats_for_route(self, route_id, start_date=None, end_date=None):
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        weights = queryset.values_list('weight', flat=True)
        return {'mean': np.mean(weights), 'std_dev': np.std(weights), 'median': np.median(weights)}

    def top_heaviest_days(self, route_id, start_date=None, end_date=None, n=5):
        """
        Returns the top 'n' heaviest days for a specific route.
        """
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('-weight')[:n].values('date', 'weight')

    def least_heaviest_days(self, route_id, start_date=None, end_date=None, n=5):
        """
        Returns the top 'n' least heaviest days for a specific route.
        """
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('weight')[:n].values('date', 'weight')

    def count_days_per_weight_range(self, route_id, bins, start_date=None, end_date=None):
        queryset = self.filter(route__route_id=route_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        df = queryset.values('date').annotate(total_weight=Sum('weight')).order_by('date')
        df = pd.DataFrame.from_records(df)

        counts = []
        for i in range(len(bins) - 1):
            count = df[(df['total_weight'] >= bins[i]) & (df['total_weight'] < bins[i + 1])].count()['date']
            counts.append(count)

        return pd.DataFrame({'bin': bins[:-1], 'count': counts})

    # Functions for fraction_analysis
    def weight_df_fraction(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None,
                           calendar=None):
        queryset = self.filter(route__fraction=fraction)
        if city_or_rural:
            queryset = queryset.filter(route__city_or_rural=city_or_rural)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if day_of_week:
            queryset = queryset.filter(route__day_of_week=day_of_week)
        if calendar:
            queryset = queryset.filter(route__calendar=calendar)

        data = queryset.values('date', 'route_id', 'weight').order_by('date')
        return pd.DataFrame.from_records(data)

    def weight_df_fraction_month(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        queryset = self.filter(route__fraction=fraction)
        if city_or_rural:
            queryset = queryset.filter(route__city_or_rural=city_or_rural)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if day_of_week:
            queryset = queryset.filter(route__day_of_week=day_of_week)
        if calendar:
            queryset = queryset.filter(route__calendar=calendar)
        data = queryset.values('date').annotate(total_weight=Sum('weight')).order_by('date')
        df = pd.DataFrame.from_records(data)

        # Manipulate the DataFrame: if the weight is less than 1000, add it to the previous date and drop the current row.
        for i in reversed(range(df.shape[0])):
            if df.loc[i, 'total_weight'] < 5000:
                if i > 0:  # ensure we are not at the first row
                    df.loc[i - 1, 'total_weight'] += df.loc[i, 'total_weight']
                df.drop(i, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def total_weight_fraction(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        queryset = self.filter(route__fraction=fraction)
        if city_or_rural:
            queryset = queryset.filter(route__city_or_rural=city_or_rural)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if day_of_week:
            queryset = queryset.filter(route__day_of_week=day_of_week)
        if calendar:
            queryset = queryset.filter(route__calendar=calendar)
        return queryset.aggregate(total_weight=Sum('weight'))['total_weight']

    def get_stats_for_fraction(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        df_month = self.weight_df_fraction_month(fraction, city_or_rural, day_of_week, start_date, end_date, calendar)
        df_day = self.weight_df_fraction(fraction, city_or_rural, day_of_week, start_date, end_date, calendar)

        weights_month = df_month['total_weight'].values
        weights_day = df_day['weight'].values

        stats_month = {
            'mean_month': np.mean(weights_month),
            'std_dev_month': np.std(weights_month),
            'median_month': np.median(weights_month)
        }

        stats_day = {
            'mean_day': np.mean(weights_day),
            'std_dev_day': np.std(weights_day),
            'median_day': np.median(weights_day)
        }

        return {**stats_day, **stats_month}

    def total_weight_fraction_per_route(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        queryset = self.filter(route__fraction=fraction)
        if city_or_rural:
            queryset = queryset.filter(route__city_or_rural=city_or_rural)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if day_of_week:
            queryset = queryset.filter(route__day_of_week=day_of_week)
        if calendar:
            queryset = queryset.filter(route__calendar=calendar)
        return queryset.values('route_id').annotate(total_weight=Sum('weight')).order_by('-total_weight')

    def daily_weight_fraction_per_route(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        queryset = self.filter(route__fraction=fraction)
        if city_or_rural:
            queryset = queryset.filter(route__city_or_rural=city_or_rural)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if day_of_week:
            queryset = queryset.filter(route__day_of_week=day_of_week)
        if calendar:
            queryset = queryset.filter(route__calendar=calendar)
        return queryset.values('date', 'route_id').annotate(daily_weight=Sum('weight')).order_by('date', 'route_id')

    def top_5_routes_by_weight(self, fraction, city_or_rural=None, day_of_week=None, start_date=None, end_date=None, calendar=None):
        queryset = self.total_weight_fraction_per_route(fraction, city_or_rural, day_of_week, start_date, end_date, calendar)
        return queryset[:5]


class ComplaintQuerySet(QuerySet):
    def get_complaints_by_street(self, street_name):
        # Fetch the Complaint instances related to the street addresses with the given street_name
        complaints = self.filter(street_address__street_name=street_name)

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_complaints_by_route(self, route):
        # Fetch the Complaint instances related to the given route
        complaints = self.filter(route=route).select_related('street_address')

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Replace the 'street_address' field in the dictionaries with the corresponding street name
        for i, complaint in enumerate(complaints):
            complaints_list[i]['street_address'] = complaint.street_address.street_name

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_latest_complaints_by_street(self, street_name, limit=10):
        # Fetch the Complaint instances related to the street addresses with the given street_name
        # Ordered by the date in descending order (latest first), limited to top 'limit'
        complaints = self.filter(street_address__street_name=street_name).order_by('complaint_date')[:limit]

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_latest_complaints_by_route(self, route, limit=200):
        # Fetch the Complaint instances related to the given route
        # Ordered by the date in descending order (latest first), limited to top 'limit'
        complaints = self.filter(route=route).select_related('street_address').order_by('complaint_date')[:limit]

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Replace the 'street_address' field in the dictionaries with the corresponding street name
        for i, complaint in enumerate(complaints):
            complaints_list[i]['street_address'] = complaint.street_address.street_name

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_recurring_complaints_by_street(self, street_name, priority='Wederkerend'):
        # Fetch the Complaint instances related to the street addresses with the given street_name
        # and with the given priority
        complaints = self.filter(street_address__street_name=street_name, priority=priority)

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_recurring_complaints_by_route(self, route, priority='Wederkerend'):
        # Fetch the Complaint instances related to the given route and with the given priority
        complaints = self.filter(route=route, priority=priority).select_related('street_address')

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Replace the 'street_address' field in the dictionaries with the corresponding street name
        for i, complaint in enumerate(complaints):
            complaints_list[i]['street_address'] = complaint.street_address.street_name

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_complaints_by_city(self, city):
        # Fetch the Complaint instances related to the given city
        complaints = self.filter(city=city)

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_complaints_by_priority_and_city(self, priority, city):
        # Fetch the Complaint instances with the given priority and city
        complaints = self.filter(priority=priority, city=city)

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_latest_complaints_by_city(self, city, limit=10):
        # Fetch the Complaint instances related to the given city
        # Ordered by the complaint_date in descending order (latest first), limited to top 'limit'
        complaints = self.filter(city=city).order_by('complaint_date')[:limit]

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df

    def get_complaints_by_modality(self, modality):
        # Fetch the Complaint instances with the given modality
        complaints = self.filter(modality=modality)

        # Convert the queryset to a list of dictionaries
        complaints_list = [model_to_dict(complaint) for complaint in complaints]

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(complaints_list)

        return df


