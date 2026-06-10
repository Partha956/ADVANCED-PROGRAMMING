from abc import ABC, abstractmethod
from dataclasses import dataclass

# ==========================================
# 1. Models & Open/Closed Principle (OCP) + Liskov Substitution Principle (LSP)
# ==========================================

@dataclass
class Order(ABC):
    """Base Order class demonstrating LSP. All subclasses must be substitutable."""
    order_id: str
    customer_name: str
    base_amount: float

    @abstractmethod
    def get_final_amount(self) -> float:
        """Calculate the final amount based on the specific order type."""
        pass

@dataclass
class RegularOrder(Order):
    def get_final_amount(self) -> float:
        return self.base_amount

@dataclass
class DiscountedOrder(Order):
    discount_percentage: float

    def get_final_amount(self) -> float:
        return self.base_amount * (1 - (self.discount_percentage / 100))

@dataclass
class PriorityOrder(Order):
    priority_fee: float

    def get_final_amount(self) -> float:
        return self.base_amount + self.priority_fee


# ==========================================
# 2. Interfaces (Interface Segregation Principle - ISP)
# ==========================================

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass

class OrderStorage(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass


# ==========================================
# 3. Concrete Implementations (Open/Closed Principle - OCP)
# ==========================================

# --- Payment Methods ---
class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f" Processing Credit Card payment of ${amount:.2f}")
        return True

class UPIPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f" Processing UPI payment of ${amount:.2f}")
        return True

class WalletPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f" Processing Wallet payment of ${amount:.2f}")
        return True

# --- Notification Channels ---
class EmailNotifier(Notifier):
    def send_notification(self, message: str) -> None:
        print(f" Sending Email: {message}")

class SMSNotifier(Notifier):
    def send_notification(self, message: str) -> None:
        print(f" Sending SMS: {message}")

class PushNotifier(Notifier):
    def send_notification(self, message: str) -> None:
        print(f" Sending Push Notification: {message}")

# --- Storage Mechanisms ---
class DatabaseStorage(OrderStorage):
    def save(self, order: Order) -> None:
        print(f" Saving Order {order.order_id} to Database.")

class FileStorage(OrderStorage):
    def save(self, order: Order) -> None:
        print(f" Saving Order {order.order_id} to File System.")



# 4. Service Layer (Dependency Inversion Principle - DIP & Single Responsibility - SRP)

class OrderService:
    """
    High-level module. It does not depend on concrete classes (like EmailNotifier),
    but rather on abstractions (Notifier). Dependencies are injected.
    """
    def __init__(
        self, 
        payment_processor: PaymentProcessor, 
        notifier: Notifier, 
        storage: OrderStorage
    ):
        self.payment_processor = payment_processor
        self.notifier = notifier
        self.storage = storage

    def process_order(self, order: Order) -> None:
        print(f"\n--- Starting Processing for {order.__class__.__name__}: {order.order_id} ---")
        
        final_amount = order.get_final_amount()
        
        # 1. Process Payment
        payment_success = self.payment_processor.process_payment(final_amount)
        
        if payment_success:
            # 2. Save Order Data
            self.storage.save(order)
            
            # 3. Send Notification
            self.notifier.send_notification(
                f"Hello {order.customer_name}, your order {order.order_id} was successfully placed."
            )
        else:
            self.notifier.send_notification(
                f"Hello {order.customer_name}, payment failed for your order {order.order_id}."
            )


# ==========================================
# 5. Example Execution
# ==========================================
if __name__ == "__main__":
    # Scenario 1: A Regular Order via UPI, Database, and SMS
    order1 = RegularOrder(order_id="ORD101", customer_name="Debankur", base_amount=100.0)
    service1 = OrderService(
        payment_processor=UPIPayment(),
        notifier=SMSNotifier(),
        storage=DatabaseStorage()
    )
    service1.process_order(order1)

    # Scenario 2: A Discounted Order via Credit Card, File Storage, and Email
    order2 = DiscountedOrder(order_id="ORD102", customer_name="Ritom", base_amount=200.0, discount_percentage=15.0)
    service2 = OrderService(
        payment_processor=CreditCardPayment(),
        notifier=EmailNotifier(),
        storage=FileStorage()
    )
    service2.process_order(order2)

    # Scenario 3: A Priority Order via Wallet, Database, and Push Notification
    order3 = PriorityOrder(order_id="ORD103", customer_name="Partha", base_amount=50.0, priority_fee=12.5)
    service3 = OrderService(
        payment_processor=WalletPayment(),
        notifier=PushNotifier(),
        storage=DatabaseStorage()
    )
    service3.process_order(order3)