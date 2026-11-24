from abc import ABC, abstractmethod

class PaymentInstrument(ABC):
    @abstractmethod
    def get_identifier(self):
        pass

    @abstractmethod
    def execute_transaction(self, amount):
        pass


class CardInstrument(PaymentInstrument):
    def __init__(self, card_no, provider_name):
        self.card_no = card_no
        self.provider_name = provider_name

    def get_identifier(self):
        return self.card_no

    def execute_transaction(self, amount):
        print(f"Payment of {amount} made using {self.provider_name} Card")
        return True


class UpiInstrument(PaymentInstrument):
    def __init__(self, vpa, provider_name):
        self.vpa = vpa
        self.provider_name = provider_name

    def get_identifier(self):
        return self.vpa

    def execute_transaction(self, amount):
        print(f"Payment of {amount} made using {self.provider_name} UPI")
        return True


class PaymentGateway(ABC):
    def __init__(self, title, fee_percent):
        self.title = title
        self.fee_percent = fee_percent

    @abstractmethod
    def build_instrument(self, mode, credential):
        pass

    def process_payment(self, mode, credential, amount):
        instrument = self.build_instrument(mode, credential)
        print(f"Processing through {self.title}")
        print(f"Processing fee: {self.fee_percent} %")
        return instrument.execute_transaction(amount)


class RazorpayGateway(PaymentGateway):
    def __init__(self):
        super().__init__("Razorpay", 2.0)

    def build_instrument(self, mode, credential):
        if mode == "card":
            return CardInstrument(credential, self.title)
        elif mode == "upi":
            return UpiInstrument(credential, self.title)
        raise ValueError("Unsupported payment mode for Razorpay")


class StripeGateway(PaymentGateway):
    def __init__(self):
        super().__init__("Stripe", 2.9)

    def build_instrument(self, mode, credential):
        if mode == "card":
            return CardInstrument(credential, self.title)
        elif mode == "upi":
            return UpiInstrument(credential, self.title)
        raise ValueError("Unsupported payment mode for Stripe")


class GatewayRegistry:
    _gateways = {
        "razorpay": RazorpayGateway,
        "stripe": StripeGateway
    }

    @classmethod
    def add_gateway(cls, key, gateway_cls):
        cls._gateways[key.lower()] = gateway_cls

    @classmethod
    def fetch(cls, key):
        gateway_cls = cls._gateways.get(key.lower())
        if not gateway_cls:
            raise ValueError("Invalid gateway selected")
        return gateway_cls()

def run_checkout():
    print("Multi-Gateway Payment Processing\n")

    try:
        selected_gateway = input("Select gateway (stripe/razorpay): ").strip().lower()
        gateway = GatewayRegistry.fetch(selected_gateway)

        mode = input("Select payment method (card/upi): ").strip().lower()

        if mode == "card":
            detail = input("Enter card number: ").strip()
        elif mode == "upi":
            detail = input("Enter UPI ID: ").strip()
        else:
            print("Invalid payment method")
            return

        amt = float(input("Enter amount: "))
        status = gateway.process_payment(mode, detail, amt)

        if status:
            print("Payment successful")
        else:
            print("Payment failed")

    except ValueError as err:
        print("Error:", err)
    except Exception as err:
        print("Something went wrong:", err)


if __name__ == "__main__":
    run_checkout()