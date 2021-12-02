# Name: Duong Hoang Thuy Vu - ID: 61624943

class InvalidInputError(Exception):
    pass


def get_center_location() -> 'Object':
    """Ask user for a center location (string) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    center = input()
    try:
        assert ('CENTER NOMINATIM' in center) or ('CENTER FILE' in center)
        if 'CENTER NOMINATIM' in center:
            assert len(center.replace('CENTER NOMINATIM ', '')) > 0
        else:
            assert len(center.replace('CENTER FILE ', '')) > 0
        return center
    except:
        raise InvalidInputError()


def get_range() -> int:
    """Ask user for a range (integer) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    range_miles = input().split()
    try:
        assert int(range_miles[1]) >= 0
        return int(range_miles[1])
    except:
        raise InvalidInputError()


def get_threshold_aqi() -> int:
    """Ask user for a threshold value (integer) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    thres = input().split()
    try:
        assert int(thres[1]) >= 0
        return int(thres[1])
    except:
        raise InvalidInputError()


def get_max_search() -> int:
    """Ask user for a max number of searched wanted (integer) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    num_max = input().split()
    try:
        assert int(num_max[1]) > 0
        return int(num_max[1])
    except:
        raise InvalidInputError()


def get_data_source() -> str:
    """Ask user for a data source (string) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    source = input()
    try:
        assert (source == 'AQI PURPLEAIR') or ('AQI FILE' in source)
        if 'AQI FILE' in source:
            assert len(source.replace('AQI FILE', '')) > 0
        return source
    except:
        raise InvalidInputError()


def get_reverse_source(num_search: int) -> str:
    """Ask user for a source to get reverse geocoding information (string) and check whether the input meets the requirements.
        If input meets the requirement, return the input, else raise InvalidInputError.
    """
    locations = input()
    try:
        assert (locations == 'REVERSE NOMINATIM') or ('REVERSE FILES' in locations)
        if 'REVERSE FILES' in locations:
            assert len(locations.replace('REVERSE FILES', '')) > 0
            assert len(locations.replace('REVERSE FILES', '').split()) >= num_search
        return locations
    except:
        raise InvalidInputError()


def return_formatted_coordinate(coordinate: tuple[float, float]) -> None:
    """Return the formatted coordinate as a string."""
    lat, lon = coordinate
    return f'{_lat_formatted(lat)} {_long_formatted(lon)}'


def _long_formatted(longtitude: float) -> str:
    """Format the longtitude into a string"""
    long_format_str = f"{longtitude}/E" if longtitude >= 0 else f"{abs(longtitude)}/W"
    return long_format_str


def _lat_formatted(latitude: float) -> str:
    """Format the latitude into a string."""
    lat_format_str = f"{latitude}/N" if latitude >= 0 else f"{abs(latitude)}/S"
    return lat_format_str
