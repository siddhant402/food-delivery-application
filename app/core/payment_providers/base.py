from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    @abstractmethod
    def create_payment(self, amount: float) -> str:
        pass
