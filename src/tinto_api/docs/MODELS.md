# Data Models Documentation

This document describes the data models for the Tinto API flight booking system based on the Entity-Relationship Diagram (DER).

## Overview

The system manages flight bookings with the following main entities:
- **Usuario** (User/Person) - System users and passengers
- **Histórico de Compras** (Purchase History) - User purchase records
- **Passagem** (Ticket) - Flight tickets/bookings
- **Voos** (Flights) - Flight information
- **Companhia** (Airline) - Airlines/companies

## Models

### 1. Person
*Table: `persons`*

- id: integer, primary key, autoincrement
- name: string, not null (full name)
- cpf: string, unique, not null (Brazilian CPF document)
- dt_birth: string, not null (date of birth)
- gender: enum, not null
- phone: string, not null
- email: string, unique, not null
- hashed_password: string, nullable (encrypted password)
- state: enum(User_Status), default ACTIVE (account status)
- p_type: enum(User_Type), default CUSTOMER (user type)
- dt_create: datetime, auto-set (creation timestamp)
- dt_update: datetime, auto-update (last update timestamp)

**Relationships:**
- One-to-Many with Purchase History
- Many-to-Many with Tickets (as passengers)

### 2. Purchase History (Histórico de Compras)
*Table: `purchase_history`*

- id: integer, primary key, autoincrement
- user_id: integer, foreign key, not null (reference to Person)
- status: enum, not null (purchase status)
- destiny: string, not null 
- origin: string, not null
- dt_create: datetime, auto-set (purchase date)
- dt_update: datetime, auto-update (last update timestamp)

**Status Types:**
- ativas (Active) - Currently active bookings
- planejadas (Planned) - Future/planned bookings  
- passadas (Past) - Completed bookings

**Relationships:**
- Many-to-One with Person
- One-to-Many with Tickets

### 3. Ticket (Passagem)
*Table: `tickets`*

- id: integer, primary key, autoincrement
- purchase_history_id: integer, foreign key, not null (reference to Purchase History)
- flight_id: integer, foreign key, not null (reference to Flight)
- passengers: json/text, not null (passenger information list)
- valor: decimal, not null (ticket price)
- horario_embarque: datetime, not null (boarding time)
- horario_desembarque: datetime, not null (arrival time)
- status: enum(Booking_Status), default MARKED (booking status)
- dt_create: datetime, auto-set (creation timestamp)
- dt_update: datetime, auto-update (last update timestamp)

**Relationships:**
- Many-to-One with Purchase History
- Many-to-One with Flight
- Many-to-Many with Person (passengers)

### 4. Flight (Voos)
*Table: `flights`*

- id: integer, primary key, autoincrement
- airline_id: integer, foreign key, not null (reference to Airline)
- flight_number: string, unique, not null (flight identifier)
- origin: string, not null (origin airport/city)
- destiny: string, not null (destination airport/city)
- f_class: enum, not null, default economy (flight class)
- departure: datetime, not null (scheduled departure)
- arrival: datetime, not null (scheduled arrival)
- a_seats: integer, not null (available seat count)
- t_seats: integer, not null (total seat capacity)
- status: enum, default SCHEDULED (flight status)
- dt_create: datetime, auto-set (creation timestamp)
- dt_update: datetime, auto-update (last update timestamp)

**Class Types:**
- economy - Economy class
- business - Business class 

**Relationships:**
- Many-to-One with Airline
- One-to-Many with Tickets

### 5. Airline (Companhia)
*Table: `airlines`*

- id: integer, primary key, autoincrement
- name: string, unique, not null (airline name)
- code: string, unique, not null (IATA/ICAO airline code)
- country: string, not null (country of origin)
- status: enum, default ACTIVE (airline status)
- dt_create: datetime, auto-set (creation timestamp)
- dt_update: datetime, auto-update (last update timestamp)

**Relationships:**
- One-to-Many with Flights

## Enumerations

### User_Status
- ACTIVE - Active user account
- INACTIVE - Temporarily inactive
- DELETED - Soft deleted account

### User_Type  
- CUSTOMER - Regular customer
- C_ADMIN - Company administrator
- SYSADMIN - System administrator

### Booking_Status
- MARKED - Initial booking state
- RESERVED - Confirmed reservation
- CANCELLED - Cancelled booking
- COMPLETED - Completed journey

### Flight_Status
- SCHEDULED - Scheduled flight
- CANCELLED - Cancelled flight

### Flight_Class
- ECONOMY - Economy class
- BUSINESS - Business class
- FIRST - First class

## Relationships Summary

```
Person (1) ←→ (N) Purchase_History
Purchase_History (1) ←→ (N) Ticket
Ticket (N) ←→ (1) Flight
Flight (N) ←→ (1) Airline
Person (N) ←→ (N) Ticket (passengers)
```

## Database Constraints

### Unique Constraints
- Person: cpf, email
- Airline: name, code
- Flight: flight_number

### Foreign Key Constraints
- All relationships maintain referential integrity
- Cascade deletion policies apply where appropriate

### Check Constraints
- CPF format validation
- Email format validation
- Phone format validation
- Date validations (birth date, flight times)
- Price validations (positive values)

## Notes

- All timestamps use UTC timezone
- Soft deletion is implemented via status fields
- Passenger information in tickets supports multiple passengers per booking
- Flight capacity management through available_seats tracking
- Price calculations may include dynamic pricing based on demand