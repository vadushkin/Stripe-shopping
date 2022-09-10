import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "products/success.html"


class CancelView(TemplateView):
    template_name = "products/cancel.html"


class ItemPageView(TemplateView):
    template_name = "products/item.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        product = Item.objects.get(pk=pk)
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class HomePageView(TemplateView):
    template_name = "products/home.html"

    def get_context_data(self, **kwargs):
        products = Item.objects.all()
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "items": products,
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Item.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
