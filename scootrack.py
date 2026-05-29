"""
ScooTrack — Scooter Rental Management System
A CLI-based OOP Python system for managing scooter rentals,
processing payments, generating receipts, and tracking revenue.
"""

from datetime import datetime
import math
import uuid
from enum import Enum
from abc import ABC, abstractmethod


# ── Rental Period Enum ────────────────────────────────────────────────────────

class RentalPeriod(Enum):
    HOURLY = 5    # $5 per scooter per hour
    DAILY  = 20   # $20 per scooter per day
    WEEKLY = 50   # $50 per scooter per week


# ── Scooter Class ─────────────────────────────────────────────────────────────

class Scooter:
    """Represents a single scooter in the rental fleet."""

    def __init__(self, scooterID, model):
        self.__scooterID        = scooterID
        self.__model            = model
        self.__rides            = 0
        self.__needsMaintenance = False
        self.__availability     = True

    def get_id(self):
        return self.__scooterID

    def get_model(self):
        return self.__model

    def is_available(self):
        return self.__availability

    def set_available(self, status):
        self.__availability = status

    def increment_ride_count(self):
        self.__rides += 1
        self.maintenanceChecker()

    def maintenanceChecker(self):
        if self.__rides % 10 == 0 and self.__rides > 0:
            self.__needsMaintenance = True
            print("Scooter needs maintenance")
        else:
            self.__needsMaintenance = False
            print("Scooter doesn't need maintenance")
        return self.__needsMaintenance

    def performMaintenance(self):
        self.__needsMaintenance = False
        self.__rides            = 0
        print("Scooter maintenance is complete")


# ── Rental Transaction Class ──────────────────────────────────────────────────

class RentalTransaction:
    """Manages the full lifecycle of a single scooter rental."""

    def __init__(self, customer_id, scooters, rental_period):
        self.__transaction_id   = str(uuid.uuid4())
        self.__customer_id      = customer_id
        self.__scooters         = scooters
        self.__rental_period    = rental_period
        self.__start_time       = datetime.now()
        self.__end_time         = None
        self.__is_active        = True
        self.__total_cost       = 0.0
        self.__discount_applied = False

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_transaction_id(self):   return self.__transaction_id
    def get_customer_id(self):      return self.__customer_id
    def get_scooters(self):         return self.__scooters
    def get_rental_period(self):    return self.__rental_period
    def get_start_time(self):       return self.__start_time
    def get_end_time(self):         return self.__end_time
    def get_is_active(self):        return self.__is_active
    def get_total_cost(self):       return self.__total_cost
    def get_discount_applied(self): return self.__discount_applied

    # ── Core Methods ──────────────────────────────────────────────────────────

    def calculate_duration(self):
        if self.__end_time is None:
            raise ValueError("Rental has not ended yet.")
        total_seconds = (self.__end_time - self.__start_time).total_seconds()
        if total_seconds <= 0:
            raise ValueError("End time must be after start time.")
        if self.__rental_period == RentalPeriod.HOURLY:
            return math.ceil(total_seconds / 3600)
        elif self.__rental_period == RentalPeriod.DAILY:
            return math.ceil(total_seconds / 86400)
        elif self.__rental_period == RentalPeriod.WEEKLY:
            return math.ceil(total_seconds / 604800)
        else:
            raise ValueError("Invalid rental period.")

    def apply_discount(self, base_cost):
        """Apply 30% discount for rentals of 3-5 scooters."""
        num_scooters = len(self.__scooters)
        if 3 <= num_scooters <= 5:
            self.__discount_applied = True
            return round(base_cost * 0.70, 2)
        self.__discount_applied = False
        return round(base_cost, 2)

    def calculate_cost(self):
        duration     = self.calculate_duration()
        num_scooters = len(self.__scooters)
        rate         = self.__rental_period.value
        base_cost    = rate * duration * num_scooters
        self.__total_cost = self.apply_discount(base_cost)
        return self.__total_cost

    def generate_receipt(self):
        if self.__is_active:
            raise ValueError("Cannot generate receipt: rental is still active.")
        duration     = self.calculate_duration()
        num_scooters = len(self.__scooters)
        rate         = self.__rental_period.value
        base_cost    = rate * duration * num_scooters
        scooter_ids  = [s.get_id() for s in self.__scooters]
        fmt          = '%Y-%m-%d %H:%M:%S'

        receipt = f"""
================================
         RENTAL RECEIPT
================================
Transaction ID : {self.__transaction_id}
Customer ID    : {self.__customer_id}
Scooter IDs    : {scooter_ids}
Rental Period  : {self.__rental_period.name}
Start Time     : {self.__start_time.strftime(fmt)}
End Time       : {self.__end_time.strftime(fmt)}
Duration       : {duration} {self.__rental_period.name.lower()}(s)
--------------------------------
Rate           : ${rate:.2f} per {self.__rental_period.name.lower()}
Scooters       : {num_scooters}
Base Cost      : ${base_cost:.2f}
Discount       : {'30% applied' if self.__discount_applied else 'None'}
--------------------------------
TOTAL (USD)    : ${self.__total_cost:.2f}
================================
        """
        print(receipt)
        return receipt

    def complete_rental(self):
        if not self.__is_active:
            raise ValueError("This rental is already completed.")
        self.__end_time  = datetime.now()
        self.__is_active = False
        self.calculate_cost()


