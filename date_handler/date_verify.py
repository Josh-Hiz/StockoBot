# File to contain methods to verify the date and time of a stock
from datetime import datetime
from re import T

def convert_timestamp(date_time):
    '''
    Convert time stamp string to datetime object
    '''
    ALLOWED_STRING_FORMATS = ["%Y/%m/%d-%H:%M:%S", "%Y/%m/%d"]
    for format in ALLOWED_STRING_FORMATS:
        try:
            d = datetime.strptime(date_time, format)
            return d
        except ValueError:
            pass
    raise ValueError
    
# Return a tuple of left and right time points
def verify_range(date1:str, date2:str):
    """
    Will parse the date strings and pass them to convert_timestamp
    """
    if(date2 == "Present"): 
        try:
            right_time_point = datetime.today()
            left_time_point = convert_timestamp(date1)
        except ValueError:
            raise ValueError
    else:
        try:
            right_time_point = convert_timestamp(date2)
            left_time_point = convert_timestamp(date1)
        except ValueError:
            raise ValueError
    return (left_time_point,right_time_point)

def validate_time(left_time_point, right_time_point):
    """
    Validate the time points to make sure they are in a valid range
    """
    return not (left_time_point > right_time_point or right_time_point > datetime.today() or left_time_point > datetime.today())