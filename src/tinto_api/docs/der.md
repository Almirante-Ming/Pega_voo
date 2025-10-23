# Tinto API — Updated Data Model

This document outlines the updated SQL data model for the Tinto flight booking system, reflecting structural improvements, naming standardization, and relational integrity.

## Updates

- All table and field names standardized to English
- Removed Redis-based seat control; seat management handled entirely in SQL
- Refactored `flights` table to include aircraft and seat class breakdown
- Separated passengers from tickets using direct foreign keys
- Added `seats` table for granular seat tracking
- Improved `purchase_history` with payment method and total amount
- Added `ticket_status_log` for audit trail of ticket status changes

---

## Tables

### 1. `users`

| Field           | Type       | Description |
|----------------|------------|-------------|
| id             | integer    | Primary key |
| full_name      | string     | Required |
| cpf            | string     | Unique, required |
| birth_date     | date       | Required |
| gender         | enum       | MALE, FEMALE, OTHER |
| phone_number   | string     | Required |
| email          | string     | Unique, required |
| hashed_password| string     | Nullable |
| status         | enum       | ACTIVE, INACTIVE, DELETED |
| user_type      | enum       | CUSTOMER, COMPANY_ADMIN, SYSADMIN |
| created_at     | datetime   | Auto-set |
| updated_at     | datetime   | Auto-update |

---

### 2. `purchase_history`

| Field           | Type       | Description |
|----------------|------------|-------------|
| id             | integer    | Primary key |
| user_id        | integer    | FK → `users.id` |
| status         | enum       | ACTIVE, PLANNED, PAST |
| total_amount   | decimal    | Total purchase value |
| payment_method | enum       | CREDIT, DEBIT, PIX, CASH |
| created_at     | datetime   | Auto-set |
| updated_at     | datetime   | Auto-update |

---

### 3. `flights`

| Field             | Type       | Description |
|------------------|------------|-------------|
| id               | integer    | Primary key |
| airline_id       | integer    | FK → `airlines.id` |
| aircraft_model   | string     | Required |
| flight_number    | string     | Unique |
| origin_city      | string     | Required |
| origin_airport   | string     | IATA code |
| destination_city | string     | Required |
| destination_airport | string  | IATA code |
| departure_time   | datetime   | Required |
| estimated_arrival| datetime   | Required |
| economy_seats    | integer    | Total economy seats |
| business_seats   | integer    | Total business seats |
| first_seats      | integer    | Total first class seats |
| status           | enum       | SCHEDULED, CANCELLED |
| created_at       | datetime   | Auto-set |
| updated_at       | datetime   | Auto-update |

---

### 4. `tickets`

| Field             | Type       | Description |
|------------------|------------|-------------|
| id               | integer    | Primary key |
| purchase_id      | integer    | FK → `purchase_history.id` |
| flight_id        | integer    | FK → `flights.id` |
| passenger_id     | integer    | FK → `users.id` |
| seat_class       | enum       | ECONOMY, BUSINESS, FIRST |
| seat_number      | string     | Optional |
| price            | decimal    | Required |
| boarding_time    | datetime   | Required |
| arrival_time     | datetime   | Required |
| status           | enum       | MARKED, RESERVED, CANCELLED, COMPLETED |
| created_at       | datetime   | Auto-set |
| updated_at       | datetime   | Auto-update |

---

### 5. `seats`

| Field         | Type     | Description |
|---------------|----------|-------------|
| id            | integer  | Primary key |
| flight_id     | integer  | FK → `flights.id` |
| seat_number   | string   | e.g., 12A |
| seat_class    | enum     | ECONOMY, BUSINESS, FIRST |
| is_available  | boolean  | Default TRUE |
| ticket_id     | integer  | FK → `tickets.id`, nullable |
| Constraints   |          | UNIQUE(flight_id, seat_number) |

---

### 6. `airlines`

| Field         | Type     | Description |
|---------------|----------|-------------|
| id            | integer  | Primary key |
| name          | string   | Unique |
| code          | string   | IATA/ICAO code |
| country       | string   | Country of origin |
| status        | enum     | ACTIVE, INACTIVE |
| created_at    | datetime | Auto-set |
| updated_at    | datetime | Auto-update |

---

### 7. `ticket_status_log`

| Field         | Type     | Description |
|---------------|----------|-------------|
| id            | integer  | Primary key |
| ticket_id     | integer  | FK → `tickets.id` |
| old_status    | enum     | Previous status |
| new_status    | enum     | New status |
| changed_at    | datetime | Timestamp |
| changed_by    | integer  | FK → `users.id` |

---

## 🔗 Relationships

- `users` → `purchase_history` (1:N)
- `users` → `tickets` (1:N)
- `users` → `ticket_status_log` (1:N)
- `purchase_history` → `tickets` (1:N)
- `flights` → `tickets` (1:N)
- `flights` → `seats` (1:N)
- `flights` → `airlines` (N:1)
- `tickets` → `seats` (1:1 optional)
- `tickets` → `ticket_status_log` (1:N)

---

## Enum Values

### User Status
- ACTIVE
- INACTIVE
- DELETED

### User Type
- CUSTOMER
- COMPANY_ADMIN
- SYSADMIN

### Purchase Status
- ACTIVE
- PLANNED
- PAST

### Payment Method
- CREDIT
- DEBIT
- PIX
- CASH

### Flight Status
- SCHEDULED
- CANCELLED

### Seat Class
- ECONOMY
- BUSINESS
- FIRST

### Ticket Status
- MARKED
- RESERVED
- CANCELLED
- COMPLETED
