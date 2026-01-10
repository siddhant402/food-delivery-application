from app.core.payment_providers.razorpay import RazorpayProvider
from app.core.payment_providers.stripe import StripeProvider

PROVIDERS = {
    "razorpay": RazorpayProvider,
    "stripe": StripeProvider,
}


def get_payment_provider(name: str):
    provider_cls = PROVIDERS.get(name.lower())
    if not provider_cls:
        raise ValueError("Unsupported payment provider")
    return provider_cls()
