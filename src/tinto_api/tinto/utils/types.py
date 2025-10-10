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