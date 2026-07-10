from geopy.distance import geodesic

def get_distance(office_latitude, office_longitude, employee_latitude, employee_longitude):

    office = (
        office_latitude,
        office_longitude,
    )
    employee = (
        employee_latitude,
        employee_longitude,
    )

    distance = geodesic(office, employee)
    return distance