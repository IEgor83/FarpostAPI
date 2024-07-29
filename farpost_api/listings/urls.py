from django.urls import path
from .views import ListingDetailView, ListingView

urlpatterns = [
    path('listing/', ListingView.as_view(), name='listing'),
    path('listing/<int:listing_id>/', ListingDetailView.as_view(), name='listing-detail'),
]