# ── Scooter Rental (Shop) Class ───────────────────────────────────────────────

class ScooterRental:
    """Manages the scooter fleet, rentals, payments, and revenue."""

    def __init__(self):
        self.__inventory      = []
        self.__active_rentals = []
        self.__rental_history = []
        self.__total_revenue  = 0.0

    def add_scooter(self, scooterID, model):
        self.__inventory.append(Scooter(scooterID, model))

    def get_available_scooters(self):
        return [s for s in self.__inventory if s.is_available()]

    def get_total_scooters(self):
        return len(self.__inventory)

    def get_scooters_needing_maintenance(self):
        return [s for s in self.__inventory if s._Scooter__needsMaintenance]

    def shop_report(self):
        print("Scooter Shop Report:")
        print(f"  Total scooters     : {self.get_total_scooters()}")
        print(f"  Available          : {len(self.get_available_scooters())}")
        print(f"  Needs maintenance  : {len(self.get_scooters_needing_maintenance())}")
        print(f"  Active Rentals     : {len(self.__active_rentals)}")
        print(f"  Total Revenue      : ${self.__total_revenue:.2f} USD")

    def rent_scooter(self, customer_id, num_scooters, rental_period):
        if not customer_id:
            raise ValueError("Customer ID cannot be empty.")
        if not isinstance(num_scooters, int) or num_scooters <= 0:
            raise ValueError("Number of scooters must be a positive integer.")
        if not isinstance(rental_period, RentalPeriod):
            raise ValueError("Invalid rental period.")
        for t in self.__active_rentals:
            if t.get_customer_id() == customer_id:
                raise ValueError(f"Customer {customer_id} already has an active rental.")
        available = self.get_available_scooters()
        if num_scooters > len(available):
            raise ValueError(f"Not enough scooters. Requested: {num_scooters}, Available: {len(available)}.")
        selected = available[:num_scooters]
        for scooter in selected:
            scooter.set_available(False)
        transaction = RentalTransaction(customer_id, selected, rental_period)
        self.__active_rentals.append(transaction)
        print(f"Rental started: {customer_id} | {rental_period.name} | {[s.get_id() for s in selected]}")
        return transaction

    def return_scooter(self, customer_id, payment_processor):
        transaction = next((t for t in self.__active_rentals if t.get_customer_id() == customer_id), None)
        if transaction is None:
            raise ValueError(f"No active rental found for {customer_id}.")
        transaction.complete_rental()
        payment_processor.process_payment(transaction.get_total_cost())
        transaction.generate_receipt()
        for scooter in transaction.get_scooters():
            scooter.set_available(True)
            scooter.increment_ride_count()
        self.__total_revenue += transaction.get_total_cost()
        self.__rental_history.append(transaction)
        self.__active_rentals.remove(transaction)
        print(f"Rental completed: {customer_id}")
        return transaction

    def get_active_rentals(self):   return self.__active_rentals
    def get_rental_history(self):   return self.__rental_history
    def get_total_revenue(self):    return self.__total_revenue

    def get_customer_history(self, customer_id):
        return [t for t in self.__rental_history if t.get_customer_id() == customer_id]


# ── Payment Interface & Implementations ──────────────────────────────────────

class IPaymentProcess(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> float:
        pass

class CashPayment(IPaymentProcess):
    def process_payment(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        return amount

class CardPayment(IPaymentProcess):
    def process_payment(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        return amount * 1.02  # 2% processing fee


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    shop = ScooterRental()
    for i in range(1, 7):
        shop.add_scooter(f"Scooter{i}", "Standard" if i % 2 != 0 else "Premium")

    cash = CashPayment()
    card = CardPayment()

    # Example 1: Hourly rental, cash payment
    shop.rent_scooter("Peter Griffin", 1, RentalPeriod.HOURLY)
    shop.return_scooter("Peter Griffin", cash)

    # Example 2: Daily rental, card payment (2% fee)
    shop.rent_scooter("Jane Smith", 1, RentalPeriod.DAILY)
    shop.return_scooter("Jane Smith", card)

    # Example 3: Weekly rental
    shop.rent_scooter("Alice Brown", 1, RentalPeriod.WEEKLY)
    shop.return_scooter("Alice Brown", cash)

    # Example 4: 3 scooters — 30% discount applied
    shop.rent_scooter("Group Z", 3, RentalPeriod.DAILY)
    shop.return_scooter("Group Z", cash)

    print(f"\nTotal Revenue     : ${shop.get_total_revenue():.2f} USD")
    print(f"Completed Rentals : {len(shop.get_rental_history())}")
    print()
    shop.shop_report()
