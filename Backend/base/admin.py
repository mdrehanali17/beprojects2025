
from django.contrib import messages
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SportDetails, SportImage, Booking, Payment
from django.forms import  inlineformset_factory


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'phone_number')
    list_filter = ('email', 'username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'phone_number')}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

# Sport Details Admin
class SportDetailsAdminForm(forms.ModelForm):
    class Meta:
        model = SportDetails
        fields = '__all__'

SportImageFormSet = inlineformset_factory(
    SportDetails, SportImage, fields=('image',), extra=1, can_delete=True
)

class SportImageInline(admin.TabularInline):
    model = SportImage
    formset = SportImageFormSet
    extra = 1

@admin.register(SportDetails)
class SportDetailsAdmin(admin.ModelAdmin):
    form = SportDetailsAdminForm
    inlines = [SportImageInline]

    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')
    list_filter = ('category', 'price')

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'location', 'price')
        }),
    )


# Booking Admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport_custom_id', 'sport_category', 'date', 'start_time', 'end_time', 'phone_number', 'amount', 'payment_status', 'booking_date', 'booking_id')
    search_fields = ('user__email', 'sport_custom_id', 'booking_id')
    list_filter = ('date', 'payment_status')
    autocomplete_fields = ['user']

    def save_model(self, request, obj, form, change):
        if change:  # Check if the object is being changed (not created)
            original_booking = Booking.objects.get(pk=obj.pk)
            if original_booking.payment_status == 'Paid' and obj.payment_status == 'Pending':
                messages.error(request, "Cannot change payment status from Paid to Pending.")
                return
        
        super().save_model(request, obj, form, change)


# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'phone_number', 'transaction_uuid')
    search_fields = ('booking__booking_id', 'phone_number')
    list_filter = ('payment_method',)