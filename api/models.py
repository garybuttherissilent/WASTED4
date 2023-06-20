import uuid
from django.db import models
from analytics.utils.data_analysis import OrderQuerySet, ComplaintQuerySet


class Route(models.Model):
    route_id = models.CharField(max_length=50, primary_key=True)
    fraction = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    day_of_week = models.IntegerField()
    city_or_rural = models.CharField(max_length=50)


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    vehicle = models.CharField(max_length=50)
    weight = models.FloatField()

    objects = OrderQuerySet.as_manager()

class StreetAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    street_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    purpose = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class RouteStreetAddress(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    street_address = models.ForeignKey(StreetAddress, on_delete=models.CASCADE)


class Complaint(models.Model):
    unique_identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    complaint_date = models.DateField()
    modality = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    street_address = models.ForeignKey(StreetAddress, on_delete=models.CASCADE)
    address_number = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    @property
    def fraction(self):
        return self.route.fraction

    objects = ComplaintQuerySet.as_manager()



