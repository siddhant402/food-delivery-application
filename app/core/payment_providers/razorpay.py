import uuid
from app.core.payment_providers.base import PaymentProvider


class RazorpayProvider(PaymentProvider):
    def create_payment(self, amount: float) -> str:
        return f"rzp_{uuid.uuid4().hex}"  # stub
