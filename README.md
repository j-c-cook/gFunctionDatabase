# gFunctionLibrary

A submodule of the GLHE Design Tool, containing libraries of g-functions, access and accurate interpolation

The libraries of g-functions available are the following:


| Configuration Name 	| Number of cases 	| Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                           	|
|--------------------	|-----------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Rectangle          	| 1651            	| Standard NxM cases (i.e. N rows, M columns) with uniform spacing. Only one key is required to access a specific configuration.                                                                                                                                                                                                                                                                                                                                  	|
| Zoned Rectangle    	| 12615           	| Similar to the Rectangle configurations, this configuration type has had rows/ columns removed from the interior in order to represent configurations where the interior spacing of the borefield is greater than the exterior (or perimeter) spacing. This library defines a specific configuration using the N and M values for the exterior as well as Ni and Mi values for the interior section. Two keys are required to access a specific configuration.  	|
| Open Rectangle     	| 2332            	| These configurations represent N by M rectangular cases where boreholes are only located around the perimeter, but the perimeter can have more than one row of boreholes. The number of rows around the perimeter is defined by an integer number ranging from 1-3. Two keys are required to access a specific configuration.                                                                                                                                   	|
| C                  	| 4525            	| This type of configuration may be thought of as an open rectangle configuration that has had some number of boreholes removed from the top side. The current C configurations in the library all have one row of boreholes around the perimeter. The number of holes removed is the secondary key integer value. The range of values depend on the configuration. Two keys are required to access a specific configuration.                                     	|
| L                  	| 495             	| These configurations consist of a line of N boreholes and M boreholes wide. The L cases have a single row of boreholes. Only one key is required to access a specific configuration.                                                                                                                                                                                                                                                                            	|
| U                  	| 3248            	| This type of configuration is U-shaped, with the opening at the top. The U may have up to 3 perimeter rows of boreholes around all sides of the U. The number of rows around the perimeter is defined by an integer ranging from 1-3. Two keys are required to access a specific configuration.                                                                                                                                                                 	|
| LopU (Lopsided U)  	| 9455            	| These configurations consist of U cases that have had some number of boreholes removed from their right side. These configurations all have a single rows of perimeter boreholes. The secondary key is an integer that is represented by the number of boreholes removed. There are two keys required to access a specific configuration.                                                                                                                       	|

# Documentation
See the online documentation at <a href="https://gfunctionlibrary.readthedocs.io/en/latest/" target="_blank">ReadTheDocs</a> and an offline [g-function library guide](https://github.com/j-c-cook/gFunctionLibrary/tree/main/Reports/g-function_library_overview.pdf) report in pdf format. 

# Acknowledgements

The need for a database of g-functions would not have been realized by the developer(s) without the Department of Energy contract DE-AC05-00OR22725, via a subcontract from Oak Ridge National Laboratory. Computation of the database g-functions was made possible
by the Oklahoma State University High Performance Computing Center. Development of the g-function calculation tool, cpgfunction, was supported via the OG&E Energy Technology Chair. 
