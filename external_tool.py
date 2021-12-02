# Name: Duong Hoang Thuy Vu - ID: 61624943

"""Interface documentation
_Interface GeoCoding: If object is of type GeoCoding then object has some common method:
    1) method get_data() which if called will get the data needed for object to perform (forward/reverse) geocoding later.
    2) method describe() which if called will return the description of the location requested
    3) method latitude() which if called will return the latitude of the location requested
    4) method longtitude() which if called will return the longtitude of the location requested.


_Interface AIrQuality: If object is of type AirQuality then object should be able to get and store the air quality data. Object's common method is:
    1) method report() which if called will return a copy of the data.
"""
import pathlib
import json
import urllib.parse
import urllib.request


class Error(Exception):
    """This class acts similar to an Exception with an additional method display_error()"""
    def __init__(self, link: str, mess: str, status=None):
        self._link = link
        self._status = status
        self._mess = mess

    def display_error(self) -> None:
        """Display error in a specific format including the status code(if available), url, and an error message"""
        print('\nFAILED')
        if self._status:
            print(type(self._status))
            print('hi')
            print(self._status, self._link)
        else:
            print(self._link)
        print(self._mess)



class GeoCodingAPI():
    """This class acts like a NominatimAPI which can perform forward geocoding and reverse geocoding based on the boolean value of reverse parameter.
        If forward geocoding, input location description into get_data() method. If reverse geocoding, input coodinate as a tuple into get_data() method.
    """
    def __init__(self, reverse=False):
        self._reverse = reverse
        self._url = str()
        self._data = None
        
    def _build_search_url(self, search_target: str) -> None:
        """Construct a URL for searching based on the input search target string and assign that to attribute _url of object."""
        if not self._reverse:
            encoded_parameter = urllib.parse.urlencode({'q': search_target, 'format': 'json', 'limit': 1})
            self._url = f'https://nominatim.openstreetmap.org/search?{encoded_parameter}'

    def _build_reverse_url(self, coordinate: tuple) -> None:
        """Construct a URL for reverse geocoding based on the input coordinate and assign that to attribute _url of object."""
        if self._reverse:
            lat, lon = coordinate
            encoded_parameter = urllib.parse.urlencode({'lat': lat, 'lon': lon, 'format': 'json', 'limit': 1})
            self._url = f'https://nominatim.openstreetmap.org/reverse?{encoded_parameter}'
        
    def get_data(self, search_target: str) -> None:
        """Use the url stored inside the object to get the data from the API."""
        if self._reverse == False:
            self._build_search_url(search_target)
        else:
            self._build_reverse_url(search_target)
        self._data = _get_data_from_API(self._url, is_nominatim=True)
    
    def describe(self) -> str:
        """Return the description of the location as a string."""
        return self._data['display_name']

    def longtitude(self) -> float:
        """Return the longtitude of the location."""
        return float(self._data['lon'])

    def latitude(self) -> float:
        """Return the latitude of the location."""
        return float(self._data['lat'])



class AirQualityAPI():
    """This class acts as the PurpleAir API which can download air data from PurpleAir and store it in the data attribute of the class."""
    def __init__(self):
        self._url = 'https://www.purpleair.com/data.json'
        self._data = self._get_data()

    def _get_data(self) -> dict:
        """Return the air data downloaded from the API"""
        data = _get_data_from_API(self._url, is_nominatim=False)
        return data['data']
        
    def report(self):
        """Return a copy of the air data."""
        return list(self._data)



