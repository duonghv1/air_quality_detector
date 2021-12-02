Nowadays, the Internet provides a valuable resource to help us to monitor and manage the impact of air quality. The program can help users answer the following question: Where are some places where the air quality is unhealthy within 30 miles of where I am now?

The program will read a sequence of lines of input from the Python shell that configure its behavior, then generate and print some output consistent with that configuration. The general goal of the program is this: Given a "center" point, a range (in miles), and an AQI threshold, describe the locations within the given range of the center point having the  worst AQI values that are at least as much as the threshold. 

For example, when user input in the following format:

CENTER NOMINATIM Bren Hall, Irvine, CA
RANGE 30
THRESHOLD 100
MAX 5
AQI PURPLEAIR
REVERSE NOMINATIM

The program will output the following information: (the results change in according to the time the program is used, this is only a sample)
CENTER 33.64324045/N 117.84185686276017/W
AQI 180
33.53814/N 117.5998/W
Garcilla Drive, Orange County, California, 92690, United States of America
AQI 157
33.690376/N 118.03055/W
Orange County, California, United States of America
AQI 154
33.68315/N 117.66642/W
Alton Parkway, Foothill Ranch, Lake Forest, Orange County, California, 92610, United States of America
AQI 152
33.816/N 118.23275/W
Arco, Tesoro Carson Refinery, Bangle, Carson, Los Angeles County, California, 90810, United States of America
AQI 151
33.86117/N 117.96228/W
1880, West Southgate Avenue, Fullerton, Orange County, California, 92833, United States of America




