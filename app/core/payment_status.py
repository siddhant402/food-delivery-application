from enum import Enum


class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
