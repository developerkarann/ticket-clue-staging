from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError
import uuid
from datetime import timedelta
from django.utils.timezone import now


class OTP(models.Model):
    email = models.EmailField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.email} - {self.otp}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5)
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s profile"
    

# ----------------------------------
#       SearchSession 
# ----------------------------------

class SearchSession(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='search_sessions', null=True, blank=True)
    hexid = models.CharField(max_length=24, unique=True)
    traceId = models.CharField(max_length=100, null=True, blank=True)
    resultIndex = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seats = models.JSONField(null=True, blank=True)
    meals = models.JSONField(null=True, blank=True)
    baggage = models.JSONField(null=True, blank=True)

    expiry = models.DateTimeField(null=True, blank=True)
    primaryContact = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    bookingId = models.CharField(max_length=50, null=True, blank=True)
    pnr = models.CharField(max_length=50, null=True, blank=True)

    isTicketed = models.BooleanField(null=True, default=False, blank=False)

    booking_response = models.JSONField(null=True, blank=True)
    ticket_response = models.JSONField(null=True, blank=True)
    isLcc = models.BooleanField(null=True,default=False,blank=False)

    passengers = models.ManyToManyField('Passenger', related_name='search_sessions', blank=True)

    # GST Details
    gst_company_address = models.CharField(max_length=100, null=True, blank=True)
    gst_company_contact_number = models.CharField(max_length=20, null=True, blank=True)
    gst_company_name = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=20, null=True, blank=True)
    gst_company_email = models.EmailField(null=True, blank=True)

    payment_status = models.CharField(max_length=20, null=True, blank=True, default='pending', choices=[
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('success', 'Success'),
    ])

    def save(self, *args, **kwargs):
        # Try to generate a unique hexid until it works
        if not self.hexid:  # Only generate if hexid is empty
            self.hexid = uuid.uuid4().hex[:24]
        
        if not self.expiry:
            self.expiry = now() + timedelta(minutes=10)

        while True:
            try:
                with transaction.atomic():
                    super(SearchSession, self).save(*args, **kwargs)
                break  # Exit the loop if successful
            except IntegrityError:
                self.hexid = uuid.uuid4().hex[:24]

    def __str__(self):
        return self.hexid

    def __str__(self):
        return self.hexid
    
    def meal_total(self):
        return sum(
            passenger.meal_preference.Price
            for passenger in self.passengers.all()
            if passenger.meal_preference and hasattr(passenger.meal_preference, "Price")
        )

    def seat_total(self):
        return sum(
            passenger.seat_preference.Price
            for passenger in self.passengers.all()
            if passenger.seat_preference and hasattr(passenger.seat_preference, "Price")
        )

    def baggage_total(self):
        return sum(
            passenger.baggage_preference.Price
            for passenger in self.passengers.all()
            if passenger.baggage_preference and hasattr(passenger.baggage_preference, "Price")
        )

    
    
class Meal(models.Model):
    AirlineCode = models.CharField(max_length=10, null=True, blank=True)
    FlightNumber = models.CharField(max_length=10, null=True, blank=True)
    WayType = models.IntegerField(null=True, blank=True)
    Code = models.CharField(max_length=10, null=True, blank=True)
    Description = models.IntegerField(null=True, blank=True)
    AirlineDescription = models.CharField(max_length=100, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)

    Currency = models.CharField(max_length=10, null=True, blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Origin = models.CharField(max_length=10, null=True, blank=True)
    Destination = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.AirlineCode} {self.FlightNumber} {self.Code}"
    
class Seat(models.Model):
    AirlineCode = models.CharField(max_length=10, null=True, blank=True)
    FlightNumber = models.CharField(max_length=10, null=True, blank=True)
    CraftType = models.CharField(max_length=10, null=True, blank=True)
    Origin = models.CharField(max_length=10, null=True, blank=True)
    Destination = models.CharField(max_length=10, null=True, blank=True)
    AvailablityType = models.IntegerField(null=True, blank=True)
    Description = models.IntegerField(null=True, blank=True)
    Code = models.CharField(max_length=10, null=True, blank=True)
    RowNo = models.CharField(max_length=10, null=True, blank=True)
    SeatNo = models.CharField(max_length=10, null=True, blank=True)
    SeatType = models.IntegerField(null=True, blank=True)
    SeatWayType = models.IntegerField(null=True, blank=True)
    Compartment = models.IntegerField(null=True, blank=True)
    Deck = models.IntegerField(null=True, blank=True)
    Currency = models.CharField(max_length=10, null=True, blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.AirlineCode} {self.FlightNumber} {self.Code}"

class Baggage(models.Model):
    AirlineCode = models.CharField(max_length=10, null=True, blank=True)
    FlightNumber = models.CharField(max_length=10, null=True, blank=True)
    WayType = models.IntegerField(null=True, blank=True)
    Code = models.CharField(max_length=10, null=True, blank=True)
    Description = models.IntegerField(null=True, blank=True)
    Weight = models.IntegerField(null=True, blank=True)

    Currency = models.CharField(max_length=10, null=True, blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Origin = models.CharField(max_length=10, null=True, blank=True)
    Destination = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.AirlineCode} {self.FlightNumber} {self.Code}"

class Fare(models.Model):
    Currency = models.CharField(max_length=10, null=True, blank=True)
    BaseFare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    YQTax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    AdditionalTxnFeeOfrd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    AdditionalTxnFeePub = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    OtherCharges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PublishedFare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    OfferedFare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TdsOnCommission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TdsOnPLB = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TdsOnIncentive = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ServiceFee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    air_trans_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

class Passenger(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Mstr', 'Mstr'),
    ]

    PAX_TYPE_CHOICES = [
        (1, 'Adult'),
        (2, 'Child'),
        (3, 'Infant'),
    ]

    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
    ]

    # Passenger Details
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    pax_type = models.IntegerField(choices=PAX_TYPE_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    passport_no = models.CharField(max_length=50, null=True, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    passport_issue = models.DateField(null=True, blank=True)
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    country_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_lead_pax = models.BooleanField(null=True, blank=True)

    # Fare
    fare = models.ForeignKey(Fare, on_delete=models.CASCADE, null=True, blank=True)

    # SSR options
    meal_preference = models.OneToOneField(Meal, related_name='passengers',on_delete=models.CASCADE,null=True, blank=True)
    seat_preference =  models.OneToOneField(Seat, related_name='passengers',on_delete=models.CASCADE,null=True, blank=True)
    baggage_preference =  models.OneToOneField(Baggage, related_name='passengers',on_delete=models.CASCADE,null=True, blank=True)
    # ff_airline_code = models.CharField(max_length=10, null=True, blank=True)
    # ff_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FlightLead(models.Model):
    from_location = models.CharField(max_length=100, null=True, blank=True)
    to_location = models.CharField(max_length=100, null=True, blank=True)

    multicity_from = models.CharField(max_length=100, null=True, blank=True)
    multicity_to = models.CharField(max_length=100, null=True, blank=True)

    departure_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_location} to {self.to_location} on {self.departure_date}"
