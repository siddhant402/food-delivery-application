import uuid
from app.core.payment_providers.base import PaymentProvider


class StripeProvider(PaymentProvider):
    def create_payment(self, amount: float) -> str:
        return f"stripe_{uuid.uuid4().hex}"  # stub
