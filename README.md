# 🛴 ScooTrack — Scooter Rental Management System

> A CLI-based OOP Python system for managing scooter rentals, processing payments, generating itemized receipts, and tracking fleet revenue.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![OOP](https://img.shields.io/badge/OOP-Encapsulation%20%7C%20Polymorphism%20%7C%20Abstraction-green?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-7%20passing-brightgreen?style=flat-square)

---

## 📌 What It Does

ScooTrack manages a fleet of scooters for a rental shop. It handles the full rental lifecycle — from checking out scooters to processing payments and printing itemized receipts — using clean OOP design with encapsulation, polymorphism, and abstract interfaces.

---

## 📸 Demo

![ScooTrack Demo](screenshots/demo.jpg)

---

## 🚀 Features

- Rent 1–5 scooters per transaction (hourly, daily, or weekly)
- Automatic 30% discount applied for 3–5 scooter rentals
- Itemized receipt generated for every completed rental
- Unique UUID transaction ID per rental
- Cash and card payment support (card adds 2% processing fee)
- Maintenance tracking — flags scooters after every 10 rides
- Revenue and rental history tracking
- Full shop report with inventory and earnings summary
- 7 passing unit tests covering all business rules

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| OOP Principles | Encapsulation, Polymorphism, Abstraction |
| Built-in Libraries | datetime, math, uuid, enum, abc, unittest |
| Testing | unittest |

---

## 🏗️ Class Structure

```
ScooterRental        ← manages fleet, processes rentals and returns
├── Scooter          ← represents a single scooter with maintenance tracking
├── RentalTransaction← full lifecycle of one rental (cost, receipt, duration)
├── IPaymentProcess  ← abstract payment interface
│   ├── CashPayment  ← no fee
│   └── CardPayment  ← 2% processing fee
└── RentalPeriod     ← HOURLY ($5) | DAILY ($20) | WEEKLY ($50)
```

---

## 🧪 Test Cases

| # | Test | Covers |
|---|---|---|
| 1 | Cash payment processes correctly | Payment handling |
| 2 | Card payment adds 2% fee | Fee calculation |
| 3 | Negative payment raises ValueError | Input validation |
| 4 | Zero payment raises ValueError | Input validation |
| 5 | Revenue increases after rental | Revenue tracking |
| 6 | 30% discount applied for 3 scooters | Discount logic |
| 7 | Duplicate rental raises ValueError | Business rule enforcement |

---

## 🏃 How to Run

```bash
# Clone the repo
git clone https://github.com/Nateit1/scootrack.git
cd scootrack

# Run the demo
python scootrack.py

# Run unit tests
python -m pytest test_scootrack.py -v
```

No external dependencies — uses Python standard library only.

---

## 🔗 Links

- 💼 [Portfolio](https://af19o4udzm.mobirisesite.com/)
