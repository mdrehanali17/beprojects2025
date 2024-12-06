import os
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# For handling the images to delete when Turf is deleted. For related code see the last of this file
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

# user Model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email 



# Sport Model
class SportCategoryCounter(models.Model):
    category = models.CharField(max_length=100, unique=True)  # Each category has a unique counter
    count = models.PositiveIntegerField(default=0)  # Persistent count

    def __str__(self):
        return f"{self.category} ({self.count})"


class SportDetails(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Category of the sport (e.g., Futsal, Basketball, Cricket)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Location of the sports facility
    price = models.FloatField()
    sport_custom_id = models.CharField(max_length=20, unique=True, editable=False)  # Custom ID field
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sport_custom_id:
            # Get or create a counter for the category
            counter, created = SportCategoryCounter.objects.get_or_create(category=self.category)
            
            # Increment the count
            counter.count += 1
            counter.save()
            
            # Generate custom ID with the updated count
            self.sport_custom_id = f"{self.category.lower()}{counter.count:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sport_custom_id})"
    
# Sport Image Model
class SportImage(models.Model):
    sport = models.ForeignKey(SportDetails, related_name='sport_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sports/')

    def __str__(self):
        return f"Image for {self.sport.name} ({self.sport.sport_custom_id})"
    
    
#Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    booking_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sport = models.ForeignKey(SportDetails, on_delete=models.CASCADE)  
    sport_custom_id = models.CharField(max_length=50)  
    sport_category = models.CharField(max_length=100) 
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    booking_date = models.DateTimeField()

    

    def __str__(self):
        return self.booking_id

#Payment Model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online Payment'),
        ('cash', 'Cash'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    phone_number = models.CharField(max_length=15)
    transaction_uuid = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Payment for {self.booking.sport.name} by {self.booking.user.email} - {self.amount} via {self.payment_method}"

# Temporary Table for storing Booking data

class TemporaryBookingData(models.Model):
    booking_id = models.CharField(max_length=50, unique=True)
    transaction_uuid = models.UUIDField(editable=False, unique=True)
    sport = models.CharField(max_length=100)
    user_id = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    sport_custom_id = models.CharField(max_length=20)  # Reference to the sport's custom_id
    sport_category = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.booking_id

# For handling the images from the media folder 

@receiver(post_delete, sender=SportImage)
def delete_sport_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_delete, sender=SportDetails)
def delete_related_images(sender, instance, **kwargs):
    for image in instance.sport_images.all():
        if image.image:
            if os.path.isfile(image.image.path):
                os.remove(image.image.path)