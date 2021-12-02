"Where are some places where the air quality is unhealthy within 30 miles of where I am now?", that would be the kind of question that this program will help to answer. 

I have not implemented a GUI application for the program so the program will only work with user input into the shell for now. First of all, the program will read a sequence of lines of input from the Python shell that configure its behavior (look at the example below), then generate and print some output consistent with that configuration. 
The  goal of the program is this: Given a "center" point, a range (in miles), and an AQI threshold, and maximum number of locations to output, the program will print out a list of the locations within the given range of the center point having the worst AQI values that are at least as much as the threshold. 

For example, when user input in the following format:

CENTER NOMINATIM Bren Hall, Irvine, CA\
RANGE 30\
THRESHOLD 100\
MAX 5\
AQI PURPLEAIR\
REVERSE NOMINATIM

The program will output the following information: 

CENTER 33.64324045/N 117.84185686276017/W\
AQI 180\
33.53814/N 117.5998/W\
Garcilla Drive, Orange County, California, 92690, United States of America\
AQI 157\
33.690376/N 118.03055/W\
Orange County, California, United States of America\
AQI 154\
33.68315/N 117.66642/W\
Alton Parkway, Foothill Ranch, Lake Forest, Orange County, California, 92610, United States of America\
AQI 152\
33.816/N 118.23275/W\
Arco, Tesoro Carson Refinery, Bangle, Carson, Los Angeles County, California, 90810, United States of America\
AQI 151\
33.86117/N 117.96228/W\
1880, West Southgate Avenue, Fullerton, Orange County, California, 92833, United States of America

(the results change in according to the time the program is used, this is only a sample)




