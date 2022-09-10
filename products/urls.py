from django.urls import path
from products.views import (
    CreateCheckoutSessionView,
    ItemPageView,
    SuccessView,
    CancelView,
    HomePageView,
)

urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('', HomePageView.as_view(), name='home-page'),
    path('item/<int:pk>', ItemPageView.as_view(), name='item'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
