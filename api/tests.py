from django.test import TestCase
from .models import Route, Order, StreetAddress, RouteStreetAddress, Complaint

class RouteModelTest(TestCase):

    def setUp(self):
        self.route = Route.objects.create(
            route_id = "123",
            fraction = "A",
            area = "TestArea",
            day_of_week = 1,
            city_or_rural = "City"
        )

    def test_route_creation(self):
        self.assertEquals(self.route.route_id, "123")


class OrderModelTest(TestCase):

    def setUp(self):
        self.route = Route.objects.create(
            route_id = "123",
            fraction = "A",
            area = "TestArea",
            day_of_week = 1,
            city_or_rural = "City"
        )

        self.order = Order.objects.create(
            route = self.route,
            date = "2023-01-01",
            vehicle = "TestVehicle",
            weight = 10.0
        )

    def test_order_creation(self):
        self.assertEquals(self.order.vehicle, "TestVehicle")


class StreetAddressModelTest(TestCase):

    def setUp(self):
        self.streetaddress = StreetAddress.objects.create(
            street_name = "TestStreet",
            zip_code = "12345",
            purpose = "TestPurpose",
            area = "TestArea",
            latitude = 12.00,
            longitude = 15.00
        )

    def test_street_address_creation(self):
        self.assertEquals(self.streetaddress.street_name, "TestStreet")


class RouteStreetAddressModelTest(TestCase):

    def setUp(self):
        self.route = Route.objects.create(
            route_id = "123",
            fraction = "A",
            area = "TestArea",
            day_of_week = 1,
            city_or_rural = "City"
        )

        self.streetaddress = StreetAddress.objects.create(
            street_name = "TestStreet",
            zip_code = "12345",
            purpose = "TestPurpose",
            area = "TestArea",
            latitude = 12.00,
            longitude = 15.00
        )

        self.routestreetaddress = RouteStreetAddress.objects.create(
            route = self.route,
            street_address = self.streetaddress
        )

    def test_route_street_address_creation(self):
        self.assertEquals(self.routestreetaddress.route.route_id, "123")


class ComplaintModelTest(TestCase):

    def setUp(self):
        self.route = Route.objects.create(
            route_id = "123",
            fraction = "A",
            area = "TestArea",
            day_of_week = 1,
            city_or_rural = "City"
        )

        self.streetaddress = StreetAddress.objects.create(
            street_name = "TestStreet",
            zip_code = "12345",
            purpose = "TestPurpose",
            area = "TestArea",
            latitude = 12.00,
            longitude = 15.00
        )

        self.complaint = Complaint.objects.create(
            route = self.route,
            complaint_date = "2023-01-01",
            modality = "TestModality",
            recipient = "TestRecipient",
            priority = "TestPriority",
            street_address = self.streetaddress,
            address_number = "123",
            zip_code = "12345",
            city = "TestCity"
        )

    def test_complaint_creation(self):
        self.assertEquals(self.complaint.recipient, "TestRecipient")

    def test_fraction_property(self):
        self.assertEquals(self.complaint.fraction, self.route.fraction)

