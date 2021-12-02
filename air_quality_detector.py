#Interface documentation is in external_tool module.

import external_tool
import calc_tool
import ui_tool



def find_center_coordinate(location: str) -> None:
    """Use interface Geocoding to get the latitude and longtitude of the given location.
        Return them as a tuple.
    """
    f_geocode = None
    if 'CENTER NOMINATIM' in location:
        location = location.replace('CENTER NOMINATIM ', '')
        f_geocode = external_tool.GeoCodingAPI()
        f_geocode.get_data(location)
    else:
        location = location.replace('CENTER FILE ', '')
        f_geocode = external_tool.GeoCodingFile(location)
    return (f_geocode.latitude(), f_geocode.longtitude())


def describe_each_data_point(data_list: list, locations: str) -> None:
    """Given the air quality data and the location, first get an object of type GeoCoding, then for each data entry in the data given,
        print out the AQI value, the formatted coordinate, and perform reverse GeoCoding to get the description of the location at that coordinate.
    """
    reverse_machine = _generate_reverse_machine(locations)
    for data in data_list:
        print(f'AQI {calc_tool.convert_concentration_t_AQI(data[1])}')
        print(ui_tool.return_formatted_coordinate((data[27], data[28])))
        reverse_machine.get_data((data[27], data[28]))
        print(reverse_machine.describe())
        

            
def process_air_data(src: str, thres: int, range_miles: int, center_coord: tuple[float, float], num_search: int) -> list:
    """Get the air quality data, filer out unqualified data entry, sore the data by AQI value in descending order and
        return a list of data entries based on the number of data entries wanted (indicated by num_search)
    """
    data_list = _get_air_data(src)
    _filter_unqualified_data(data_list, thres, range_miles, center_coord)
    _sort_data_by_AQI_value(data_list)
    return data_list[:num_search]


def _generate_reverse_machine(locations: str) -> 'GeoCodingAPI or GeoCodingFile':
    """Create and return an object of interface GeoCoding that is specifically for doing reverse geocoding."""
    if locations == 'REVERSE NOMINATIM':
        return external_tool.GeoCodingAPI(reverse=True)
    locations = locations.replace('REVERSE FILES ', '').split()
    return external_tool.GeoCodingFile(locations, reverse=True)


def _get_air_data(src: str) -> list:
    """Create and return an object of interface AirQuality that will store the air quality data downloaded from the given source."""
    if 'AQI PURPLEAIR' in src:
        return external_tool.AirQualityAPI().report()
    src = src.replace('AQI FILE ', '')
    data = external_tool.AirQualityFile(src)
    return data.report()


def _filter_unqualified_data(data_list: list, thres: int, range_miles: int, center_coord: tuple[float, float]) -> None:
    """Filter out all the unqualified air data entry: those that are not within the given range, below the minimum AQI threshold,
       have missing data elements, and those where the last recorded time exceeds an hour.
    """
    for data in list(data_list):
        try:
            assert data[1] >= 0
            assert _is_data_AQI_acceptable(data[1], thres)
            assert data[4] <= 3600
            assert data[25] == 0
            assert type(data[27]) == float or type(data[27]) == int
            assert type(data[28]) == float or type(data[28]) == int
            assert _is_data_within_range(range_miles, center_coord, (data[27], data[28]))
        except:
            data_list.remove(data)


def _sort_data_by_AQI_value(data_list: list) -> None:
    """Sore the list of data entries by their AQI values in descending order."""
    data_list.sort(reverse=True, key=lambda x: x[1])


def _is_data_AQI_acceptable(conc: float, thres: int) -> bool:
    """Check whether the data's AQI value meets the minimum threshold given."""
    return calc_tool.convert_concentration_t_AQI(conc) >= thres


def _is_data_within_range(range_miles: int, fst_coord, sec_coord) -> bool:
    """Check whether the distance between two coodinates given is within the specified range."""
    return (calc_tool.calc_equirect_dist(fst_coord, sec_coord) <= range_miles)  


def run():
    """Control the flow of the program by getting the user's inputs and call other functions to perform operations and output information.
        If error arises, the program output formatted error message and stop.
    """
    try:
        center = ui_tool.get_center_location()
        range_in_miles = ui_tool.get_range()
        threshold_aqi = ui_tool.get_threshold_aqi()
        max_search = ui_tool.get_max_search()
        data_source = ui_tool.get_data_source()
        locations = ui_tool.get_reverse_source(max_search)
        center_coordinate = find_center_coordinate(center)
        print('CENTER', ui_tool.return_formatted_coordinate(center_coordinate))
        air_data = process_air_data(data_source, threshold_aqi, range_in_miles, center_coordinate, max_search)
        describe_each_data_point(air_data, locations)
    except external_tool.Error as err:
        err.display_error()
        

if __name__ == '__main__':
    run()

