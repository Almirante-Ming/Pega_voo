from enum import Enum

class User_Type(Enum):
    CUSTOMER = "customer"
    C_ADMIN= "c_admin"
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
    ACTIVE = "ativas"
    PLANNED = "planejadas"
    PAST = "passadas"

class Flight_Status(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"

class Flight_Class(Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"