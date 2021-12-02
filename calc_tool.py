# Name: Duong Hoang Thuy Vu - ID: 61624943

import decimal
import math

def calc_equirect_dist(first_coord: tuple[float, float], sec_coord: tuple[float, float]) -> float:
    """Calculate and return the equirectangular distance between two coordinates."""
    dlat = math.radians(sec_coord[0] - first_coord[0])
    dlon = math.radians(sec_coord[1] - first_coord[1])
    alat = math.radians((first_coord[0] + sec_coord[0])/2)        
    R = 3958.8
    x = dlon * math.cos(alat)
    return R * (math.sqrt(x**2 + dlat**2))




def convert_concentration_t_AQI(conc: float) -> int:
    """Convert and return AQI value associated with the given pm concentration based on the specified formula."""
    result = 0
    if 0.0 <= conc < 12.1:
        result = decimal.Decimal(0 + (conc - 0.0)*(50/12.0))
    elif 12.1 <= conc < 35.5:
        result = decimal.Decimal(51 + (conc - 12.1)*((100-51)/(35.4-12.1)))
    elif 35.5 <= conc < 55.5:
        result = decimal.Decimal(101 + (conc - 35.5)*((150-101)/(55.4-35.5)))
    elif 55.5 <= conc < 150.5:
        result = decimal.Decimal(151 + (conc - 55.5)*((200-151)/(150.4-55.5)))
    elif 150.5 <= conc < 250.5:
        result = decimal.Decimal(201 + (conc - 150.5)*((300-201)/(250.4-150.5)))
    elif 250.5 <= conc < 350.5:
        result = decimal.Decimal(301 + (conc - 250.5)*((400-301)/(350.4-250.5)))
    elif 350.5 <= conc < 500.5:
        result = decimal.Decimal(401 + (conc - 350.5)*((500-401)/(500.4-350.5)))
    else:
        result = decimal.Decimal(501)
    return int(result.to_integral_value(rounding=decimal.ROUND_HALF_UP))
