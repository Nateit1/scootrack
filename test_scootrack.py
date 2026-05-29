"""
ScooTrack — Unit Tests
7 test cases covering rental lifecycle, discounts,
business rules, and payment processing.
"""

import unittest
from scootrack import (
    ScooterRental, RentalPeriod,
    CashPayment, CardPayment
)


class TestScooTrack(unittest.TestCase):

    # Test 1: Cash payment processes correctly
    def test_cash_payment_valid(self):
        self.assertEqual(CashPayment().process_payment(100), 100)

    # Test 2: Card payment adds 2% fee
    def test_card_payment_valid(self):
        self.assertAlmostEqual(CardPayment().process_payment(100), 102)

    # Test 3: Negative payment raises error
    def test_negative_payment(self):
        with self.assertRaises(ValueError):
            CashPayment().process_payment(-50)

    # Test 4: Zero payment raises error
    def test_zero_payment(self):
        with self.assertRaises(ValueError):
            CardPayment().process_payment(0)

    # Test 5: Revenue increases after completed rental
    def test_rental_calculation(self):
        shop = ScooterRental()
        shop.add_scooter("S1", "Standard")
        shop.rent_scooter("Nathan Tsegai", 1, RentalPeriod.HOURLY)
        shop.return_scooter("Nathan Tsegai", CashPayment())
        self.assertGreater(shop.get_total_revenue(), 0)

    # Test 6: 30% discount applied for 3 scooters
    def test_discount_application(self):
        shop = ScooterRental()
        for i in range(3):
            shop.add_scooter(f"S{i}", "Standard")
        shop.rent_scooter("Ephy Njuguna", 3, RentalPeriod.HOURLY)
        t = shop.get_active_rentals()[0]
        shop.return_scooter("Ephy Njuguna", CashPayment())
        self.assertTrue(t.get_discount_applied())

    # Test 7: Duplicate active rental raises error
    def test_business_rule_enforcement(self):
        shop = ScooterRental()
        shop.add_scooter("S1", "Standard")
        shop.rent_scooter("Tylen Holloway", 1, RentalPeriod.HOURLY)
        with self.assertRaises(ValueError):
            shop.rent_scooter("Tylen Holloway", 1, RentalPeriod.DAILY)


if __name__ == "__main__":
    unittest.main()
