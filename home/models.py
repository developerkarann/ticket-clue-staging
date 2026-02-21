from django.db import models
from django.utils.text import slugify
import uuid
from ckeditor.fields import RichTextField

class Airline(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    # Basic Information
    slug = models.SlugField(unique=False, editable=False)
    logo = models.ImageField(upload_to='airlines/', null=True, blank=True)
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    hero_image = models.URLField(blank=True, null=True)
    hub = models.CharField(max_length=255)
    call_sign = models.CharField(max_length=100, blank=True, null=True)
    headquarters = models.CharField(max_length=255)
    popular_route = models.CharField(max_length=255, blank=True, null=True)
    
    # Popular Destinations
    popular_destinations = models.TextField(blank=True, null=True)
    
    # Travel Insights
    senior_travelers_percentage = models.CharField(max_length=50, blank=True, null=True)
    child_travelers_percentage = models.CharField(max_length=50, blank=True, null=True)
    millennial_travelers_percentage = models.CharField(max_length=50, blank=True, null=True)
    female_travelers_percentage = models.CharField(max_length=50, blank=True, null=True)
    premium_class_bookings_percentage = models.CharField(max_length=50, blank=True, null=True)
    most_popular_destination = models.CharField(max_length=255, blank=True, null=True)
    most_popular_airport = models.CharField(max_length=255, blank=True, null=True)
    
    # Description and Tips
    description = models.TextField(blank=True, null=True)
    booking_tips = models.TextField(blank=True, null=True)
    
    # FAQs
    faq = models.ManyToManyField('FAQ', blank=True)
    
    # Contact Information
    support_number = models.CharField(max_length=50, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    


class DirectFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None

class FlightFrom(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    

class CityVacationPackage(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    
class InternationalFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    

class AirlineVacationPackage(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    

class LastMinuteFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    

class OneWayFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    


class RoundTripFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None
    

class NonStopFlight(models.Model):
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the content, e.g., 'Direct Flights to Costa'",
        null=True,
    )
    slug = models.SlugField(unique=False, editable=False, null=True)
    intro = RichTextField(
        null=True,
    )
    
    advantages_heading = models.CharField(
        max_length=255,
        default="",
        help_text="Heading for the advantages section.",
        null=True,
    )
    advantages = RichTextField(
        null=True,
    )
    
    airlines_heading = models.CharField(
        max_length=255,
        help_text="Heading for the airlines section.",
        null=True,
    )
    major_airlines = RichTextField(
        null=True,
    )
    
    cities_heading = models.CharField(
        max_length=255,
        help_text="Heading for the cities section.",
        null=True,
    )
    popular_cities = RichTextField(
        null=True,
    )

    faq = models.ManyToManyField('FAQ', blank=True)
   
    
    image = models.ImageField(
        upload_to='limited_time_offers/',
        help_text="Promotional image for the direct flight offer.",
        null=True,
    )
    description = models.TextField(
        null=True,
    )
    rating = models.FloatField(
        null=True, blank=True,
        help_text="Rating for the direct flight offer.",
    )
    
    discount = models.FloatField(
        null=True, blank=True,
        help_text="Discount percentage if applicable.",
    )
    price = models.FloatField(
        null=True, blank=True,
        help_text="Price for the direct flight offer.",
    )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount/100)
        return None

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    hex = models.CharField(max_length=32, unique=True, blank=True, editable=False)
    excerpt = models.TextField(help_text="A short description for blog listings")
    content = RichTextField()
    featured_image = models.ImageField(upload_to='blogs/')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Space-separated tags")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.hex:
            self.hex = uuid.uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title

class HomeFaq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
