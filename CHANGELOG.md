# History of changes

## Version 0.2

### Changes

- [Issue 17](https://github.com/j-c-cook/gFunctionLibrary/issues/17) - The projects name is modified from `gFunctionLibrary` to `gFunctionDatabase` to more accurately describe its contents. The database contains both the data and the database management system (DBMS). 

### Documents

- [Issue 13](https://github.com/j-c-cook/gFunctionLibrary/issues/13) - Update the table of contents in the README with the library contents from the Oak Ridge report. 
- [Issue 12](https://github.com/j-c-cook/gFunctionLibrary/issues/12) - Adds in a `Reports/` folder. A report written for Oak Ridge National Laboratory is the first of the reports to be included in the reports folder. The g-function library over view report discusses the contents of the library and how it was computed.
- [Issue 11](https://github.com/j-c-cook/gFunctionLibrary/issues/11) - Adds in acknowledgments to Oak Ridge National Laboratory and Dr. Jeffrey Spitler in the README file.

### Enhances

- [Issue 16](https://github.com/j-c-cook/gFunctionDatabase/issues/16) - The U configurations file was limited. Many of the layouts (NxM) did not have a single layer of thickness, but rather contained just double and triple U configurations. This update seeks to flesh out the missing configurations.

### New features

- [Issue 25](https://github.com/j-c-cook/gFunctionDatabase/issues/25) - A base object for [retrieval.py](https://github.com/j-c-cook/gFunctionDatabase/tree/main/gFunctionDatabase/Management/retrieval.py) is added. The object has a load_data method that takes in a configuration string argument, loads the specific database configuration file into memory and returns the entire file as a dictionary.
- [Issue 24](https://github.com/j-c-cook/gFunctionDatabase/issues/24) - A base object for the database management module [data_definition.py](https://github.com/j-c-cook/gFunctionDatabase/tree/main/gFunctionDatabase/Management/data_definition.py) is created. The object registers the available configurations into an instance refered to as `registry`. The registry contains quick access to the path of a configuration given a key input of L, U, LopU, Open, rectangle or zoned.  
- [Issue 23](https://github.com/j-c-cook/gFunctionDatabase/issues/23) - A function named find_data_files is defined in [available.py](https://github.com/j-c-cook/gFunctionDatabase/tree/main/gFunctionDatabase/Database/available.py) that locates and returns the file paths of all the configurations in the database.
- [Issue 22](https://github.com/j-c-cook/gFunctionDatabase/issues/22) - A configuration object is added to the [available.py](https://github.com/j-c-cook/gFunctionDatabase/tree/main/gFunctionDatabase/Database/available.py) module. This class seeks to serve as the base class for many of the database management modules. The instances provided here are user defined and pertain to the json levels. 
- [Issue 14](https://github.com/j-c-cook/gFunctionLibrary/issues/14) - A Python `tests/` folder is created and a yml file is created that runs tests on a local server. 
- [Issue 10](https://github.com/j-c-cook/gFunctionDatabase/issues/10) - The following is a list of new database files added: C, L and LopU configurations. The existing data files were rectangle, zoned, U, and open configurations. 

## Version 0.1.12 (2021-05-18)

### New features

- [Issue 5](https://github.com/j-c-cook/gFunctionLibrary/issues/5) - Add functionality to the fileio module that can read any `csv`, `xlsx` or `json` and return a dictionary with one function.


