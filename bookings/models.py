from django.db import models
from django.contrib.auth.models import User
from accounts.models import SearchSession

# ----------------------------------
# Fare model
# ----------------------------------
class Fare(models.Model):
    currency = models.CharField(max_length=10)
    base_fare = models.FloatField()
    tax = models.FloatField()
    yq_tax = models.FloatField()
    additional_txn_fee_ofrd = models.FloatField()
    additional_txn_fee_pub = models.FloatField()
    pg_charge = models.FloatField()
    other_charges = models.FloatField()
    discount = models.FloatField()
    published_fare = models.FloatField()
    commission_earned = models.FloatField()
    plb_earned = models.FloatField()
    incentive_earned = models.FloatField()
    offered_fare = models.FloatField()
    tds_on_commission = models.FloatField()
    tds_on_plb = models.FloatField()
    tds_on_incentive = models.FloatField()
    service_fee = models.FloatField()
    total_baggage_charges = models.FloatField()
    total_meal_charges = models.FloatField()
    total_seat_charges = models.FloatField()
    total_special_service_charges = models.FloatField()

    def __str__(self):
        return f"Fare({self.currency} {self.offered_fare})"


# ----------------------------------
# Passenger model
# ----------------------------------
class Passenger(models.Model):
    pax_id = models.IntegerField()
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pax_type = models.IntegerField()
    date_of_birth = models.DateTimeField()
    gender = models.IntegerField()
    is_lead_pax = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, null=True)
    # Storing minimal address fields
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True)
    pan = models.CharField(max_length=50, blank=True, null=True)
    passport_no = models.CharField(max_length=50, blank=True, null=True)

    # Link to Fare (One-to-One or separate — depends on your logic)
    fare = models.OneToOneField(Fare, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"


# ----------------------------------
# Segment model
# ----------------------------------
class Segment(models.Model):
    baggage = models.CharField(max_length=50, blank=True, null=True)
    cabin_baggage = models.CharField(max_length=50, blank=True, null=True)
    cabin_class = models.IntegerField()
    trip_indicator = models.IntegerField()
    segment_indicator = models.IntegerField()
    airline_code = models.CharField(max_length=10)
    airline_name = models.CharField(max_length=50)
    flight_number = models.CharField(max_length=10)
    fare_class = models.CharField(max_length=10, blank=True, null=True)
    operating_carrier = models.CharField(max_length=50, blank=True, null=True)
    airline_pnr = models.CharField(max_length=50, blank=True, null=True)
    
    # Origin
    origin_airport_code = models.CharField(max_length=10)
    origin_airport_name = models.CharField(max_length=100, blank=True, null=True)
    origin_terminal = models.CharField(max_length=10, blank=True, null=True)
    origin_city_code = models.CharField(max_length=10)
    origin_city_name = models.CharField(max_length=50)
    origin_country_code = models.CharField(max_length=10)
    origin_country_name = models.CharField(max_length=50)
    dep_time = models.DateTimeField()
    
    # Destination
    dest_airport_code = models.CharField(max_length=10)
    dest_airport_name = models.CharField(max_length=100, blank=True, null=True)
    dest_terminal = models.CharField(max_length=10, blank=True, null=True)
    dest_city_code = models.CharField(max_length=10)
    dest_city_name = models.CharField(max_length=50)
    dest_country_code = models.CharField(max_length=10)
    dest_country_name = models.CharField(max_length=50)
    arr_time = models.DateTimeField()

    duration = models.IntegerField()
    ground_time = models.IntegerField()
    mile = models.IntegerField()
    stop_over = models.BooleanField(default=False)
    craft = models.CharField(max_length=50, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    flight_status = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.airline_code}{self.flight_number} {self.origin_city_name} -> {self.dest_city_name}"


# ----------------------------------
# FareRule model (simplified)
# ----------------------------------
class FareRule(models.Model):
    origin = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    airline = models.CharField(max_length=10)
    fare_basis_code = models.CharField(max_length=50)
    fare_rule_detail = models.TextField(blank=True, null=True)


# ----------------------------------
# Invoice model
# ----------------------------------
class Invoice(models.Model):
    invoice_id = models.IntegerField()
    invoice_no = models.CharField(max_length=50)
    invoice_amount = models.FloatField()
    invoice_status = models.IntegerField()
    invoice_created_on = models.DateTimeField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.invoice_no}"


# ----------------------------------
# Flight Itinerary (primary model)
# ----------------------------------
class FlightItinerary(models.Model):
    # Basic top-level fields
    agent_remarks = models.TextField(blank=True, null=True)
    is_auto_reissuance_allowed = models.BooleanField(default=False)
    issuance_pcc = models.CharField(max_length=50, blank=True, null=True)
    journey_type = models.IntegerField()
    search_combination_type = models.IntegerField()
    trip_indicator = models.IntegerField()
    booking_allowed_for_roamer = models.BooleanField(default=False)
    booking_id = models.IntegerField()
    is_coupon_applicable = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)
    pnr = models.CharField(max_length=20, blank=True, null=True)
    is_domestic = models.BooleanField(default=False)
    result_fare_type = models.CharField(max_length=50, blank=True, null=True)
    source = models.IntegerField()
    origin = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    airline_code = models.CharField(max_length=10)
    last_ticket_date = models.DateTimeField(blank=True, null=True)
    validating_airline_code = models.CharField(max_length=10, blank=True, null=True)
    airline_remark = models.TextField(blank=True, null=True)
    airline_toll_free_no = models.CharField(max_length=20, blank=True, null=True)
    is_lcc = models.BooleanField(default=False)
    non_refundable = models.BooleanField(default=False)
    fare_type = models.CharField(max_length=50, blank=True, null=True)
    credit_note_no = models.CharField(max_length=50, blank=True, null=True)

    # Link main fare
    fare = models.OneToOneField(Fare, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.IntegerField()
    invoice_amount = models.FloatField()
    invoice_no = models.CharField(max_length=50)
    invoice_status = models.IntegerField()
    invoice_created_on = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_web_check_in_allowed = models.BooleanField(default=False)

    # Relationships
    passengers = models.ManyToManyField(Passenger, blank=True)
    segments = models.ManyToManyField(Segment, blank=True)
    fare_rules = models.ManyToManyField(FareRule, blank=True)
    invoices = models.ManyToManyField(Invoice, blank=True)

    def __str__(self):
        return f"PNR: {self.pnr} (BookingID: {self.booking_id})"


# ----------------------------------
# Main API Response model
# ----------------------------------
class Bookings(models.Model):
    search_session = models.ForeignKey(
        SearchSession,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )
    response_status = models.IntegerField()
    trace_id = models.CharField(max_length=100)
    # Link to flight itinerary
    flight_itinerary = models.OneToOneField(FlightItinerary, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"TraceID: {self.trace_id}"
