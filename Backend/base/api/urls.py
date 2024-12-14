from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from .views import BookingListCreateView, BookingDetailView, PaymentListCreateView, PaymentDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('signup/', views.signup, name='Signup'),
    path('signin/', views.signin, name='Signin'),

    path('users/<int:user_id>/', views.get_user_details, name='user-detail'),

    # Updated URLs to handle multiple sports
    path('latest-sports/', views.latest_sports_by_category, name='latest-sports-by-category'),
    path('sports/category/<str:category>/', views.sport_by_category, name='sport-by-category'),

    path('sportDetails/<int:id>/', views.sport_detail, name='sport_detail'),  
    path('increase_view_count/<int:sport_id>/', views.increase_view_count, name='increase_view_count'),
    path('recommendations/<int:user_id>/', views.recommendations_view, name='recommendations'),


    path('availability/', views.check_availability, name='check_availability'),

    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),

    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),

    path('booking-history/', views.booking_history, name='booking_history'),
]
