from enum import Enum

class User_Type(Enum):
    CUSTOMER = "customer"
    COMPANY_ADMIN = "company_admin"
    SYSADMIN = "sysadmin"
    
class User_Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    
class Booking_Status(Enum):
    MARKED = "marked"
    RESERVED = "reserved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Purchase_Status(Enum):
    ACTIVE = "active"
    PLANNED = "planned"
    PAST = "past"

class Payment_Method(Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    PIX = "pix"
    CASH = "cash"

class Flight_Status(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class Seat_Class(Enum):
    ECONOMY = "economy"
    PREMIUM = "premium"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"