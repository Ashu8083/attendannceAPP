from enum import Enum 

class AttendanceStatus(str, Enum):

    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    #HALF_DAY = "HALF_DAY"
    LEAVE = "LEAVE"