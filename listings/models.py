

import uuid
from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    available_from = models.DateField()
    available_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    class Meta:
        unique_together = ('user', 'listing', 'start_date', 'end_date')

    def __str__(self):
        return f"{self.customer_name} booking {self.listing.title}"


class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"Review by {self.reviewer_name} on {self.listing.title}"