class GeoCodingFile():
    """This class acts as a local geocoding device which can perform forward geocoding and reverse geocoding based on the boolean value of reverse parameter.
        If forward geocoding, input a filepath in the parameter when creating the object. If reverse geocoding, input a list of filepaths and set reverse to True
        in the object's paramter.
    """
    def __init__(self, file_path: 'list of filepath/filepath', reverse: bool=False):
        self._reverse = reverse
        self._data = None
        if self._reverse == True:
            self._file_path_list = file_path
            self._count = 0
            self._file_path = None
        else:
            self._file_path = pathlib.Path(file_path)
            self.get_data()
            
    def _next_file_path(self):
        """Initiates the _file_path attribute of the object with an element stored in _file_path_list.
            The element is chosen based on the order of element's index in the list of filepaths.
            Reaching the end of the file path list will reset the function to take element from the first element again.
        """
        if 0 <= self._count < len(self._file_path_list):
            self._file_path = pathlib.Path(self._file_path_list[self._count])
            self._count += 1
        if self._count >= len(self._file_path_list):
            self._count = 0
        
    def get_data(self, search_target=None):
        """Get the data from the file using the filepath in _file_path attribute and assign the data to _data attribute of object."""
        if self._reverse == True:
            self._next_file_path()
        self._data = _initialize_data_from_file(self._file_path)
        self._data = self._data[0] if type(self._data) == list else self._data
        
    def describe(self):
        """Return the description of the location as a string."""
        return self._data['display_name']

    def longtitude(self):
        """Return the longtitude of the location."""
        return float(self._data['lon'])

    def latitude(self):
        """Return the latitude of the location."""
        return float(self._data['lat'])


class AirQualityFile():
    """This class acts as a local PurpleAir API which can get air data from file path and store it in the _data attribute of the class."""
    def __init__(self, file_path):
        self._file_path = pathlib.Path(file_path)
        self._data = _initialize_data_from_file(self._file_path)['data']
        
    def report(self):
        """Return a copy of the air data."""
        return list(self._data)


def _get_data_from_API(url: pathlib.Path, is_nominatim: bool) -> dict:
    """Send request to the server, check and decode the data downloaded from the server.
        Raise format error if file is not in json format, raise Not 200 Error if server response's status code is not 200,
        raise Network error if unable to connect to the internet. If no error, return the decoded version of the data.
    """
    response = None
    try:
        response = _send_request_online(url, is_nominatim)
        json_text = response.read().decode(encoding = 'utf-8')
        data = json.loads(json_text)
        return _check_matching_data_type(data)
    except urllib.error.HTTPError as err:
        raise Error(url, 'NOT 200', err.status)
    except (urllib.error.URLError, ConnectionAbortedError):
        raise Error(url, 'NETWORK')
    except (AssertionError, json.decoder.JSONDecodeError):
        raise Error(url, 'FORMAT', response.status)
    finally:
        if response != None:
            response.close()


def _send_request_online(url: pathlib.Path, is_nominatim: bool) -> 'http.client.HTTPResponse':
    """Send request to the server using the url given and return the response gotten back from server."""
    request = urllib.request.Request(url)
    if is_nominatim:
        request.add_header('Referer', r'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/duonghv1')
    response = urllib.request.urlopen(request)
    if response.status != 200:
        raise Error(url, 'NOT 200', response.status)
    return response


def _check_matching_data_type(data: 'list or dict') -> dict:
    """Check if data type is properly formatted (data's type is a dictionary or a list) and return data as a dictionary.
        If not, raise Assertionerror.
    """
    if type(data) == list:
        assert (len(data) == 1) and (type(data[0]) == dict)
        assert len(data[0]) > 0
        return data[0]
    elif type(data) == dict:
        assert len(data) > 0
        return data
    else:
        assert False
    

def _initialize_data_from_file(file_path: pathlib.Path) -> 'list or dict':
    """Get the data from the file using the file path given, decode that file and return the decoded data if no error occurs.
        Raise Format error if file is not in json format, raise Missing Error if file path does not exist or cannot be opened.
    """
    myfile = None
    try:
        myfile = file_path.open('r', encoding = 'utf-8')
        data = json.loads(myfile.read())
        assert len(data) > 0
        return data
    except (AssertionError, json.decoder.JSONDecodeError):
        raise Error(file_path, 'FORMAT')
    except:
        raise Error(file_path, 'MISSING')
    finally:
        if myfile != None:
            myfile.close()

